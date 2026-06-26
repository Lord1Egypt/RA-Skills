---
name: graph-limitless-mcp
description: "Query Limitless prediction markets on Base — live odds, trader P&L, whale tracking, market stats, and daily volume from The Graph's decentralized network."
version: 1.0.0
homepage: https://github.com/PaulieB14/limitless-subgraphs
metadata:
  clawdbot:
    emoji: "🎯"
    requires:
      bins: ["node"]
      env: ["GRAPH_API_KEY"]
    primaryEnv: "GRAPH_API_KEY"
---

# Graph Limitless MCP

Query Limitless prediction markets on Base. Get live market data, trader analytics, positions, and volume — powered by The Graph's decentralized network.

## Try it

- `"What are the top markets on Limitless by volume?"`
- `"Show me the biggest traders on Limitless"`
- `"Daily volume trends for the last 30 days"`
- `"Who holds the largest positions in this market?"`
- `"What markets resolved today?"`
- `"Show me whale trades over $10K"`

## What's inside

| Tool | What it does |
|------|-------------|
| `get_platform_stats` | Total markets, volume, trades, users across Simple + NegRisk |
| `get_markets` | Browse markets with volume, trade counts, resolution status |
| `search_markets` | Search by keyword or category via Limitless API |
| `get_market_details` | Deep dive on a specific market — conditions, outcomes, payouts |
| `get_trades` | Recent trades with USD amounts, buy/sell, maker/taker |
| `get_user_stats` | Trader profile — volume, trade count, first/last trade |
| `get_user_trades` | Full trade history for any wallet |
| `get_user_positions` | Current holdings with token balances |
| `get_daily_snapshots` | Daily volume, trades, splits, merges, redemptions |
| `get_market_daily_snapshots` | Per-market daily breakdown |
| `get_top_traders` | Leaderboard by volume |
| `get_whale_trades` | Large trades filtered by minimum USD amount |

## Data coverage

- **Simple Markets**: 8,000+ markets, 3.9M trades, $317M volume
- **NegRisk Markets**: 700+ markets, multi-outcome prediction markets
- **Network**: Base L2
- **Updated**: Real-time via The Graph's decentralized indexing network

## Install

```bash
GRAPH_API_KEY=your-key npx graph-limitless-mcp
```

Get a free API key at [The Graph Market](https://thegraph.market/dashboard#api-keys).

## External Endpoints

| Endpoint | Data sent | Purpose |
|----------|-----------|---------|
| `gateway.thegraph.com` | GraphQL queries with your API key | Queries 2 Limitless subgraphs on Base |
| `api.limitless.exchange` | Market search queries | Fetches market metadata and categories |

No other endpoints are contacted. No data is stored locally.

## Security & Privacy

- **Runs locally** via `npx` — no remote server
- **Your API key stays local** — only sent to The Graph Gateway
- **No persistent storage** — no database, no local files
- **Open source** — full code at [github.com/PaulieB14/limitless-subgraphs](https://github.com/PaulieB14/limitless-subgraphs)

## Model Invocation Note

This skill may be invoked autonomously by your AI agent when it detects a prediction market question about Limitless. Disable the skill to opt out.

## Trust Statement

By using this skill, GraphQL queries are sent to `gateway.thegraph.com` using your API key, and market metadata requests go to `api.limitless.exchange`. Only install if you trust these endpoints with your query data.

## Links

- GitHub: https://github.com/PaulieB14/limitless-subgraphs
- npm: https://www.npmjs.com/package/graph-limitless-mcp
- Limitless: https://limitless.exchange
- The Graph: https://thegraph.com
