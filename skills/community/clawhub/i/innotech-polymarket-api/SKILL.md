---
name: innotech-polymarket-api
description: Polymarket API and data access guide. Learn how to connect, find markets, get real-time data via WebSocket, access order books, place orders via CLOB SDK, and understand market mechanics.
---

# Polymarket API & Data Access Guide

**Purpose**: Comprehensive reference for connecting to, understanding, and using Polymarket APIs  
**Last Updated**: 2026-03-23

---

## 🎯 What This Skill Covers

1. ✅ **Connect to Polymarket** - API endpoints, authentication
2. ✅ **Find Markets** - Search, filter, time-based pattern discovery
3. ✅ **Get Real-time Data** - WebSocket usage and event types
4. ✅ **Access Order Books** - Liquidity, bid/ask spreads, depth
5. ✅ **Place Orders** - CLOB SDK, market/limit orders, decimal precision
6. ✅ **Market Mechanics** - How 5-min markets work, winner determination, timing
7. ✅ **Known Pitfalls** - Data reliability, timing issues, common bugs

**This skill does NOT include**:
- ❌ Trading strategies
- ❌ Signal analysis methodology

---

## 🏗️ Architecture Overview

### **API Components**

| Component | URL | Purpose | Auth? |
|-----------|-----|---------|-------|
| **Gamma API** | `https://gamma-api.polymarket.com` | Market info, prices, metadata | No |
| **CLOB API** | `https://clob.polymarket.com` | Order books, trades, market structure | No |
| **CLOB Auth API** | `https://clob-auth.polymarket.com` | JWT token for trading | Yes |
| **Data API** | `https://data-api.polymarket.com` | Historical data, order books | No |
| **WebSocket** | `wss://ws-subscriptions-clob.polymarket.com/ws/market` | Real-time price/book updates | No |

### **Data Flow for 5-Minute BTC Up/Down Markets**

```
1. Generate timestamp → slug: btc-updown-5m-{timestamp}
2. Fetch market info from Gamma API → get asset IDs
3. Subscribe to WebSocket with asset IDs → real-time bid/ask
4. Place orders via CLOB SDK → buy UP or DOWN tokens
5. Market closes (5 min) → Polymarket resolves winner
6. Verify winner via Gamma API outcomePrices (1.0 = winner)
```

---

## 🔍 Finding Markets

### **5-Minute Markets — Timestamp Pattern**

```python
import time

def get_current_interval(interval_seconds=300):
    """Calculate current 5-minute interval timestamp"""
    current_time = int(time.time())
    return (current_time // interval_seconds) * interval_seconds

def generate_market_timestamps(num_markets=8):
    """Generate N market timestamps: current + next (N-1) intervals"""
    base = get_current_interval()
    return [base + i * 300 for i in range(num_markets)]

# Supported cryptos: btc, eth, sol, xrp
# Slug pattern: {crypto}-updown-5m-{timestamp}
# Example: btc-updown-5m-1772699400
```

### **API Search Methods**

```python
import requests

# By slug (most reliable for 5-min markets)
resp = requests.get("https://gamma-api.polymarket.com/markets", params={"slug": "btc-updown-5m-1772699400"})

# By keyword search
resp = requests.get("https://gamma-api.polymarket.com/markets", params={"_s": "bitcoin"})

# Active markets
resp = requests.get("https://gamma-api.polymarket.com/markets", params={"active": "true", "limit": 100})
```

---

## 🆔 Asset IDs (Token IDs)

**Critical**: Each outcome (UP/DOWN) has a unique asset ID required for WS subscriptions and trading.

### **Getting Asset IDs**

```python
import json

def get_asset_ids(market):
    """Get asset IDs from clobTokenIds field (preferred)"""
    clob_token_ids_str = market.get('clobTokenIds')
    if clob_token_ids_str:
        return json.loads(clob_token_ids_str)  # List of 2 IDs: [UP_ID, DOWN_ID]
    return []
```

**Important**:
- ✅ `clobTokenIds` is a **JSON string**, not an array — must `json.loads()`
- ✅ Index 0 = UP, Index 1 = DOWN (for btc-updown markets)
- ⚠️ Fall back to `tokens[].token_id` only if `clobTokenIds` missing

---

## 📡 WebSocket — Real-time Data

