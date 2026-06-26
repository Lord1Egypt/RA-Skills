# Polymarket API Reference

Complete documentation of the Gamma and CLOB APIs used by Polymarket Command Center.

## Overview

Polymarket provides two public APIs for market data:

1. **Gamma API** — Market metadata, outcomes, pricing history
2. **CLOB API** — Live order book, bid/ask spreads, midpoints

Both are unauthenticated, rate-limited generously for read-only access, and require no API key.

---

## Gamma API

Base URL: `https://gamma-api.polymarket.com`

The Gamma API provides comprehensive market data for browsing, searching, and analysis.

### Endpoints

#### GET /markets
List active/closed markets with optional filtering.

**Parameters:**
| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `active` | bool | true | Filter by active status |
| `closed` | bool | false | Include closed markets |
| `tag` | string | | Filter by category (politics, crypto, sports, etc.) |
| `limit` | int | 100 | Results per page (max 1000) |
| `offset` | int | 0 | Pagination offset |
| `order` | string | | Sort order: `volume`, `liquidityNum`, `createdAt` |
| `ascending` | bool | false | Sort ascending/descending |
| `slug` | string | | Exact slug search |

**Response (array of market objects):**
```json
[
  {
    "id": "0x...",
    "slug": "will-trump-win-2024",
    "question": "Will Trump win the 2024 US Presidential Election?",
    "description": "This market will resolve YES if...",
    "outcomes": "[\"Yes\", \"No\"]",
    "outcomePrices": "[0.68, 0.32]",
    "volumeNum": 18500000.0,
    "volume": "18500000.0",
    "liquidityNum": 4200000.0,
    "liquidity": "4200000.0",
    "active": true,
    "closed": false,
    "endDate": "2024-11-05T23:59:59Z",
    "createdAt": "2023-11-01T00:00:00Z",
    "clobTokenIds": "[\"0x...\", \"0x...\"]",
    "resolutionSource": "Associated Press"
  }
]
```

**Example requests:**
```bash
# Top 10 crypto markets by volume
curl "https://gamma-api.polymarket.com/markets?tag=crypto&limit=10&order=volume&ascending=false"

# Search by slug
curl "https://gamma-api.polymarket.com/markets?slug=bitcoin-above-100k&limit=1"

# All active politics markets
curl "https://gamma-api.polymarket.com/markets?tag=politics&active=true&closed=false"
```

#### GET /markets/{id}
Get a single market by ID.

**Parameters:** None (path parameter only)

**Response:**
```json
{
  "id": "0x...",
  "slug": "will-trump-win-2024",
  "question": "Will Trump win the 2024 US Presidential Election?",
  "outcomes": "[\"Yes\", \"No\"]",
  "outcomePrices": "[0.68, 0.32]",
  "volumeNum": 18500000.0,
  "liquidityNum": 4200000.0,
  "active": true,
  "endDate": "2024-11-05T23:59:59Z",
  "clobTokenIds": "[\"0x...\", \"0x...\"]"
}
```

**Example:**
```bash
curl "https://gamma-api.polymarket.com/markets/will-trump-win-2024"
```

---

### Response Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique market identifier (contract address) |
| `slug` | string | URL-friendly identifier |
| `question` | string | Market prediction question |
| `description` | string | Full market description and rules |
| `outcomes` | string | JSON-stringified array of outcome labels |
| `outcomePrices` | string | JSON-stringified array of outcome probabilities (0.0-1.0) |
| `volumeNum` | number | 24h trading volume in USD (numeric) |
| `volume` | string | 24h trading volume in USD (string) |
| `liquidityNum` | number | Available liquidity in USD (numeric) |
| `liquidity` | string | Available liquidity in USD (string) |
| `active` | bool | Market is currently accepting trades |
| `closed` | bool | Market has resolved |
| `endDate` | string | ISO 8601 UTC timestamp of market close |
| `createdAt` | string | Market creation timestamp |
| `clobTokenIds` | string | JSON-stringified array of CLOB token IDs |
| `resolutionSource` | string | Authority for market resolution |

