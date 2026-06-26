import asyncio
import json
import time
import ccxt.pro as ccxt  # Advanced async crypto lib
import redis.asyncio as redis
from loguru import logger

class MarketDataFeed:
    def __init__(self, symbol, redis_url="redis://localhost:6379"):
        self.symbol = symbol
        self.exchange = ccxt.okx({'options': {'defaultType': 'swap'}})
        self.redis = redis.from_url(redis_url)
        self.pub_channel = f"tick_{symbol.replace('/', '')}"

    async def start(self):
        logger.info(f"Starting Data Feed for {self.symbol}")
        while True:
            try:
                # Subscribe to orderbook and trades
                orderbook = await self.exchange.watch_order_book(self.symbol)
                trades = await self.exchange.watch_trades(self.symbol)
                
                # Construct payload
                payload = {
                    "ts": time.time_ns(),
                    "bid": orderbook['bids'][0][0],
                    "ask": orderbook['asks'][0][0],
                    "bid_vol": orderbook['bids'][0][1],
                    "ask_vol": orderbook['asks'][0][1],
                    "last_price": trades[-1]['price'] if trades else 0
                }
                
                # Publish to Redis (Low Latency IPC)
                await self.redis.publish(self.pub_channel, json.dumps(payload))
                
            except Exception as e:
                logger.error(f"WS Error: {e}")
                await asyncio.sleep(1) # Reconnect backoff

    async def close(self):
        await self.exchange.close()