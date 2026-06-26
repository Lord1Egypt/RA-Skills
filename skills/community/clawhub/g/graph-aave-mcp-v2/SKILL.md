---
name: graph-aave-mcp
description: Aave V2/V3/V4 MCP server — 46 tools across 16 Graph subgraphs + Aave V4 API + on-chain view contracts. Reserves, positions, cross-chain liquidation risk monitoring with live HF confirmation, governance, V4 hubs/spokes, exchange rates, swap quotes, rewards, protocol history, and a durable findings store that survives context compaction.
version: 4.1.21
metadata:
  openclaw:
    requires:
      env:
        - GRAPH_API_KEY
    primaryEnv: GRAPH_API_KEY
    envVars:
      - name: GRAPH_API_KEY
        required: true
        description: API key for The Graph network. Free at https://thegraph.com/studio/ (100K queries/month).
    emoji: "📊"
    homepage: https://github.com/PaulieB14/graph-aave-mcp
---

# graph-aave-mcp

MCP server for Aave V2, V3, and V4 — 46 tools across 16 Graph subgraphs + the Aave V4 API + on-chain view contracts.

## Setup

```bash
npm install -g graph-aave-mcp
graph-aave-mcp
```

Or add to Claude Code:

```bash
claude mcp add graph-aave -- graph-aave-mcp
```

Set your Graph API key (free at https://thegraph.com/studio/):

```bash
export GRAPH_API_KEY=your-key-here
```

## What it does

- **V2/V3** (16 tools): Reserves, positions, liquidations, borrows, supplies, flash loans, governance across 11 subgraphs on 7 chains (Ethereum, Arbitrum, Base, Polygon, Optimism, Avalanche)
- **Liquidation Risk** (8 tools): Cross-chain health factors, risk scores, risk alerts, at-risk positions across 5 chains, with **live on-chain HF confirmation against Aave view contracts**
- **V4 API** (16 tools): Hubs, spokes, reserves, exchange rates, user positions, activities, swap quotes, claimable rewards
- **Findings store** (new in 4.1.0): durable per-session findings that survive context compaction

## What's new in 4.1.0

- Live on-chain reads — every reported health factor is double-checked against the Aave protocol's view contracts before surfacing
- Durable findings store — investigations persist across context-window compaction so multi-step analyses don't lose state

## Example questions

- "What are the top Aave V3 markets on Ethereum by TVL?"
- "Compare WETH borrow rates across all chains"
- "Which positions are at risk of liquidation on Arbitrum?"
- "Show me Aave V4 hub utilization"
- "Is wallet 0x... at risk of liquidation on any chain — and confirm the HF on-chain?"

## Links

- npm: https://www.npmjs.com/package/graph-aave-mcp
- GitHub: https://github.com/PaulieB14/graph-aave-mcp
