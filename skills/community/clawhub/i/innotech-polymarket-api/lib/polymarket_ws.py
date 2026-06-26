#!/usr/bin/env python3
"""
Polymarket WebSocket Client - Real-time market data

Provides:
- WebSocket connection to Polymarket
- Market subscription management
- Order book tracking
- Price updates

Usage:
    from lib.polymarket_ws import PolymarketWS
    
    ws = PolymarketWS()
    await ws.connect()
    await ws.subscribe(["asset_id_1", "asset_id_2"])
    
    async def handle_update(data):
        print(f"Update: {data}")
    
    await ws.listen(handle_update)
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Callable, Any
import aiohttp


class PolymarketWS:
    """
    Real-time market data via WebSocket
    
    Endpoint: wss://ws-subscriptions-clob.polymarket.com/ws/market
    """

    WS_ENDPOINT = "wss://ws-subscriptions-clob.polymarket.com/ws/market"
    PING_INTERVAL = 10  # seconds

    def __init__(self):
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self.subscribed_assets: set = set()
        self.last_ping: float = 0
        self.running: bool = False

    async def connect(self):
        """Connect to WebSocket"""
        self.session = aiohttp.ClientSession()
        self.ws = await self.session.ws_connect(
            self.WS_ENDPOINT,
            heartbeat=None,
            timeout=aiohttp.ClientWSTimeout(ws_close=30.0)
        )
        self.running = True
        print("✅ Connected to Polymarket WebSocket")

    async def subscribe(self, asset_ids: List[str]):
        """
        Subscribe to market updates
        
        Args:
            asset_ids: List of asset IDs to subscribe
        """
        if not self.ws:
            raise RuntimeError("WebSocket not connected. Call connect() first.")
        
        msg = {
            "assets_ids": asset_ids,
            "type": "market",
            "custom_feature_enabled": True
        }
        await self.ws.send_json(msg)
        self.subscribed_assets.update(asset_ids)
        print(f"✅ Subscribed to {len(asset_ids)} assets")

    async def unsubscribe(self, asset_ids: List[str]):
        """
        Unsubscribe from market updates
        
        Args:
            asset_ids: List of asset IDs to unsubscribe
        """
        if not self.ws:
            return
        
        msg = {
            "assets_ids": asset_ids,
            "type": "unsubscribe"
        }
        await self.ws.send_json(msg)
        self.subscribed_assets.difference_update(asset_ids)
        print(f"✅ Unsubscribed from {len(asset_ids)} assets")

    async def send_ping(self):
        """Send PING to keep connection alive"""
        if time.time() - self.last_ping >= self.PING_INTERVAL:
            await self.ws.send_str("PING")
            self.last_ping = time.time()

    async def listen(self, callback: Callable[[Dict[str, Any]], None]):
        """
        Listen for updates with callback
        
        Args:
            callback: Async function to handle updates
            
        Event types:
            - book: Full order book snapshot (bids/asks at top level)
            - best_bid_ask: Best bid/ask prices
            - price_change: Price notification (less reliable)
        """
        if not self.ws:
            raise RuntimeError("WebSocket not connected. Call connect() first.")
        
        try:
            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == "PONG":
                        continue  # Heartbeat response
                    
                    try:
                        data = json.loads(msg.data)
                        await callback(data)
                    except json.JSONDecodeError:
                        pass
                
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print(f"❌ WebSocket error: {self.ws.exception()}")
                    break
                
                # Send heartbeat
                await self.send_ping()
        
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.running = False

    async def close(self):
        """Close WebSocket connection"""
        self.running = False
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()
        print("✅ WebSocket closed")

    @staticmethod
    def parse_orderbook(data: Dict) -> Dict[str, Any]:
        """
        Parse order book from WebSocket message
        
        IMPORTANT: 'book' event has bids/asks at TOP LEVEL, not under 'book' key!
        
        Args:
            data: WebSocket message dict
            
        Returns:
            Dict with parsed order book data
        """
        if data.get('event_type') != 'book':
            return {}
        
        # ✅ CORRECT: bids/asks at top level
        bids = data.get('bids', [])
        asks = data.get('asks', [])
        asset_id = data.get('asset_id', 'unknown')
        
        if not bids or not asks:
            return {
                'asset_id': asset_id,
                'bids': [],
                'asks': [],
                'best_bid': None,
                'best_ask': None,
                'liquidity': 0
            }
        
        best_bid = float(bids[0].get('price', 0))
        best_ask = float(asks[0].get('price', 0))
        best_bid_size = float(bids[0].get('size', 0))
        best_ask_size = float(asks[0].get('size', 0))
        
        # Calculate total liquidity
        total_liquidity = sum(float(b.get('size', 0)) for b in bids)
        total_liquidity += sum(float(a.get('size', 0)) for a in asks)
        
        return {
            'asset_id': asset_id,
            'bids': bids,
            'asks': asks,
            'best_bid': best_bid,
            'best_ask': best_ask,
            'best_bid_size': best_bid_size,
            'best_ask_size': best_ask_size,
            'liquidity': total_liquidity
        }