### Error Responses

| Status | Response | Meaning |
|--------|----------|---------|
| 200 | Market(s) data | Success |
| 404 | Not found | Invalid market ID |
| 400 | Invalid parameter | Malformed query |
| 500 | Server error | Gamma API down |
| 429 | Rate limited | Too many requests |

---

## CLOB API

Base URL: `https://clob.polymarket.com`

The CLOB (Central Limit Order Book) API provides real-time order book data and pricing.

### Endpoints

#### GET /midpoint
Get the live bid/ask midpoint for a specific token.

**Parameters:**
| Parameter | Type | Required | Notes |
|-----------|------|----------|-------|
| `token_id` | string | Yes | CLOB token ID from Gamma API |

**Response:**
```json
{
  "mid": "0.678",
  "bid": "0.676",
  "ask": "0.680",
  "last": "0.679",
  "ts": 1646000000000
}
```

**Example request:**
```bash
curl "https://clob.polymarket.com/midpoint?token_id=0x..."
```

#### GET /orderbook
Get the full order book for a token.

**Parameters:**
| Parameter | Type | Required | Notes |
|-----------|------|----------|-------|
| `token_id` | string | Yes | CLOB token ID |

**Response:**
```json
{
  "bids": [
    {"price": "0.676", "size": "5000"},
    {"price": "0.675", "size": "10000"}
  ],
  "asks": [
    {"price": "0.680", "size": "3000"},
    {"price": "0.681", "size": "7500"}
  ],
  "mid": "0.678",
  "ts": 1646000000000
}
```

**Example request:**
```bash
curl "https://clob.polymarket.com/orderbook?token_id=0x..."
```

#### GET /markets
List all CLOB-enabled markets (often called "order books").

**Parameters:**
| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `limit` | int | 100 | Results per page |
| `offset` | int | 0 | Pagination offset |

**Response:**
```json
{
  "markets": [
    {
      "id": "0x...",
      "slug": "will-trump-win-2024",
      "tokens": ["0x...", "0x..."],
      "mid": "0.678"
    }
  ]
}
```

### Error Responses

| Status | Response | Meaning |
|--------|----------|---------|
| 200 | Order book data | Success |
| 400 | Invalid token_id | Token not found or invalid |
| 500 | Server error | CLOB API down |
| 429 | Rate limited | Too many requests |

---

## Data Format Details

### Outcome Prices
Prices are always decimal probabilities between 0.0 and 1.0:
- `0.68` = 68% probability
- `0.50` = 50% (even odds)
- `0.25` = 25% probability

When displaying, multiply by 100 to show as percentage: `0.68 * 100 = 68%`

### Outcomes (Binary Markets)
For binary markets (yes/no):
```json
{
  "outcomes": "[\"Yes\", \"No\"]",
  "outcomePrices": "[0.68, 0.32]"
}
```

Meaning:
- Outcome 0: "Yes" at 68% probability
- Outcome 1: "No" at 32% probability

### Outcomes (Categorical Markets)
For categorical markets (3+ outcomes):
```json
{
  "outcomes": "[\"Trump\", \"Harris\", \"RFK Jr\"]",
  "outcomePrices": "[0.45, 0.35, 0.20]"
}
```

Meaning:
- Trump: 45%
- Harris: 35%
- RFK Jr: 20%

### Timestamps
All timestamps are ISO 8601 UTC format with optional `Z` suffix:
- `2024-11-05T23:59:59Z` (with Z)
- `2024-11-05T23:59:59+00:00` (with offset)

Convert to Python `datetime`:
```python
from datetime import datetime
ts_str = "2024-11-05T23:59:59Z"
clean = ts_str.replace("Z", "+00:00")
dt = datetime.fromisoformat(clean)
```

