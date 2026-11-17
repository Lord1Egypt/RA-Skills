---
name: graph-aave-mcp
description: Aave V2/V3/V4 MCP server — 62 tools across 18 Graph subgraphs + Aave V4 API + on-chain view contracts. Reserves, positions, cross-chain liquidation risk monitoring with live HF confirmation, governance, V4 hubs/spokes, Base equity gap shock and oracle status, loan-swap analytics, exchange rates, swap quotes, rewards, protocol history, and a durable findings store that survives context compaction.
version: 4.3.3
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

MCP server for Aave V2, V3, and V4 — 62 tools across 18 Graph subgraphs + the Aave V4 API + on-chain view contracts.

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

- **V2/V3** (16 tools): Reserves, positions, liquidations, borrows, supplies, flash loans, governance across 11 subgraphs on 7 chains (Ethereum, Arbitrum, Base, Polygon, Optimism, Avalanche). `get_aave_reserves` and `get_v4_reserves` accept `symbols` / `limit` / `compact` — use them, the unfiltered Ethereum response is ~28k tokens. `_humanReadable.availableLiquidity` is aToken supply minus debt, and `*APY` is compounded. `_freshness.lagSeconds` is subgraph lag.
- **Liquidation Risk** (8 tools): Cross-chain health factors, risk scores, risk alerts, at-risk positions across 5 chains, with **live on-chain HF confirmation against Aave view contracts**
- **Live RPC** (2 tools): `get_live_user_account_data`, `get_live_reserve_detail`. Public RPC fallbacks plus 429 backoff. Set `ETHEREUM_RPC_URL` / `BASE_RPC_URL` for production.
- **Findings store** (4 tools): durable per-session findings that survive context compaction
- **V4 API** (16 tools): Hubs, spokes, reserves, exchange rates, user positions, activities, swap quotes, claimable rewards. Hub, reserve, and user reads default to Ethereum + Base.
- **Loan swaps** (3 tools): `get_v4_loan_swaps`, `get_v4_loan_swap_stats`, `get_v4_borrow_swap_quote` (quote only, no order signing)
- **V4 Omnigraph** (5 tools): hub flows, user risk trajectory, liquidation post-mortems, treasury flows, spoke config history
- **V4 Subgraph** (6 tools, Base default / Ethereum): liquidations by liquidator/user, hub asset rates + fees, config-change history, daily hub flows, user risk premium + activity, treasury events
- **Base stocks** (2 tools): `simulate_stock_gap_shock`, `get_oracle_status`

## What's new

- V3 `availableLiquidity` is derived (aToken − debt) and reserve answers include `_freshness` (block, timestamp, lag)
- V3 APYs are compounded the way the Aave UI does; `supplyAPR` keeps the linear ray figure
- V4 hub, spoke, reserve, and user reads default to Ethereum + Base (pass `chainId` to narrow)
- `get_live_reserve_detail` tries several public RPCs and backs off on HTTP 429
- Base equities: `simulate_stock_gap_shock` and `get_oracle_status` (Chainlink 24/5, weekend-update flag)
- Loan swaps: `get_v4_loan_swaps`, `get_v4_loan_swap_stats`, and a read-only `get_v4_borrow_swap_quote`. `get_v4_user_activities` takes `types` and includes `BORROW_SWAP` by default

## What's new in 4.2.0 – 4.3.x

- V4 subgraph tools: Base (Coinbase tokenized-stocks hub) by default, Ethereum optional via `network`
- Dead backends fail loudly instead of returning empty data; reserve tools accept `symbols` / `limit` / `compact`

## Added in 4.1.0

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
