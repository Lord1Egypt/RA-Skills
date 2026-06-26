# Polymarket API Reference

Complete reference for Polymarket API endpoints, parameters, and responses.

**Author**: Calvin Lam  
**Last Updated**: 2026-03-23

---

## Table of Contents

1. [Gamma API](#gamma-api)
2. [CLOB API](#clob-api)
3. [CLOB Auth API](#clob-auth-api)
4. [Data API](#data-api)
5. [WebSocket](#websocket)
6. [Response Formats](#response-formats)
7. [Error Handling](#error-handling)
8. [Rate Limits](#rate-limits)

---

## Gamma API

**Base URL**: `https://gamma-api.polymarket.com`

Primary public API for market data. No authentication required.

### GET /markets

List/search markets.

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | int | 100 | Number of results |
| `offset` | int | 0 | Pagination offset |
| `active` | bool | - | Filter active status |
| `closed` | bool | - | Filter closed status |
| `slug` | string | - | Filter by URL slug |
| `_s` | string | - | Search term |
| `tag` | string | - | Filter by tag |
| `order` | string | - | Sort order |

**Response**: Array of market objects (see Response Formats)

### GET /markets/{id}

Get specific market by ID.

**Response**: Single market object

### GET /markets/{id}/price

Get current prices.

**Response**:
```json
{
  "market": "abc123",
  "outcomes": ["Yes", "No"],
  "outcomePrices": ["0.67", "0.33"],
  "volume": "1234567.89",
  "timestamp": "2024-03-15T12:34:56Z"
}
```

### ⚠️ outcomePrices Timing

| Timing | outcomePrices Values | Meaning |
|--------|---------------------|---------|
| During trading | [0.60, 0.40] | Current market prices (midpoint probability) |
| After close, resolving | [0.60, 0.40] | Still showing trading prices, NOT resolved |
| After resolved | [1.00, 0.00] | Winner = 1.0, Loser = 0.0 |
| 60+ seconds after close | [1.00, 0.00] | Usually resolved by now |

**Poll outcomePrices until it resolves to 1.0/0.0. Resolution takes 60+ seconds after close.**

---

## CLOB API

**Base URL**: `https://clob.polymarket.com`

Central Limit Order Book API. No auth required for public endpoints.

### GET /book

Get orderbook for a token.

**Parameters**: `token_id` (asset ID)

**Response**:
```json
{
  "market": "token_id_here",
  "asset_id": "token_id_here",
  "bids": [
    {"price": "0.45", "size": "1000"}
  ],
  "asks": [
    {"price": "0.47", "size": "800"}
  ],
  "hash": "abc123",
  "current_highest_bid": "0.45",
  "current_lowest_ask": "0.47",
  "base_fee": "0"
}
```

### GET /midpoint

Get current midpoint price.

### POST /order

Place an order (requires auth headers).

### GET /markets

List all CLOB markets.

---

## CLOB Auth API

**Base URL**: `https://clob-auth.polymarket.com`

### POST /derive-api-keys

Derive API credentials from your wallet.

**Required**: API key, API secret, API passphrase (from Polymarket account settings)

### Auth Flow

```python
# 1. Derive API keys from your private key
creds = client.derive_api_key()
# Returns: api_key, api_secret, api_passphrase

# 2. Set credentials on client
client.set_api_creds(ApiCreds(
    api_key=creds.api_key,
    api_secret=creds.api_secret,
    api_passphrase=creds.api_passphrase
))

# 3. Now you can place orders
```

---

## Data API

**Base URL**: `https://data-api.polymarket.com`

### GET /orderbook/{id}

Order book by market ID.

### GET /trades/{id}

Trade history. Supports pagination with `limit` and `before` parameters.

---

## WebSocket

**Endpoint**: `wss://ws-subscriptions-clob.polymarket.com/ws/market`

### Subscribe

```json
{
  "assets_ids": ["asset_id_1", "asset_id_2"],
  "type": "market",
  "custom_feature_enabled": true
}
```

### Unsubscribe

```json
{
  "assets_ids": ["asset_id_1"],
  "type": "unsubscribe"
}
```

### Heartbeat

Send `"PING"` every 10 seconds. Server responds with `"PONG"`.

### Event Types — Reliability Matrix

| Event | Data | Reliable for | ⚠️ Notes |
|-------|------|-------------|----------|
| `book` | `bids[]`, `asks[]` at **top level** | Orderbook state | Full snapshot, use for bid/ask |
| `best_bid_ask` | `best_bid`, `best_ask` | Quick price check | No sizes included |
| `price_change` | `price`, `side`, `size` | ❌ NOT orderbook | Past trade records only |
| `last_trade_price` | `price` | ❌ NOT orderbook | Last executed trade |

### ⚠️ price_change Misconception

```
price_change with side="BUY" → someone BOUGHT at this price in the past
price_change with side="SELL" → someone SOLD at this price in the past

These are HISTORICAL trade records, NOT current bid/ask prices.
Using them as orderbook data causes impossible states (ask < bid).
```

---

## Response Formats

### Market Object (Gamma API)

```json
{
  "id": "string",
  "slug": "string",
  "question": "string",
  "description": "string",
  "outcomes": ["Yes", "No"] | "[\"Yes\",\"No\"]",
  "outcomePrices": ["0.67", "0.33"],
  "volume": "1234567.89",
  "active": true,
  "closed": false,
  "expirationDate": "2024-12-31T23:59:59Z",
  "createdAt": "2024-01-01T00:00:00Z",
  "clobTokenIds": "[\"token1\",\"token2\"]",
  "tokens": [{"token_id": "...", "outcome": "Yes"}]
}
```

**⚠️ Tricky Fields**:
- `clobTokenIds`: JSON **string** (not array) — must `json.loads()`
- `outcomes`: Can be array OR JSON string — check type before use
- All prices returned as **strings** — parse with `float()`

### WebSocket Book Event

```json
{
  "event_type": "book",
  "asset_id": "token_id_here",
  "bids": [
    {"price": "0.45", "size": "1000"}
  ],
  "asks": [
    {"price": "0.47", "size": "800"}
  ]
}
```

**⚠️ `bids` and `asks` are at TOP LEVEL, not under `data['book']`**

### WebSocket best_bid_ask Event

```json
{
  "event_type": "best_bid_ask",
  "asset_id": "token_id_here",
  "best_bid": "0.45",
  "best_ask": "0.47"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 400 | Bad Request | Check parameters, decimal precision |
| 404 | Not Found | Verify market/asset ID |
| 429 | Rate Limited | Implement backoff |
| 500 | Server Error | Retry with backoff |

### Common Error: Invalid Amounts

```
"invalid amounts, the buy orders maker amount supports a max accuracy of 4 decimals,
taker amount a max of 2 decimals"
```

**Fix**: Round tokens to 4 decimals, USD to 2 decimals BEFORE submitting.

```python
tokens = round(amount_usd / price, 4)
usd = round(tokens * price, 2)
price = round(price, 4)
```

---

## Rate Limits

| API | Limit | Best Practice |
|-----|-------|---------------|
| Gamma API | ~100 req/min | Use WebSocket for real-time |
| CLOB API | ~50 req/min | Batch requests |
| Data API | ~50 req/min | Cache responses |
| WebSocket | No hard limit | PING every 10s, batch subs |

---

## Best Practices

1. ✅ **WebSocket > Polling** for real-time data
2. ✅ **`clobTokenIds` > `tokens`** for asset IDs
3. ✅ **Only `book` + `best_bid_ask`** from WebSocket events
4. ✅ **Round decimals explicitly** before order submission
5. ✅ **Poll outcomePrices** until resolved (1.0/0.0)
6. ✅ **Verify with Gamma API** outcomePrices post-session
7. ✅ **Interval-based rotation** (not time-based)
8. ✅ **PING every 10s** to keep WebSocket alive
9. ✅ **Handle disconnections** with auto-reconnect

---

**Need WebSocket details?** See `WEBSOCKET_GUIDE.md`
**Need trading details?** See main `SKILL.md`
