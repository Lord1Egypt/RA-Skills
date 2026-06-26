---
name: luzia
homepage: https://luzia.dev
user-invocable: true
description: >
  Use this skill whenever the user wants to fetch cryptocurrency prices, stream
  real-time market data, list exchanges or markets, or retrieve historical OHLCV
  candlestick data using the Luzia API (luzia.dev). Triggers include: any mention
  of "Luzia", "crypto price", "BTC/USDT", "exchange ticker", "OHLCV", "real-time
  price stream", or requests to connect to wss://api.luzia.dev. Also use when the
  user wants to build trading bots, portfolio trackers, or price alert tools on
  top of the Luzia platform. Do NOT use for non-Luzia crypto APIs (e.g. CoinGecko,
  Binance direct) unless the user explicitly wants Luzia as the data source.
---

# Luzia API Integration Skill

## Overview

Luzia (luzia.dev) provides **real-time cryptocurrency pricing** from multiple
exchanges through a unified REST and WebSocket API.

- **Base REST URL:** `https://api.luzia.dev`
- **WebSocket URL:** `wss://api.luzia.dev/v1/ws`
- **Swagger UI:** `https://api.luzia.dev/docs`
- **Docs:** `https://luzia.dev/docs`

---

## Core Principles

1. **Always authenticate** — every endpoint requires `Authorization: Bearer lz_<key>`.
2. **Choose REST vs WebSocket correctly** — REST for on-demand lookups; WebSocket for
   streaming updates (Pro plan required).
3. **Respect rate limits** — Free: 100 req/min, 5 000 req/day. Pro: 1 000 req/min, unlimited/day.
4. **Use the right symbol format** — REST paths use `BTC-USDT` (hyphen); channel
   subscriptions and response payloads use `BTC/USDT` (slash).
5. **Handle errors explicitly** — inspect HTTP status codes for REST; handle `error`
   message type for WebSocket.

---

## Authentication

All requests require an API key in the `Authorization` header:

```
Authorization: Bearer lz_your_api_key
```

API keys follow the format `lz_` + 32 random characters.
Get one at: https://luzia.dev/signup

---

## Tier Summary

| Feature              | Free          | Pro ($29.99/mo)     | Enterprise      |
|----------------------|---------------|---------------------|-----------------|
| REST requests/min    | 100           | 1 000               | Custom          |
| REST requests/day    | 5 000         | Unlimited           | Unlimited       |
| WebSocket access     | ❌            | ✅ (5 conns, 50 sub) | ✅ (25, 500 sub) |
| History lookback     | 30 days       | 90 days             | Unlimited       |

---

## REST API Reference

### 1. List Exchanges

```
GET /v1/exchanges
```

Returns all supported exchanges with their status.

**Example response:**
```json
{
  "exchanges": [
    { "id": "binance", "name": "Binance", "status": "active" },
    { "id": "coinbase", "name": "Coinbase", "status": "active" }
  ]
}
```

---

### 2. List Markets for an Exchange

```
GET /v1/markets/:exchange
```

Returns all trading pairs available on the given exchange.

**Path params:** `exchange` — e.g. `binance`, `coinbase`, `kraken`

**Example response:**
```json
{
  "exchange": "binance",
  "markets": [
    { "symbol": "BTC-USDT", "base": "BTC", "quote": "USDT" }
  ]
}
```

---

### 3. Get Ticker (single pair)

```
GET /v1/ticker/:exchange/:symbol
```

Fetches the latest price for one trading pair.

**Path params:**
- `exchange` — e.g. `binance`
- `symbol` — hyphen-separated, e.g. `BTC-USDT`

**Query params:**
- `maxAge` (optional, ms) — max acceptable data age. Default: `120000` (2 min).

