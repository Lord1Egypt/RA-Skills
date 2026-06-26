---
name: predictfun-mcp
description: Access Predict.fun prediction market data on BNB Chain — platform stats, market analysis, trader profiling, yield mechanics, and behavioral meta-tools via The Graph.
metadata:
  {"openclaw": {"requires": {"bins": ["node"], "env": ["GRAPH_API_KEY"]}, "primaryEnv": "GRAPH_API_KEY", "homepage": "https://github.com/PaulieB14/predictfun-subgraphs"}}
---

# Predict.fun MCP

Structured access to Predict.fun prediction market data on BNB Chain — platform stats, market analysis, trader profiling, yield mechanics, and behavioral meta-tools.

## Tools

- **get_platform_stats** — Full platform overview: volume, OI, yield, sync status
- **get_top_markets** — Rank markets by volume, open interest, or trade count
- **get_market_details** — Deep dive: OI, resolution, top holders, orderbook stats
- **get_trader_profile** — Full P&L: trades, positions, payouts, yield rewards
- **get_recent_activity** — Latest trades, splits, merges, redemptions, or yield claims
- **get_yield_overview** — Venus Protocol deposits, redemptions, yield stats
- **get_whale_positions** — Largest holders with % of market OI
- **get_leaderboard** — Top traders by volume, payouts, or trade count
- **get_resolved_markets** — Recently settled markets with outcomes
- **query_subgraph** — Custom GraphQL against any of the three subgraphs
- **find_trader_persona** — Classify a trader: whale, yield farmer, arbitrageur, early mover, sniper
- **scan_trader_personas** — Find traders matching a behavioral archetype
- **tag_market_structure** — Tag a market by resolution latency, liquidity, oracle type, tail risk
- **scan_markets_by_structure** — Find markets by structural filter

## Requirements

- **Runtime:** Node.js >= 18 (runs via `npx`)
- **Environment variables:**
  - `GRAPH_API_KEY` (required) — Free API key from [The Graph Studio](https://thegraph.com/studio/). Used to query three Predict.fun subgraphs via The Graph Gateway. Queries are billed to your key (free tier: 100K queries/month).

## Install

```bash
GRAPH_API_KEY=your-key npx predictfun-mcp
```

## Network & Data Behavior

- All tool calls make GraphQL requests to The Graph Gateway (`gateway.thegraph.com`) using your API key.
- Three subgraphs are queried: predictfun-orderbook, predictfun-positions, and predictfun-yield (subgraph IDs are built into the server).
- No local database or persistent storage is used.
- The SSE transport (`--http` / `--http-only`) starts a local HTTP server on port 3850 (configurable via `MCP_HTTP_PORT` env var).

## Use Cases

- Get real-time platform stats and market rankings on Predict.fun
- Profile traders by P&L, volume, and behavioral archetypes
- Analyze market quality: liquidity depth, OI concentration, resolution speed
- Track yield mechanics via Venus Protocol integration
- Run custom GraphQL queries against orderbook, positions, and yield subgraphs
