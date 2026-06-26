# Polymarket API & Data Access Guide

🎯 **Learn how to connect to and use Polymarket APIs for prediction market data**

---

## ✨ What This Skill Covers

This skill teaches you **HOW** to:

- ✅ **Connect to Polymarket** - API endpoints and authentication
- ✅ **Find Markets** - Search, filter, and browse prediction markets
- ✅ **Get Real-time Data** - WebSocket and Socket.IO connections
- ✅ **Use Polling Methods** - Fallback when real-time isn't available
- ✅ **Access Order Books** - Market depth and liquidity data

**This is a general API reference** - use this knowledge to build your own applications!

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ~/.openclaw/workspace/skills/polymarket-api
pip install -r requirements.txt
```

### 2. Basic API Call

```python
import requests

# Get all active markets
response = requests.get("https://gamma-api.polymarket.com/markets")
markets = response.json()

# Search for specific markets
response = requests.get(
    "https://gamma-api.polymarket.com/markets",
    params={"_s": "bitcoin"}
)
bitcoin_markets = response.json()
```

### 3. Get Real-time Data

```python
import websocket
import json

def on_message(ws, message):
    print(f"Received: {json.loads(message)}")

def on_open(ws):
    ws.send(json.dumps({
        "type": "subscribe",
        "market": "your_market_id"
    }))

ws = websocket.WebSocketApp(
    "wss://ws-subscriptions.polymarket.com",
    on_message=on_message,
    on_open=on_open
)
ws.run_forever()
```

---

## 📁 File Structure

```
polymarket-api/
├── SKILL.md                    # Complete API documentation
├── README.md                   # This file
├── skill.json                  # Skill configuration
├── requirements.txt            # Python dependencies
├── examples/
│   ├── connect.py              # Basic API connection examples
│   ├── find_markets.py         # Market search and filtering
│   ├── realtime_data.py        # WebSocket and Socket.IO examples
│   ├── polling.py              # Polling methods and fallbacks
│   └── orderbook.py            # Order book access and analysis
└── references/
    ├── API_REFERENCE.md        # Detailed API endpoint reference
    └── WEBSOCKET_GUIDE.md      # WebSocket implementation guide
```

---

## 🔌 API Overview

### Gamma API (Public)

**Base URL**: `https://gamma-api.polymarket.com`

| Endpoint | Description | Auth Required |
|----------|-------------|---------------|
| `GET /markets` | List all markets | No |
| `GET /markets/{id}` | Get market by ID | No |
| `GET /markets/{id}/price` | Get current prices | No |
| `GET /markets?_s={term}` | Search markets | No |

### Data API

**Base URL**: `https://data-api.polymarket.com`

| Endpoint | Description | Auth Required |
|----------|-------------|---------------|
| `GET /orderbook/{id}` | Get order book | No |
| `GET /trades/{id}` | Get trade history | No |

### WebSocket

**Endpoint**: `wss://ws-subscriptions.polymarket.com`

Real-time updates for prices, order books, and trades.

---

## 📚 Examples

### Finding Markets

```python
# See examples/find_markets.py for full implementation

# Search by keyword
bitcoin_markets = search_markets("bitcoin")

# Filter by volume
high_volume = filter_high_volume_markets(min_volume=500000)

# Find closing soon
closing = find_closing_soon_markets(hours=48)
```

### Real-time Data

```python
# See examples/realtime_data.py for full implementation

# Native WebSocket (recommended)
websocket_example()

# Socket.IO (fallback)
socketio_example()

# With reconnection logic
client = RobustWebSocket(url, market_ids)
client.connect()
```

### Polling

```python
# See examples/polling.py for full implementation

# Basic polling
for data in poll_market_prices(market_id, interval=5):
    print(f"Prices: {data['prices']}")

# With change detection
poller = SmartPoller(market_id)
for data in poller.poll():
    if data['change_detected']:
        print(f"New prices: {data['prices']}")
```

### Order Book

```python
# See examples/orderbook.py for full implementation

# Get order book
orderbook = get_orderbook(market_id)

# Analyze
analysis = analyze_orderbook(orderbook)
print(f"Spread: {analysis['spread']}")
print(f"Bid volume: {analysis['total_bid_volume']}")

# Check liquidity
liquidity = check_liquidity(market_id, min_volume=10000)
print(f"Sufficient: {liquidity['sufficient']}")
```

---

## 📖 Documentation

### Primary Documentation

- **SKILL.md** - Complete API guide with all methods and examples
- **references/API_REFERENCE.md** - Detailed endpoint documentation
- **references/WEBSOCKET_GUIDE.md** - WebSocket implementation details

### Code Examples

All examples in the `examples/` directory are:
- ✅ Well-documented with comments
- ✅ Ready to run (with your market IDs)
- ✅ Educational and generic

---

## ⚙️ Configuration

### Optional Environment Variables

```bash
# Only needed for authenticated endpoints (advanced usage)
POLYMARKET_API_KEY=your_key_here
POLYMARKET_API_SECRET=your_secret_here
```

**Note**: Most public endpoints don't require authentication!

---

## ⚠️ Important Notes

### Rate Limits

- **Gamma API**: ~100 requests/minute
- **Data API**: ~50 requests/minute
- **WebSocket**: No hard limit (be reasonable)

### Best Practices

1. ✅ Use WebSocket for real-time data (preferred)
2. ✅ Implement exponential backoff on errors
3. ✅ Cache responses when possible
4. ✅ Use polling intervals >= 5 seconds
5. ✅ Handle disconnections gracefully

---

## 🎓 Learning Path

### Beginner

1. Read `SKILL.md` for overview
2. Run `examples/connect.py` to test connection
3. Try `examples/find_markets.py` to explore markets
4. Study the API structure

### Intermediate

1. Implement real-time data with `examples/realtime_data.py`
2. Learn polling methods from `examples/polling.py`
3. Analyze order books with `examples/orderbook.py`
4. Read `references/API_REFERENCE.md`

### Advanced

1. Build custom applications using these APIs
2. Implement robust error handling
3. Create monitoring dashboards
4. Combine multiple data sources

---

## 🔗 Resources

- **Polymarket Website**: https://polymarket.com
- **API Documentation**: https://docs.polymarket.com
- **Community**: OpenClaw Discord

---

## 💡 Use Cases

This skill is useful for:

- **Data Analysis** - Collect and analyze prediction market data
- **Monitoring** - Track market prices and changes
- **Research** - Study market behavior and trends
- **Building Tools** - Create dashboards, alerts, and applications
- **Learning** - Understand how prediction markets work

---

## 📊 Stats

- **API Endpoints**: 10+ documented
- **Examples**: 5 complete examples
- **Languages**: Python
- **Difficulty**: Beginner to Advanced

---

**Version**: 1.0.0
**Status**: ✅ General API Guide
**Last Updated**: 2026-03-03
**Author**: Calvin Lam

---

**Start exploring Polymarket data today!** 🚀