**Example response:**
```json
{
  "symbol": "BTC/USDT",
  "exchange": "binance",
  "last": 67432.50,
  "bid": 67430.00,
  "ask": 67435.00,
  "high": 68500.00,
  "low": 66800.00,
  "open": 67000.00,
  "close": 67432.50,
  "volume": 12345.678,
  "quoteVolume": 832456789.50,
  "change": 432.50,
  "changePercent": 0.65,
  "timestamp": "2024-01-20T12:00:00.000Z"
}
```

---

### 4. Get All Tickers for an Exchange

```
GET /v1/tickers/:exchange
```

Fetches prices for all pairs on an exchange. Supports pagination.

**Query params:**
- `maxAge` (optional, ms) — Default: `120000`
- `limit` (optional) — Default: `20`, max: `50`
- `offset` (optional) — Default: `0`

**Example response:**
```json
{
  "tickers": [ { /* same shape as single ticker */ } ],
  "total": 150,
  "limit": 20,
  "offset": 0
}
```

---

### 5. Historical OHLCV Data

```
GET /v1/history/:exchange/:symbol
```

Returns candlestick data for a trading pair.

**Path params:** `exchange`, `symbol` (hyphen format, e.g. `BTC-USDT`)

**Query params:**
- `interval` — `1m` | `5m` | `15m` | `1h` | `1d`
- `limit` — default `300`, max `500`
- `start` — Unix ms timestamp (default: 24h ago)
- `end` — Unix ms timestamp (default: now)

**Example response:**
```json
{
  "exchange": "binance",
  "symbol": "BTC-USDT",
  "interval": "1h",
  "candles": [
    {
      "open": 67000.00,
      "high": 67450.00,
      "low": 66950.00,
      "close": 67432.50,
      "volume": 1234.56,
      "timestamp": "2024-01-20T12:00:00.000Z"
    }
  ],
  "count": 24,
  "start": "2024-01-20T00:00:00.000Z",
  "end": "2024-01-21T00:00:00.000Z"
}
```

---

## REST: Code Patterns

### TypeScript / fetch

```typescript
const API_KEY = "lz_your_api_key";
const BASE = "https://api.luzia.dev";

async function getTicker(exchange: string, symbol: string) {
  const res = await fetch(`${BASE}/v1/ticker/${exchange}/${symbol}`, {
    headers: { Authorization: `Bearer ${API_KEY}` },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res.json();
}

async function getHistory(exchange: string, symbol: string, interval = "1h", limit = 24) {
  const url = new URL(`${BASE}/v1/history/${exchange}/${symbol}`);
  url.searchParams.set("interval", interval);
  url.searchParams.set("limit", String(limit));
  const res = await fetch(url.toString(), {
    headers: { Authorization: `Bearer ${API_KEY}` },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res.json();
}
```

### Python / httpx

```python
import httpx

API_KEY = "lz_your_api_key"
BASE = "https://api.luzia.dev"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def get_ticker(exchange: str, symbol: str) -> dict:
    r = httpx.get(f"{BASE}/v1/ticker/{exchange}/{symbol}", headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_history(exchange: str, symbol: str, interval: str = "1h", limit: int = 24) -> dict:
    r = httpx.get(
        f"{BASE}/v1/history/{exchange}/{symbol}",
        headers=HEADERS,
        params={"interval": interval, "limit": limit}
    )
    r.raise_for_status()
    return r.json()
```

---

## WebSocket API Reference

> **Requires Pro plan or above.**

### Connection

```
wss://api.luzia.dev/v1/ws
Header: Authorization: Bearer lz_your_api_key
```

### Channel Format

| Channel                      | Description                          |
|------------------------------|--------------------------------------|
| `ticker:binance:BTC/USDT`   | Single pair from one exchange        |
| `ticker:coinbase:ETH/USDT`  | Single pair from another exchange    |
| `ticker:binance`             | All tickers from Binance (1 sub slot)|

> ⚠️ **Symbol format in channels is slash** (`BTC/USDT`), not hyphen.

### Client → Server Messages

