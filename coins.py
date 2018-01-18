import requests
import json
import datetime
import time
from peewee import *

db = MySQLDatabase(host = '127.0.0.1', user = 'root', passwd = '123456', database = 'coinmarketcap')

class Coin(Model):
    coin_id = CharField()
    name = CharField()
    symbol = CharField()
    rank = IntegerField()
    price_usd = FloatField(null=True)
    price_btc = FloatField(null=True)
    volume_24h_usd = FloatField(null=True)
    market_cap_usd = FloatField(null=True)
    available_supply = FloatField(null=True)
    total_supply = FloatField(null=True)
    max_supply = FloatField(null=True)
    percent_change_1h = FloatField(null=True)
    percent_change_24h = FloatField(null=True)
    percent_change_7d = FloatField(null=True)
    last_updated =  IntegerField(null=True)
    price_cny = FloatField(null=True)
    volume_24h_cny = FloatField(null=True)
    market_cap_cny = FloatField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

class Coinlog(Model):
    start = DateTimeField()
    end = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

class Global(Model):
    total_market_cap_usd = FloatField()
    total_24h_volume_usd = FloatField()
    bitcoin_percentage_of_market_cap = FloatField()
    active_currencies = IntegerField()
    active_assets = IntegerField()
    active_markets = IntegerField()
    last_updated = IntegerField()
    total_market_cap_cny = FloatField()
    total_24h_volume_cny = FloatField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db        

db.connect()

if not Coin.table_exists():
  db.create_tables([Coin])

if not Coinlog.table_exists():
  db.create_tables([Coinlog])  

if not Global.table_exists():
  db.create_tables([Global])    

response = requests.get('https://api.coinmarketcap.com/v1/ticker/?convert=CNY&limit=1500')

start = datetime.datetime.now()

ticker = json.loads(response.text)
# print ticker
print type(ticker)
for index,item in enumerate(ticker):
    # print index
    # print item['id']
    
    coin = Coin(
    coin_id = item['id'],
    name = item['name'],
    symbol = item['symbol'],
    rank = item['rank'],
    price_usd = item['price_usd'],
    price_btc = item['price_btc'],
    volume_24h_usd = item['24h_volume_usd'],
    market_cap_usd = item['market_cap_usd'],
    available_supply = item['available_supply'],
    total_supply = item['total_supply'],
    max_supply = item['max_supply'],
    percent_change_1h = item['percent_change_1h'],
    percent_change_24h = item['percent_change_24h'],
    percent_change_7d = item['percent_change_7d'],
    last_updated =  item['last_updated'],
    price_cny = item['price_cny'],
    volume_24h_cny = item['24h_volume_cny'],
    market_cap_cny = item['market_cap_cny'])

    coin.save()

coinlog = Coinlog(start=start) 
coinlog.save()   

response_global = requests.get('https://api.coinmarketcap.com/v1/global/?convert=CNY')

globaljson = json.loads(response_global.text)

globaldata = Global(
    total_market_cap_usd = globaljson['total_market_cap_usd'],
    total_24h_volume_usd = globaljson['total_24h_volume_usd'],
    bitcoin_percentage_of_market_cap = globaljson['bitcoin_percentage_of_market_cap'],
    active_currencies = globaljson['active_currencies'],
    active_assets = globaljson['active_assets'],
    active_markets = globaljson['active_markets'],
    last_updated = globaljson['last_updated'],
    total_market_cap_cny = globaljson['total_market_cap_cny'],
    total_24h_volume_cny = globaljson['total_24h_volume_cny'],
) 
globaldata.save()   

db.close()

