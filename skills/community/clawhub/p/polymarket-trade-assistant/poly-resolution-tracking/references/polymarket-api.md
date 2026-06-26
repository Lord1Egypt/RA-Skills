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
| `slug` | string | Filter by event slug (exact match) |

**Response structure:**

```json
[
  {
    "id": "event-id",
    "slug": "event-slug-for-url",
    "title": "Event Title",
    "description": "Event description with resolution criteria",
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

### Event Slug vs Market Slug

Polymarket page URLs use the **event-level slug**, not the market-level slug:

- Correct: `https://polymarket.com/event/will-trump-win-2028` (event slug)
- Wrong: `https://polymarket.com/event/will-trump-win-republican-primary-2028` (market slug — returns 404)

### GET /public-search

Search for events and markets by keyword.

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search keyword |

## 2. CLOB API (Price & Order Book)

**Base URL:** `https://clob.polymarket.com`

### GET /book?token_id={token_id}

Fetch full order book for a token.

### GET /price?token_id={token_id}&side={BUY|SELL}

Get indicative price for a specific side.

### GET /midpoint?token_id={token_id}

Get midpoint price.

### GET /prices-history?token_id={token_id}&interval={interval}&fidelity={fidelity}

Historical price data. Intervals: `1d`, `1w`, `1m`, `3m`, `all`.

## Constructing Market URLs

Market page: `https://polymarket.com/event/{event_slug}`

**You must use the event-level slug** (from the top-level `slug` field of the `/events` endpoint), not the market-level slug. Using a market slug will result in a 404 error.