```json
// Subscribe
{ "type": "subscribe", "channels": ["ticker:binance:BTC/USDT"] }

// Unsubscribe
{ "type": "unsubscribe", "channels": ["ticker:binance:BTC/USDT"] }

// Heartbeat (send every 30s)
{ "type": "ping" }
```

### Server → Client Messages

```json
// After connect
{ "type": "connected", "tier": "pro", "limits": { "maxSubscriptions": 50 } }

// Subscription confirmed
{ "type": "subscribed", "channel": "ticker:binance:BTC/USDT" }

// Heartbeat response
{ "type": "pong", "timestamp": "2024-01-23T10:13:20.000Z" }

// Price update
{
  "type": "ticker",
  "exchange": "binance",
  "symbol": "BTC/USDT",
  "data": { /* same fields as REST ticker response */ },
  "timestamp": "2024-01-23T10:13:20.050Z"
}

// Error
{ "type": "error", "code": "SUBSCRIPTION_LIMIT", "message": "..." }
```

### WebSocket Error Codes

| Code                  | Meaning                                        |
|-----------------------|------------------------------------------------|
| `CONNECTION_REJECTED` | Wrong tier or connection limit exceeded        |
| `SUBSCRIPTION_LIMIT`  | Max subscriptions reached for your tier        |
| `INVALID_CHANNEL`     | Bad channel format                             |
| `INVALID_JSON`        | Message is not valid JSON                      |
| `INVALID_REQUEST`     | Missing required fields                        |
| `UNKNOWN_TYPE`        | Unrecognized message type                      |
| `SERVER_SHUTDOWN`     | Server shutting down — reconnect shortly       |

---

## WebSocket: Code Patterns

### Node.js / Native WebSocket (no SDK)

```typescript
import WebSocket from "ws"; // npm install ws

const API_KEY = "lz_your_api_key";

function createLuziaStream(channels: string[]) {
  const ws = new WebSocket("wss://api.luzia.dev/v1/ws", {
    headers: { Authorization: `Bearer ${API_KEY}` },
  });

  // Heartbeat every 30s
  const heartbeat = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: "ping" }));
    }
  }, 30_000);

  ws.on("open", () => console.log("WebSocket open"));

  ws.on("message", (raw: string) => {
    const msg = JSON.parse(raw);
    switch (msg.type) {
      case "connected":
        console.log("Connected — tier:", msg.tier);
        ws.send(JSON.stringify({ type: "subscribe", channels }));
        break;
      case "subscribed":
        console.log("Subscribed to:", msg.channel);
        break;
      case "ticker":
        console.log(`[${msg.exchange}] ${msg.symbol}: $${msg.data.last}`);
        break;
      case "pong":
        // heartbeat acknowledged
        break;
      case "error":
        console.error(`WS error [${msg.code}]:`, msg.message);
        break;
    }
  });

  ws.on("close", (code, reason) => {
    clearInterval(heartbeat);
    console.log(`Disconnected: ${code} ${reason}`);
    // implement exponential backoff reconnect here
  });

  ws.on("error", (err) => console.error("WS error:", err));

  return ws;
}

// Usage
createLuziaStream(["ticker:binance:BTC/USDT", "ticker:coinbase:ETH/USDT"]);
```

### Python / websockets

```python
import asyncio, json, websockets

API_KEY = "lz_your_api_key"
WS_URL = "wss://api.luzia.dev/v1/ws"

async def stream_prices(channels: list[str]):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    async with websockets.connect(WS_URL, additional_headers=headers) as ws:
        async def heartbeat():
            while True:
                await asyncio.sleep(30)
                await ws.send(json.dumps({"type": "ping"}))

        asyncio.create_task(heartbeat())

        async for raw in ws:
            msg = json.loads(raw)
            match msg["type"]:
                case "connected":
                    print(f"Connected — tier: {msg['tier']}")
                    await ws.send(json.dumps({"type": "subscribe", "channels": channels}))
                case "ticker":
                    d = msg["data"]
                    print(f"[{msg['exchange']}] {msg['symbol']}: ${d['last']}")
                case "error":
                    print(f"Error [{msg['code']}]: {msg['message']}")

asyncio.run(stream_prices(["ticker:binance:BTC/USDT"]))
```

