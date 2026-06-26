# Polymarket API Reference

## Overview

Three public APIs power market data access. No authentication is required for read-only operations.

## 1. Gamma API (Market Discovery)

**Base URL:** `https://gamma-api.polymarket.com`

### GET /markets

List markets with filtering and sorting.

| Parameter | Type | Description |
|-----------|------|-------------|
| `active` | bool | Filter by active status (`true` = tradeable) |
| `closed` | bool | Filter by closed status |
| `order` | string | Sort by: `volume_24hr`, `liquidity`, `start_date`, `end_date`, `competitive` |
| `ascending` | bool | Sort direction (default: `false`) |
| `limit` | int | Results per page (max 100) |
| `offset` | int | Pagination offset |

### GET /markets/{id}

Fetch a single market by ID.

### Key Response Fields

```json
{
  "id": "string",
  "slug": "url-friendly-id",
  "question": "Will X happen by Y?",
  "description": "Detailed resolution criteria...",
  "outcomes": "[\"Yes\",\"No\"]",
  "outcomePrices": "[\"0.35\",\"0.65\"]",
  "clobTokenIds": "[\"token_yes\",\"token_no\"]",
  "conditionId": "0x...",
  "active": true,
  "closed": false,
  "enableOrderBook": true,
  "liquidityNum": 50000.0,
  "volume24hr": 12000.0,
  "volumeNum": 500000.0,
  "bestBid": 0.34,
  "bestAsk": 0.36,
  "spread": 0.02,
  "lastTradePrice": 0.35,
  "oneDayPriceChange": -0.05,
  "oneWeekPriceChange": 0.10,
  "endDate": "2026-06-01T00:00:00Z"
}
```

Note: `outcomes`, `outcomePrices`, and `clobTokenIds` may be JSON-encoded strings; parse them accordingly.

### GET /events

List events. Each event contains a nested `markets` array. **Recommended endpoint** for market discovery because it provides the event-level slug needed for correct URL construction.

| Parameter | Type | Description |
|-----------|------|-------------|
| `active` | bool | Filter by active status (`true` = tradeable) |
| `closed` | bool | Filter by closed status |
| `order` | string | Sort by: `volume24hr`, `liquidity`, `startDate`, `endDate` |
| `ascending` | bool | Sort direction (default: `false`) |
| `limit` | int | Results per page (max **50**, lower than /markets' 100) |
| `offset` | int | Pagination offset |

**Response structure:**

```json
[
  {
    "id": "event-id",
    "slug": "event-slug-for-url",
    "title": "Event Title",
    "description": "Event description",
    "markets": [
      {
        "id": "market-id",
        "slug": "market-slug",
        "question": "Specific question?",
        "outcomes": "[\"Yes\",\"No\"]",
        "outcomePrices": "[\"0.35\",\"0.65\"]",
        "clobTokenIds": "[\"token_yes\",\"token_no\"]",
        "liquidityNum": 50000.0,
        "volume24hr": 12000.0,
        "enableOrderBook": true,
        "endDate": "2026-06-01T00:00:00Z"
      }
    ]
  }
]
```

Note: One event may contain one or more markets. The nested markets array fields are identical to those returned by the `/markets` endpoint.

### Event Slug vs Market Slug

Polymarket page URLs use the **event-level slug**, not the market-level slug:

- Correct: `https://polymarket.com/event/will-trump-win-2028` (event slug)
- Wrong: `https://polymarket.com/event/will-trump-win-republican-primary-2028` (market slug — returns 404)

When fetching from `/events`, the event slug is in the top-level `slug` field, while the market slug is in the nested `markets[].slug`. Always use the event-level slug for URL construction.

### GET /public-search

Search for events and markets by keyword.

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search keyword |

## 2. CLOB API (Price & Order Book)

**Base URL:** `https://clob.polymarket.com`

### GET /book?token_id={token_id}

Fetch full order book for a token.

```json
{
  "market": "condition_id",
  "asset_id": "token_id",
  "bids": [{"price": "0.34", "size": "1500.0"}, ...],
  "asks": [{"price": "0.36", "size": "2000.0"}, ...],
  "tick_size": "0.01",
  "min_order_size": "5"
}
```

Bids are sorted descending by price; asks are sorted ascending.

### GET /price?token_id={token_id}&side={BUY|SELL}

Get indicative price for a specific side.

### GET /midpoint?token_id={token_id}

Get midpoint price (average of best bid and best ask).

### GET /spread?token_id={token_id}

Get current bid-ask spread.

### GET /prices-history?token_id={token_id}&interval={interval}&fidelity={fidelity}

Historical price data. Intervals: `1d`, `1w`, `1m`, `3m`, `all`. Fidelity: number of data points.

## 3. Data API (Analytics)

**Base URL:** `https://data-api.polymarket.com`

### GET /trades

Recent trades with filtering.

| Parameter | Type | Description |
|-----------|------|-------------|
| `market` | string[] | Condition ID(s) |
| `limit` | int | Page size (max 10000) |
| `side` | string | `BUY` or `SELL` |

### GET /oi?market={condition_id}

Open interest for a market.

### GET /holders?market={condition_id}

Top token holders for a market.

## Constructing Market URLs

Market page: `https://polymarket.com/event/{event_slug}`

**You must use the event-level slug** (from the top-level `slug` field of the `/events` endpoint), not the market-level slug. Using a market slug will result in a 404 error.

If you only have market data (via `/markets`), its `slug` field is market-level and not suitable for URL construction. Use the `/events` endpoint instead.
