---
name: graph-limitless-mcp
description: "Protocol-wide on-chain analytics for Limitless prediction markets on Base — trader P&L, top traders, market and daily volume history, liquidity events, and raw GraphQL, from the Limitless subgraphs on The Graph's decentralized network."
version: 1.1.0
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

19 tools, all read-only.

| Tool | What it does |
|------|-------------|
| **Protocol-wide** | |
| `get_global_stats` | Get combined protocol-wide stats across both simple and negrisk markets. |
| `get_daily_protocol_stats` | Get daily protocol stats (volume, trades, fees, splits, merges, redemptions) across both market types as a time series. |
| `compare_market_types` | Side-by-side comparison of simple vs negrisk market performance. |
| `get_recent_activity` | Get a unified feed of all recent on-chain activity: trades, splits, merges, and redemptions across both market types wit |
| `get_liquidity_events` | Get splits, merges, and redemptions — the liquidity lifecycle events. |
| `get_conditions` | Get conditions (markets that have been prepared on-chain) with resolution status. |
| **Markets** | |
| `search_markets` | Search markets by keyword or category. |
| `get_market_analytics` | Get full analytics for a specific market by conditionId. |
| `get_market_trades` | Get trades for a specific market. |
| `get_market_positions` | Get top position holders for a specific market. |
| `get_market_daily_snapshots` | Get daily volume, trades, and fees for a specific market over time. |
| `get_market_lifecycle` | Get the complete lifecycle of a market: creation, trading stats, splits/merges, resolution status, and redemptions — all |
| **Traders** | |
| `get_trader_profile` | Get a trader's profile across both simple and negrisk markets. |
| `get_trader_trades` | Get a trader's recent trades across both market types, enriched with market names. |
| `get_trader_positions` | Get a trader's current positions across both market types with balances and PnL. |
| `get_trader_pnl` | Calculate a trader's estimated profit & loss from on-chain data. |
| `get_top_traders` | Get top traders ranked by volume, trade count, or PnL. |
| **Escape hatches** | |
| `get_subgraph_schema` | Get the GraphQL schema for a Limitless subgraph via introspection. |
| `query_subgraph` | Run a raw GraphQL query against a Limitless subgraph. |

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
