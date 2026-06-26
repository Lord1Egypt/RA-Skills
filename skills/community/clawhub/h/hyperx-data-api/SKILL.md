---
name: hyperx-data-api
description: "Use when building apps with HyperX Data API — Hyperliquid wallet analytics, market data, Twitter/news feeds. Triggers on: \"HyperX API\", \"data-api.hyperx.trade\", \"wallet analysis\", \"Hyperliquid data\", \"crypto Twitter API\", \"market positions\", \"fills API\", \"trading analytics\"."
---

# HyperX Data API

Base URL: `https://data-api.hyperx.trade`

Hyperliquid on-chain analytics API — wallet PnL, market positions, crypto Twitter, news feeds.

## Authentication

| Method | Header / Field | How to get |
|--------|---------------|------------|
| API Token | `X-API-Key: <token>` | Login at [hyperx.trade](https://hyperx.trade) → Settings → API Token |
| Cookie | HyperX session cookie | Login at [hyperx.trade](https://hyperx.trade) |

To get an API key: visit [hyperx.trade/hyperliquid/settings](https://hyperx.trade/hyperliquid/settings), log in with your account, and generate a token in the **API Token** section. Free tier is available.

Twitter & News endpoints are **free, no auth required**.

## Rate Limits

| Tier | Budget / min | Monthly | Price |
|------|-------------|---------|-------|
| Free | 30 | 10,000 | $0 |
| Pro | 300 | 500,000 | $99/mo |
| Ultra | 1,200 | 5,000,000 | $399/mo |

Each endpoint has a **weight** (1–5). Each call costs `weight` from your budget.

## Endpoints

### Wallet Analysis

| Method | Path | Weight | Auth | Description |
|--------|------|--------|------|-------------|
| POST | `/wallet_analysis/{address}` | 5 | optional | Full wallet PnL analysis with positions, trades, risk metrics |
| GET | `/wallet_metrics/{address}` | 2 | none | Pre-calculated wallet performance metrics (win rate, ROI, PnL) |
| POST | `/wallet_metrics_query` | 2 | optional | Batch query wallet metrics with filters and sorting |
| GET | `/fills/{address}` | 5 | optional | Trading history (fills) for a wallet address |
| WS | `/fills/ws` | 5/msg | optional | Real-time fills stream. Addr limits: free=1, pro=50, ultra=300 |

### Market Analysis

All **weight 1**, **no auth** required.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/market/coins` | All tradable coins with metadata |
| GET | `/market/snapshots` | Market overview snapshots |
| GET | `/market/overview` | Aggregated market overview |
| GET | `/market/aggregate-positions` | Cross-asset aggregated position data |
| GET | `/market/top-positions/{asset}` | Top positions for a specific asset |
| GET | `/market/leverage-distribution/{asset}` | Leverage distribution |
| GET | `/market/pnl-distribution/{asset}` | PnL distribution |
| GET | `/market/concentration/{asset}` | Position concentration analysis |
| GET | `/market/whale-changes/{asset}` | Whale position changes tracking |
| GET | `/market/entry-price/{asset}` | Entry price distribution |
| GET | `/market/high-leverage-whales/{asset}` | High-leverage whale positions |
| GET | `/market/top-losers/{asset}` | Top losing positions |
| GET | `/market/top-winners/{asset}` | Top winning positions |
| GET | `/market/liquidation-heatmap/{asset}` | Liquidation price heatmap |
| GET | `/market/liquidation-positions/{asset}` | Positions near liquidation |

### Time Distribution

All **weight 1**, **auth optional**.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/wallet/time-distribution/{address}/hourly` | Hourly trading activity |
| GET | `/wallet/time-distribution/{address}/day-of-week` | Day-of-week patterns |
| GET | `/wallet/time-distribution/{address}/heatmap` | Full activity heatmap (hour × day) |
| GET | `/wallet/time-distribution/{address}/daily` | Daily trading volume |

### Twitter (FREE)

All **weight 1**, **no auth** required.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/twitter` | Twitter feed with filtering |
| GET | `/twitter/authors` | Active authors ranked by tweet count |
| WS | `/twitter/ws` | Real-time Twitter feed stream |

**GET `/twitter` params:**

| Param | Type | Description |
|-------|------|-------------|
| `screen_name` | string | Filter by author(s), comma-separated |
| `min_followers` | int | Minimum follower count |
| `user_tags` | string | Filter by tags: `trader`, `kol`, `founder`, `featured` |
| `tweet_type` | string | `reply`, `quote`, `retweet` |
| `keyword` | string | Content keyword search |
| `hours` | int | Time range in hours (1–168, default 24) |
| `page` / `page_size` | int | Pagination (max 100/page) |

**Response fields:**

```json
{
  "id": 12345,
  "sfe_id": "a2552b68aad7c9fa",
  "tweet_type": "reply",
  "tweet_id": "2032041519130296698",
  "tweet_time": "2026-03-12T10:30:26",
  "content": "tweet text...",
  "screen_name": "elonmusk",
  "display_name": "Elon Musk",
  "avatar_url": "https://pbs.twimg.com/...",
  "follower_count": 694593,
  "user_tags": ["founder", "featured"],
  "tweet_interaction_type": "reply",
  "media": [{"t": "image", "u": "https://..."}],
  "source_tweet": {
    "tweet_id": "...",
    "content": "original tweet...",
    "screen_name": "...",
    "follower_count": 24977,
    "media": []
  }
}
```

**WS `/twitter/ws` params:** `screen_names`, `min_followers`, `user_tags` (same filters as REST). Messages are JSON objects with same fields as REST response items.

### News (FREE)

All **weight 1**, **no auth** required.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/news` | Trading news from multiple sources |
| GET | `/news/channels` | Available news channel categories |

### BTC Mining

| Method | Path | Weight | Auth | Description |
|--------|------|--------|------|-------------|
| GET | `/btc-mining/shutdown-prices` | 1 | none | BTC mining shutdown prices by miner model |

## Quick Start

```python
import requests

BASE = "https://data-api.hyperx.trade"

# No auth needed for Twitter
tweets = requests.get(f"{BASE}/twitter", params={"hours": 1, "min_followers": 10000}).json()
for t in tweets["items"]:
    print(f"@{t['screen_name']}: {t['content']}")

# With API key for wallet analysis (get yours at hyperx.trade/hyperliquid/settings)
headers = {"X-API-Key": "your-api-key"}
pnl = requests.post(f"{BASE}/wallet_analysis/0x1234...", headers=headers).json()
```

```python
# WebSocket — real-time Twitter stream
import asyncio, websockets, json

async def stream():
    async with websockets.connect(f"wss://data-api.hyperx.trade/twitter/ws?min_followers=5000") as ws:
        async for msg in ws:
            tweet = json.loads(msg)
            print(f"@{tweet['screen_name']}: {tweet.get('content', '')}")

asyncio.run(stream())
```

## API Catalog Endpoint

`GET /api-catalog` — returns the full structured catalog as JSON with dynamic weights.