### CLOB Token IDs
Markets have 1+ CLOB token IDs (one per outcome):
```json
{
  "outcomes": "[\"Yes\", \"No\"]",
  "clobTokenIds": "[\"0xabc123...\", \"0xdef456...\"]"
}
```

To get live odds for "Yes", use `clobTokenIds[0]` in `/midpoint` request.

---

## Rate Limiting

Both Gamma and CLOB APIs use IP-based rate limiting:

| Endpoint | Limit | Notes |
|----------|-------|-------|
| `/markets` (list) | ~100 req/min | Generous for read-only |
| `/markets/{id}` | ~200 req/min | Single market lookups |
| `/midpoint` | ~500 req/min | High rate for real-time data |
| `/orderbook` | ~100 req/min | Full book is heavier |

**Rate limit headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1646000060
```

If you hit a 429, wait `Retry-After` seconds before retrying.

---

## Authentication

**No authentication required.** Both APIs are fully public.

- No API keys needed
- No OAuth/tokens
- No authentication headers
- No IP whitelisting

All requests must include a `User-Agent` header for logging/abuse detection.

---

## Common Use Cases

### Get Trending Markets
```bash
curl "https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=10&order=volume&ascending=false"
```

### Search for Specific Market
```bash
curl "https://gamma-api.polymarket.com/markets?slug=bitcoin-above-100k&limit=1"
```

### Get Live Prices for Watchlist
```bash
# 1. Get market from Gamma API
curl "https://gamma-api.polymarket.com/markets?slug=will-trump-win-2024&limit=1"

# Extract clobTokenIds, then:
# 2. Get live midpoint from CLOB API
curl "https://clob.polymarket.com/midpoint?token_id=0xabc123"
```

### Build Morning Brief
```bash
# Fetch top 5 trending markets from Gamma
curl "https://gamma-api.polymarket.com/markets?active=true&limit=5&order=volume&ascending=false"

# Extract prices, volumes, close dates
# Format for user display
```

### Monitor Price Movements
```bash
# Periodic polling of CLOB midpoints:
for token_id in 0x... 0x... 0x...; do
  curl "https://clob.polymarket.com/midpoint?token_id=$token_id"
  sleep 1
done
```

---

## Troubleshooting

### "No markets found for [query]"
- Gamma API only returns 100 active markets per page
- Try broader search terms
- Check if market is closed (excluded from active listings)

### Missing CLOB midpoint
- Market may be new (not yet enabled on CLOB)
- Token IDs may be empty in response
- Graceful fallback: show Gamma API prices instead

### Empty outcomes/outcomePrices
- Market may be in initialization phase
- Some edge-case categorical markets may have non-standard formats
- Fallback to ["Yes", "No"] if parsing fails

### 429 Rate Limit
- Space requests out (use caching with 2min TTL)
- Batch similar queries
- Implement exponential backoff retry logic

### 500 Server Error
- Polymarket API may be temporarily down
- Retry after 30 seconds
- Check status page: https://polymarket.com

---

## Implementation Best Practices

1. **Always cache responses** — Use 120s TTL minimum for Gamma, 60s for CLOB
2. **Handle parsing gracefully** — Outcomes/prices may be strings; detect and parse as needed
3. **Set User-Agent header** — Required for all requests
4. **Implement timeout** — 10s per request; fail gracefully
5. **Use slug for lookups** — More reliable than market IDs
6. **Fallback outcomes** — Default to ["Yes", "No"] if parsing fails
7. **Filter client-side** — No full-text search endpoint; fetch and filter locally
8. **Graceful degredation** — CLOB midpoints are optional; show Gamma prices if unavailable

---

## Resources

- **Polymarket Web:** https://polymarket.com
- **API Status:** https://polymarket.com/status
- **Documentation:** https://polymarket.com/docs
- **Support:** support@polymarket.com

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-09 | Initial reference documentation |

Last updated: 2026-03-09