### **Connection & Subscription**

```python
import aiohttp, asyncio, json, time

async def monitor_market(asset_ids):
    async with aiohttp.ClientSession() as session:
        ws = await session.ws_connect(
            "wss://ws-subscriptions-clob.polymarket.com/ws/market",
            heartbeat=None,
            timeout=aiohttp.ClientWSTimeout(ws_close=30.0)
        )
        # Subscribe
        await ws.send_json({
            "assets_ids": asset_ids,
            "type": "market",
            "custom_feature_enabled": True
        })
        # Heartbeat every 10 seconds
        last_ping = time.time()
        async for msg in ws:
            if msg.data == "PONG": continue
            if time.time() - last_ping >= 10:
                await ws.send_str("PING")
                last_ping = time.time()
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                # Handle events...
```

### **⚠️ CRITICAL: Event Type Reliability**

| Event Type | Description | Reliability | Use? |
|------------|-------------|-------------|------|
| **`book`** | Full orderbook snapshot | ⭐⭐⭐ | ✅ YES |
| **`best_bid_ask`** | Best bid/ask update | ⭐⭐⭐ | ✅ YES |
| **`price_change`** | Past trade records | ⭐ | ❌ NO |
| **`last_trade_price`** | Last trade price | ⭐ | ❌ NO |

**🔥 Key Lesson**: `price_change` = past trades, NOT current orderbook state. Using it as real-time bid/ask causes **impossible states** (ask < bid). Only use `book` and `best_bid_ask`.

### **⚠️ CRITICAL: Book Event Structure**

```python
# ❌ WRONG: bids/asks are NOT under 'book' key
bids = data.get('book', {}).get('bids', [])  # EMPTY!

# ✅ CORRECT: bids/asks at TOP LEVEL
bids = data.get('bids', [])
asks = data.get('asks', [])
```

### **Order Book Fields**

```python
# Each bid/ask entry:
{
    'price': '0.4550',  # Price level (0-1)
    'size': '7270'      # Size in USD at this price
}

# Liquidity = sum of all bid sizes + sum of all ask sizes
total_liquidity = sum(float(b.get('size', 0)) for b in bids) + sum(float(a.get('size', 0)) for a in asks)
```

---

## 💰 Placing Orders — CLOB SDK

### **Authentication**

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds

host = "https://clob.polymarket.com"
chain_id = 137  # Polygon

client = ClobClient(host, key=key, chain_id=chain_id)
client.set_api_creds(ApiCreds(
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
    api_passphrase="YOUR_API_PASSPHRASE"
))
```

### **🔥 CRITICAL: Decimal Precision Rules**

| Amount Type | Max Decimals | Example |
|-------------|-------------|---------|
| **Maker amount (tokens)** | **4** | 10.7419 |
| **Taker amount (USD)** | **2** | 3.33 |
| **Price** | **4** | 0.3100 |

**Rule: Calculate tokens FIRST, then derive USD**

```python
# ✅ CORRECT: Explicit precision control
raw_tokens = amount_usd / price           # e.g. 3.33 / 0.31 = 10.74193548
tokens = round(raw_tokens, 4)             # 10.7419 (max 4 decimals)
usd_amount = round(tokens * price, 2)     # 3.33 (max 2 decimals)
price_rounded = round(price, 4)           # 0.3100 (max 4 decimals)

# ❌ WRONG: Let SDK auto-calculate → may produce > 4 decimal tokens
# ❌ WRONG: Market order with SDK auto-calculation → same issue
```

### **Limit Order (Recommended — More Control)**

```python
from py_clob_client.order_builder.constants import BUY

