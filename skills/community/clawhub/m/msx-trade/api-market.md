# Module: Market Data

**When to load this file:** User asks about token prices, market quotes, order book depth, or chart/candlestick data.

Trigger phrases: "quote", "price", "orderbook", "candle", "价格", "行情", "报价", "盘口", "K线", "走势"

---

## GET /market/tokens

Returns the full list of tradable security tokens on MSX.

**Request**
```
GET /market/tokens
X-API-KEY: {MSX_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| status | string | No | Filter by `active` / `suspended`. Default: `active` |

**Response**
```json
{
  "tokens": [
    {
      "symbol": "TOKEN-AAPL",
      "name": "Apple Inc. Token",
      "asset_type": "equity",
      "exchange": "MSX",
      "status": "active"
    }
  ]
}
```

---

## GET /market/tokens/{symbol}/quote

Returns the latest price quote for a specific token.

**Request**
```
GET /market/tokens/TOKEN-AAPL/quote
X-API-KEY: {MSX_API_KEY}
```

**Response**
```json
{
  "symbol": "TOKEN-AAPL",
  "last_price": 195.00,
  "bid": 194.95,
  "ask": 195.05,
  "change": 2.50,
  "change_pct": 1.30,
  "volume": 125000,
  "timestamp": "2025-03-25T10:30:00Z"
}
```

> Always display `timestamp` so the user knows how fresh the data is.

---

## GET /market/tokens/{symbol}/orderbook

Returns the current bid/ask order book for a token.

**Request**
```
GET /market/tokens/TOKEN-AAPL/orderbook
X-API-KEY: {MSX_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| depth | integer | No | Number of price levels per side. Default: `10` |

**Response**
```json
{
  "symbol": "TOKEN-AAPL",
  "bids": [
    { "price": 194.95, "quantity": 200 },
    { "price": 194.90, "quantity": 500 }
  ],
  "asks": [
    { "price": 195.05, "quantity": 150 },
    { "price": 195.10, "quantity": 300 }
  ],
  "timestamp": "2025-03-25T10:30:00Z"
}
```

---

## GET /market/tokens/{symbol}/candles

Returns OHLCV candlestick data for charting or trend analysis.

**Request**
```
GET /market/tokens/TOKEN-AAPL/candles
X-API-KEY: {MSX_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| interval | string | Yes | `1m`, `5m`, `15m`, `1h`, `1d` |
| limit | integer | No | Number of candles to return. Default: `100`, max: `500` |

**Response**
```json
{
  "symbol": "TOKEN-AAPL",
  "interval": "1d",
  "candles": [
    {
      "time": "2025-03-24T00:00:00Z",
      "open": 192.00,
      "high": 196.50,
      "low": 191.00,
      "close": 195.00,
      "volume": 980000
    }
  ]
}
```