### Reconnection with Exponential Backoff (TypeScript)

```typescript
async function connectWithRetry(channels: string[], maxAttempts = 10) {
  let attempt = 0;
  const delay = (ms: number) => new Promise(r => setTimeout(r, ms));

  while (attempt < maxAttempts) {
    try {
      await createLuziaStream(channels); // resolves on close
    } catch (err) {
      attempt++;
      const backoff = Math.min(1000 * 2 ** attempt + Math.random() * 500, 30_000);
      console.log(`Reconnecting in ${Math.round(backoff)}ms (attempt ${attempt})`);
      await delay(backoff);
    }
  }
  throw new Error("Max reconnect attempts reached");
}
```

---

## SDK Quick Reference (Official)

Both SDKs wrap REST and WebSocket with TypeScript types and auto-reconnect:

### TypeScript SDK

```bash
npm install @luziadev/sdk
```
```typescript
import { Luzia } from "@luziadev/sdk";
const luzia = new Luzia({ apiKey: "lz_your_api_key" });

// REST
const ticker = await luzia.getTicker("binance", "BTC-USDT");

// WebSocket
const ws = luzia.createWebSocket({ autoReconnect: true });
ws.on("connected", () => ws.subscribe(["ticker:binance:BTC/USDT"]));
ws.on("ticker", (data) => console.log(data));
ws.connect();
```

### Python SDK

Docs: https://luzia.dev/docs/python-sdk

---

## Decision Tree: REST vs WebSocket

```
Need data?
│
├─ One-off / on-demand lookup?
│   └─ Use REST → GET /v1/ticker/:exchange/:symbol
│
├─ All pairs on an exchange?
│   └─ Use REST → GET /v1/tickers/:exchange  (paginate with limit/offset)
│
├─ Historical chart / backtesting?
│   └─ Use REST → GET /v1/history/:exchange/:symbol  (choose interval)
│
└─ Continuous stream / sub-second updates?
    ├─ Free tier? → Poll REST every N seconds (respect rate limits)
    └─ Pro tier?  → WebSocket → subscribe to specific channels
```

---

## Common Mistakes to Avoid

| Mistake                                  | Fix                                              |
|------------------------------------------|--------------------------------------------------|
| Using `BTC/USDT` in REST URL path        | Use `BTC-USDT` (hyphen) in path params           |
| Using `BTC-USDT` in WS channel name      | Use `BTC/USDT` (slash) in channel strings        |
| Sending WS messages before `connected`   | Wait for `{ type: "connected" }` before subscribing |
| No heartbeat on native WS                | Send `{ type: "ping" }` every 30 seconds         |
| Subscribing to exchange-level channel unnecessarily | Use symbol-level channels to save sub slots |
| Forgetting `maxAge` for latency-sensitive apps | Set `maxAge=5000` (5s) for fresher REST data |
| Not handling `SERVER_SHUTDOWN` error     | Reconnect with backoff when you receive this code|

---

## Useful Links

| Resource          | URL                                      |
|-------------------|------------------------------------------|
| Docs home         | https://luzia.dev/docs                   |
| Swagger UI        | https://api.luzia.dev/docs               |
| WebSocket docs    | https://luzia.dev/docs/websocket         |
| TypeScript SDK    | https://luzia.dev/docs/sdk               |
| Python SDK        | https://luzia.dev/docs/python-sdk        |
| MCP Server        | https://luzia.dev/docs/mcp-server        |
| Get API key       | https://luzia.dev/signup                 |
| Manage API keys   | https://luzia.dev/keys                   |