order_args = OrderArgs(
    token_id=asset_id,
    price=price_rounded,    # 0.3100 (max 4 decimals)
    size=tokens,            # 10.7419 (max 4 decimals)
    side=BUY,
    expiration=0,           # GTC (Good Till Cancelled)
)
# A limit order at market price = instant fill with full precision control
```

### **Market Order (From Official Docs)**

```python
market_order = client.create_market_order(
    token_id="TOKEN_ID",
    side=BUY,
    amount=100,      # Dollar amount! SDK calculates tokens
    price=0.50,      # Slippage protection (can be 0)
    order_type=OrderType.FOK
)
client.post_order(market_order, OrderType.FOK)
```

**Market Order Notes**:
- `amount` = USD amount (SDK calculates tokens internally)
- `price` = slippage protection ceiling, NOT exact execution price
- ⚠️ SDK may produce >4 decimal tokens → prefer limit orders for safety

### **⚠️ ALWAYS Read Official Docs Before Trading**

- https://docs.polymarket.com/trading/orders/create
- https://docs.polymarket.com/trading/orders/overview

**Never guess API behavior — read docs first.** Multiple failed versions were caused by not reading official documentation.

---

## ⏰ 5-Minute Market Mechanics

### **How Markets Work**

1. **New market every 5 minutes** — timestamp-based: `btc-updown-5m-{unix_ts}`
2. **Market duration**: Exactly 5 minutes (300 seconds)
3. **Winner determination**: Polymarket resolves based on BTC price movement during the 5-minute interval
   - UP wins → outcomePrices: UP=1.0, DOWN=0.0
   - DOWN wins → outcomePrices: UP=0.0, DOWN=1.0
4. **Market appears on Polymarket**: ~30-60 seconds before interval start
5. **Orderbook becomes active**: Shortly after market appears

### **Timing — What Happens When**

| Time | Event |
|------|-------|
| T-60s | Market appears on Gamma API |
| T-30s | Orderbook starts getting liquidity |
| T+0 | 5-minute interval starts |
| T+0 ~ T+30s | Ask prices around 0.50, active trading |
| T+240s | Most trading done, prices converge |
| T+300s | Market closes |
| T+300s ~ T+360s | Winner being resolved |
| T+360s+ | Gamma API `outcomePrices` shows 1.0/0.0 (resolved) |

### **⚠️ CRITICAL: Winner Resolution Timing**

```python
# ❌ WRONG: Fetch winner immediately after market close
# Gamma API returns trading prices (0.60/0.40), NOT resolved prices (1.0/0.0)
# Can take 60+ seconds to resolve

