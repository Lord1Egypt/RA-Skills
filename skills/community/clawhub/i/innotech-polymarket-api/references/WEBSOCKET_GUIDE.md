# Polymarket WebSocket Guide

Complete guide for connecting to Polymarket's real-time CLOB data streams.

**Author**: Calvin Lam  
**Last Updated**: 2026-03-23

---

## ⚠️ Critical: Use the CLOB WebSocket Endpoint

**✅ Correct Endpoint**: `wss://ws-subscriptions-clob.polymarket.com/ws/market`

❌ Old/legacy endpoint: `wss://ws-subscriptions.polymarket.com` (different protocol, different events)

---

## Connection & Subscription

### aiohttp (Recommended for async bots)

```python
import aiohttp, asyncio, json, time

async def monitor_market(asset_ids):
    async with aiohttp.ClientSession() as session:
        ws = await session.ws_connect(
            "wss://ws-subscriptions-clob.polymarket.com/ws/market",
            heartbeat=None,
            timeout=aiohttp.ClientWSTimeout(ws_close=30.0)
        )
        
        # Subscribe to assets
        await ws.send_json({
            "assets_ids": asset_ids,
            "type": "market",
            "custom_feature_enabled": True
        })
        
        # Heartbeat
        last_ping = time.time()
        
        async for msg in ws:
            if msg.data == "PONG":
                continue
            
            # Send PING every 10 seconds
            if time.time() - last_ping >= 10:
                await ws.send_str("PING")
                last_ping = time.time()
            
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                handle_event(data)

asyncio.run(monitor_market(["up_asset_id", "down_asset_id"]))
```

### websocket-client (Sync)

```python
import websocket, json, time

last_ping = time.time()

def on_message(ws, message):
    global last_ping
    if message == "PONG": return
    data = json.loads(message)
    handle_event(data)
    
    if time.time() - last_ping >= 10:
        ws.send("PING")
        last_ping = time.time()

ws = websocket.WebSocketApp(
    "wss://ws-subscriptions-clob.polymarket.com/ws/market",
    on_open=lambda ws: ws.send(json.dumps({
        "assets_ids": ["asset_1", "asset_2"],
        "type": "market",
        "custom_feature_enabled": True
    })),
    on_message=on_message
)
ws.run_forever()
```

---

## Event Types — Complete Reference

### 1. `book` — Full Orderbook Snapshot ⭐⭐⭐

**Most reliable source for bid/ask data**

```json
{
  "event_type": "book",
  "asset_id": "0x123...",
  "bids": [
    {"price": "0.45", "size": "1000"},
    {"price": "0.44", "size": "500"}
  ],
  "asks": [
    {"price": "0.47", "size": "800"},
    {"price": "0.48", "size": "300"}
  ]
}
```

**⚠️ CRITICAL: `bids` and `asks` at TOP LEVEL, not under `book` key**

```python
# ✅ CORRECT
bids = data.get('bids', [])
asks = data.get('asks', [])

# ❌ WRONG — returns empty
bids = data.get('book', {}).get('bids', [])
```

### 2. `best_bid_ask` — Best Bid/Ask Update ⭐⭐⭐

**Quick price check, no sizes included**

```json
{
  "event_type": "best_bid_ask",
  "asset_id": "0x123...",
  "best_bid": "0.45",
  "best_ask": "0.47"
}
```

### 3. `price_change` — Trade Record ❌ NOT ORDERBOOK

**Records PAST trades, NOT current orderbook state**

```json
{
  "event_type": "price_change",
  "asset_id": "0x123...",
  "price": "0.46",
  "side": "BUY",
  "size": "50"
}
```

**⚠️ MISCONCEPTION**: 
- `side: "BUY"` = someone BOUGHT at this price in the past
- This is NOT the current best ask
- Using `price_change` as bid/ask causes impossible states (ask < bid)
- **DO NOT USE for orderbook data**

### 4. `last_trade_price` — Last Trade ❌ NOT ORDERBOOK

```json
{
  "event_type": "last_trade_price",
  "asset_id": "0x123...",
  "price": "0.46"
}
```

**DO NOT USE for orderbook data**

---

## Reliability Matrix

| Event | Data Available | Is Orderbook? | Use For |
|-------|---------------|---------------|---------|
| `book` | Full bids[] + asks[] | ✅ YES | Bid/ask with sizes, liquidity |
| `best_bid_ask` | Best bid + ask price | ✅ YES | Quick price check |
| `price_change` | Last trade price + side | ❌ NO | Historical trades only |
| `last_trade_price` | Last trade price | ❌ NO | Historical trades only |

---

## Unsubscribe

```python
await ws.send_json({
    "assets_ids": ["old_asset_1", "old_asset_2"],
    "type": "unsubscribe"
})
```

---

## Reconnection with Exponential Backoff

```python
import aiohttp, asyncio, json

async def connect_with_retry(asset_ids, max_retries=10):
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                ws = await session.ws_connect(
                    "wss://ws-subscriptions-clob.polymarket.com/ws/market",
                    heartbeat=None,
                    timeout=aiohttp.ClientWSTimeout(ws_close=30.0)
                )
                await ws.send_json({
                    "assets_ids": asset_ids,
                    "type": "market",
                    "custom_feature_enabled": True
                })
                print(f"✅ Connected (attempt {attempt + 1})")
                
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT and msg.data != "PONG":
                        yield json.loads(msg.data)
                    
                    if msg.type in (aiohttp.WSMsgType.ERROR, aiohttp.WSMsgType.CLOSED):
                        break
                        
        except Exception as e:
            wait = min(2 ** attempt, 60)
            print(f"❌ Disconnected, retrying in {wait}s... ({e})")
            await asyncio.sleep(wait)
```

---

## Market Rotation Pattern

For 5-minute markets that rotate every 5 minutes:

```python
import time

async def rotation_loop():
    last_interval = None
    
    while True:
        current = (int(time.time()) // 300) * 300
        
        if current != last_interval:
            # New interval — rotate subscriptions
            last_interval = current
            
            # Unsubscribe old
            if old_assets:
                await ws.send_json({"assets_ids": old_assets, "type": "unsubscribe"})
            
            # Fetch new market, get new asset IDs
            new_assets = await fetch_new_assets(current)
            
            # Subscribe new
            await ws.send_json({"assets_ids": new_assets, "type": "market", "custom_feature_enabled": True})
        
        await asyncio.sleep(1)  # Check every second
```

**⚠️ Use interval-based detection, NOT time-based**:
```python
# ❌ WRONG: Off by up to 15 seconds
if time.time() - last_rotation >= 300: rotate()

# ✅ CORRECT: Instant detection
if (int(time.time()) // 300) * 300 != current_base: rotate()
```

---

## Best Practices

1. ✅ **PING every 10 seconds** to keep connection alive
2. ✅ **Only use `book` + `best_bid_ask`** for orderbook data
3. ✅ **Ignore `price_change` + `last_trade_price`** for orderbook
4. ✅ **Interval-based rotation** for time-based markets
5. ✅ **Auto-reconnect** with exponential backoff
6. ✅ **Batch subscribe/unsubscribe** when rotating markets
7. ✅ **Check `bids` and `asks` at top level** (not under `book`)

---

**Need REST API details?** See `API_REFERENCE.md`
**Need trading details?** See main `SKILL.md`