# ✅ CORRECT: Wait for outcomePrices to show 1.0/0.0
# After market close, poll Gamma API until resolved
# outcomePrices [1.00, 0.00] = UP winner confirmed
# outcomePrices [0.00, 1.00] = DOWN winner confirmed
```

---

## 📊 Data Reliability — What to Trust

### **Price Data Hierarchy**

| Data Source | Use For | Accuracy | Latency |
|-------------|---------|----------|---------|
| `book` (WS) | Orderbook, bid/ask | ⭐⭐⭐ | Real-time |
| `best_bid_ask` (WS) | Quick price check | ⭐⭐⭐ | Real-time |
| `outcomePrices` (Gamma) | Market probability | ⭐⭐ | 5-30s delayed |
| `outcomePrices` (Gamma, resolved) | Winner verification | ⭐⭐⭐ | 60s+ after close |
| `price_change` (WS) | Past trades only | ❌ | N/A |
| `best_bid_ask` ask price | Trading probability | ⚠️ | NOT true probability |

### **⚠️ `best_bid_ask` Ask Price ≠ Market Probability**

- Ask price = lowest sell order in orderbook
- This is **not** the market's consensus probability
- It reflects orderbook dynamics, not market sentiment
- All versions using ask price as probability showed ~50% accuracy

---

## 🔄 Market Rotation

### **Interval-Based Rotation (Correct Method)**

```python
def get_current_interval():
    """Get current 5-minute interval boundary"""
    current_time = int(time.time())
    return (current_time // 300) * 300

def should_rotate(current_interval, last_interval):
    """Check if we've entered a new interval"""
    return current_interval != last_interval

# ❌ WRONG: Time-based (rotates at wrong time)
# time_since_rotation = time.time() - last_rotation
# if time_since_rotation >= 300: rotate()  # Off by up to 15 seconds!

# ✅ CORRECT: Interval-based (rotates exactly when interval changes)
# if get_current_interval() != current_base_timestamp: rotate()
```

---

## ⚠️ Known Pitfalls & Lessons Learned

### **1. Never Use `price_change` as Orderbook Data**
- `price_change` = past trade records
- BUY in `price_change` = someone bought at this price IN THE PAST
- This is NOT the current best ask
- Using it causes impossible states (ask < bid)

### **2. Decimal Precision Will Break Your Orders**
- Maker amount (tokens): max 4 decimals
- Taker amount (USD): max 2 decimals
- Calculate tokens first, derive USD second
- Never trust SDK auto-calculation
- Use limit orders for full control

### **3. Read Official Docs Before Implementing**
- Multiple wasted versions from guessing API behavior
- Official docs: https://docs.polymarket.com/trading/orders/create

### **4. Winner Resolution Takes Time**
- Gamma API doesn't return 1.0/0.0 immediately after close
- Poll until outcomePrices resolves to 1.0/0.0
- Verify with Gamma API outcomePrices post-session

### **⚠️ Pitfall #5: Market Resolution Timing**
- Gamma API doesn't return 1.0/0.0 immediately after close
- Can take 60+ seconds for outcomePrices to resolve
- Poll until you see 1.0/0.0, don't assume immediate resolution

### **6. Market Appearance Timing is Variable**
- Markets don't always appear exactly 60s before start
- Sometimes 30s, sometimes 90s
- Fetch ask immediately when market appears — don't delay

### **7. Ask Price at Market Start ≈ 0.50**
- Fresh market ask is ~0.50 (fair odds)
- Ask drifts quickly (within seconds) based on BTC movement
- If you see ask = 0.99, market is already closed/ending

---

## 📚 API Reference

### **Gamma API Endpoints**

| Endpoint | Method | Description | Auth? |
|----------|--------|-------------|-------|
| `/markets` | GET | List/search markets | No |
| `/markets/{id}` | GET | Get market by ID | No |
| `/markets?slug={slug}` | GET | Get market by slug | No |
| `/markets/{id}/price` | GET | Current prices | No |

### **WebSocket Events**

| Event | Direction | Reliable? | Structure |
|-------|-----------|-----------|-----------|
| `book` | S→C | ✅ | `bids[]`, `asks[]` at **top level** |
| `best_bid_ask` | S→C | ✅ | `best_bid`, `best_ask` |
| `price_change` | S→C | ❌ | Past trades, not orderbook |
| `last_trade_price` | S→C | ❌ | Last trade, not orderbook |

### **Rate Limits**

| API | Limit | Best Practice |
|-----|-------|---------------|
| Gamma API | ~100 req/min | Use WebSocket instead of polling |
| Data API | ~50 req/min | Cache responses |
| WebSocket | No hard limit | PING every 10s, batch subscriptions |

---

## 🔧 CLOB SDK Quick Reference

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType, ApiCreds
from py_clob_client.order_builder.constants import BUY

# Initialize
client = ClobClient("https://clob.polymarket.com", key=key, chain_id=137)
client.set_api_creds(ApiCreds(api_key=..., api_secret=..., api_passphrase=...))

# Limit order (recommended)
order = OrderArgs(token_id=ASSET_ID, price=0.50, size=10.0, side=BUY, expiration=0)
# size = tokens (max 4 decimals), price (max 4 decimals)

# Market order
market_order = client.create_market_order(token_id=ASSET_ID, side=BUY, amount=100, price=0, order_type=OrderType.FOK)
# amount = USD, price = slippage ceiling

# Nonces: Must be unique per order. Use counter or UUID.
```

### **Official Documentation**
- Orders: https://docs.polymarket.com/trading/orders/create
- Overview: https://docs.polymarket.com/trading/orders/overview

---

## 📝 Version History

- **v2.0.0 (2026-03-23)**:
  - ✅ Added CLOB SDK trading section (limit/market orders, decimal precision)
  - ✅ Added 5-min market mechanics (timing, winner determination)
  - ✅ Added data reliability guide (what to trust, what not to)
  - ✅ Added known pitfalls section (7 critical lessons)
  - ✅ Added winner verification timing guide
  - ✅ Added winner verification timing guide
  - ✅ Added market rotation (interval-based vs time-based)
  - ✅ Updated WebSocket reliability table
  - ✅ Removed arbitrage scanner example (not applicable to 5-min markets)

- **v1.2.0 (2026-03-05)**:
  - ✅ Fixed WebSocket book event structure
  - ✅ Added real-time liquidity tracking
  - ✅ Added multi-cryptocurrency monitoring

- **v1.0.0 (2026-03-03)**:
  - Initial release
