---
name: polymarket-data-layer
description: Shared Polymarket and prediction-market data access layer. Use this skill whenever another skill or task needs trader positions, trade history, market metadata, leaderboard data, win-rate or PnL statistics, or any other read-only market intelligence.
---

# Polymarket Data Access Layer

This skill is the shared data layer for the repository. It exists so that individual skills do not need to re-implement MCP session handling, query helpers, market metadata lookups, or local caching logic.

---

## Data Source Priority

```text
1. PredicTradar MCP Server  https://api.predictradar.ai/api/mcp/v2  (primary)
2. polymarket-cli           polymarket <command>                    (service degradation fallback)
3. Polymarket Data API      https://data-api.polymarket.com         (final fallback)
```

Use the **PredicTradar MCP Server** by default. It is the canonical shared entry point for this repo.

---

## Current MCP Notes

The live MCP service now requires a full MCP session handshake:

1. Call `initialize`
2. Read the `mcp-session-id` response header
3. Send `notifications/initialized`
4. Reuse the session header for `tools/list` and `tools/call`

The repository wrapper at [mcp-client.js](/Users/cutie/Documents/New%20project/predictradar-agent-skills/polymarket-data-layer/scripts/mcp-client.js) already handles this automatically, so skills should call the wrapper instead of implementing raw MCP requests unless they need low-level debugging.

Health endpoint observed on March 31, 2026:
- `service`: `predictradar-mcp`
- `version`: `1.0.0`
- `protocolVersion`: `2025-03-26`

---

## MCP Capabilities

The current live tool catalog includes:

| Tool | Purpose | Notes |
|------|---------|-------|
| `get_traders` | Trader list with sorting and pagination | Sort fields include `volume_24h`, `volume_7d`, `volume_30d`, `pnl_24h`, `pnl_7d`, `pnl_30d`, `win_rate` |
| `get_trader_detail` | Detailed trader profile | Includes positions, recent activity, and analysis payloads |
| `get_markets` | Market list | Supports `status`, `search`, `limit`, `offset` |
| `get_market_detail` | Single-market detail | Newer high-level tool, useful when a skill already has a `conditionId` |
| `get_leaderboard` | Ranked trader leaderboard | `period`: `24h`, `7d`, `30d`, `all` |
| `get_market_stats` | Aggregate market statistics | Includes volume, trader counts, active markets, hot markets |
| `search_events` | Event search | Supports `query`, `category`, `status`, `limit` |
| `run_query_preview` | Preferred read-only SQL preview | Preview mode only, limited rows |
| `run_query` | Legacy alias for preview SQL | Keep compatibility, but prefer `run_query_preview` in new docs |
| `open_query_stream` | Streamed SQL export | Use for larger result sets instead of overloading preview queries |
| `list_tables` | Table catalog | Supports `category` filter: `trading`, `market`, `user`, `system`, `all` |
| `describe_table` | Table schema inspection | Can include sample rows |

Key documentation updates compared with the older version:
- The handshake requirement must be documented explicitly.
- `get_market_detail` should be listed as a first-class tool.
- `run_query_preview` should be treated as the preferred preview-query tool.
- `run_query` should be described as a compatibility alias.
- `open_query_stream` should be documented for larger exports.

---

## Current Table Inventory

Live `list_tables` currently returns two trading tables:

| Table | Description | Approx. Rows |
|------|-------------|--------------|
| `trades` | Historical trade records including `trade`, `mint`, `burn`, and `redeem` actions | ~296.6M |
| `positions` | Current and historical positions | ~30.5M |

These row counts are service-side approximations and may grow over time.

---

## Key Schema Notes

### `trades`

Important columns currently exposed by `describe_table("trades")`:
- `id`
- `created_at`
- `updated_at`
- `platform`
- `wallet_address`
- `platform_id`
- `tx_hash`
- `transaction_hash`
- `condition_id`
- `trader_id`
- `market_id`
- `token_id`
- `side`
- `type`
- `outcome`
- `outcome_side`
- `price`
- `size`
- `amount`
- `fee`
- `fee_amount`
- `outcome_index`
- `profit`
- `usd_amount`
- `chain_id`
- `block_number`
- `block_timestamp`
- `traded_at`

Practical takeaways:
- `amount` remains the most portable trade-size field for aggregate SQL.
- `usd_amount` is available and nullable, which is useful for whale-style filters.
- `type` is not just `trade`; it also includes `mint`, `burn`, and `redeem`.
- `condition_id` and `market_id` are both available directly in the table, so legacy mapping tables should not be required for normal skill flows.

### `positions`

Important columns currently exposed by `describe_table("positions")`:
- `id`
- `created_at`
- `updated_at`
- `platform`
- `wallet_address`
- `trader_id`
- `market_id`
- `token_id`
- `condition_id`
- `outcome`
- `outcome_index`
- `outcome_side`
- `size`
- `size_frozen`
- `avg_price`
- `avg_entry_price`
- `current_price`
- `initial_value`
- `current_value`
- `total_bought`
- `realized_pnl`
- `unrealized_pnl`
- `unrealized_pnl_percent`
- `daily_pnl_change`
- `is_redeemable`
- `is_closed`
- `chain_id`
- `last_updated_at`
- `opened_at`
- `closed_at`

Practical takeaways:
- `avg_entry_price`, `current_price`, `is_redeemable`, and lifecycle timestamps should now be reflected in any field documentation.
- `positions` is richer than the older docs implied, so skills can describe both PnL state and lifecycle state more precisely.

---

## Quick Start

```js
const mcp = require("../../polymarket-data-layer/scripts/mcp-client");

// health + handshake
const ok = await mcp.ping();
const health = await mcp.health();
const init = await mcp.initialize();

// high-level tools
const leaderboard = await mcp.getLeaderboard({ period: "7d", rankBy: "pnl", limit: 10 });
const traders = await mcp.getTraders({ sortBy: "pnl_7d", order: "desc", limit: 20 });
const markets = await mcp.getMarkets({ status: "active", search: "Fed", limit: 20 });
const market = await mcp.getMarketDetail("0x...");

// preview query
const rows = await mcp.query(`
  SELECT condition_id, SUM(amount) AS volume_24h
  FROM trades
  WHERE traded_at >= now() - INTERVAL 1 DAY
    AND type = 'trade'
  GROUP BY condition_id
  ORDER BY volume_24h DESC
  LIMIT 20
`);

// streamed query export
const stream = await mcp.openQueryStream(`
  SELECT wallet_address, SUM(amount) AS volume_30d
  FROM trades
  WHERE traded_at >= now() - INTERVAL 30 DAY
  GROUP BY wallet_address
`);
```

---

## Environment Variables

```bash
MCP_URL=https://api.predictradar.ai
MCP_API_KEY=pr_public_predictradar
```

The wrapper already defaults to these values unless overridden.

---

## Shared Scripts

### [mcp-client.js](/Users/cutie/Documents/New%20project/predictradar-agent-skills/polymarket-data-layer/scripts/mcp-client.js)

Use this for:
- session-aware MCP calls
- preview SQL queries
- streamed query exports
- health and initialization checks
- high-level market and trader tools

Highlights:
- automatic MCP session handshake
- retry support for transient network issues
- `openQueryStream`, `consumeQueryStream`, `cancelQueryStream`, and `queryStream`
- wrappers for `getTraders`, `getTraderDetail`, `getLeaderboard`, `getMarketStats`, `getMarkets`, `getMarketDetail`, and `searchEvents`

### [mcp-examples.js](/Users/cutie/Documents/New%20project/predictradar-agent-skills/polymarket-data-layer/scripts/mcp-examples.js)

Run this when you need to inspect:
- health and handshake behavior
- current tool inventory
- table catalog and schema previews
- example preview queries
- stream-export behavior
- trader lookup examples

### [gamma-client.js](/Users/cutie/Documents/New%20project/predictradar-agent-skills/polymarket-data-layer/scripts/gamma-client.js)

Use this when a skill needs:
- market metadata by `conditionId`
- market-to-domain mapping
- keyword-based market discovery
- event URL resolution

### [queries.js](/Users/cutie/Documents/New%20project/predictradar-agent-skills/polymarket-data-layer/scripts/queries.js)

Use this for reusable repo-level aggregations such as:
- all addresses
- base trading metrics
- ROI metrics
- address-to-domain volume breakdowns

### [smartmoney.js](/Users/cutie/Documents/New%20project/predictradar-agent-skills/polymarket-data-layer/scripts/smartmoney.js)

Use this only when a skill explicitly needs the local smart-money classification layer. Prefer read-only cache access when possible unless the workflow truly requires a fresh classification.

### [cache.js](/Users/cutie/Documents/New%20project/predictradar-agent-skills/polymarket-data-layer/scripts/cache.js)

Use this for local file-backed cache reads and writes inside longer-running scripts.

---

## Query Guidance

### Preview Queries

Use preview SQL when:
- you need a compact result set
- the skill only needs top rows or aggregate rows
- a result set comfortably fits within preview limits

Guidance:
- use `mcp.query(...)` or `mcp.queryWithRetry(...)`
- keep result sizes tight with `LIMIT`
- explicitly filter `type = 'trade'` when you do not want `mint`, `burn`, or `redeem`

### Streamed Exports

Use `open_query_stream` when:
- you need more rows than a preview call should return
- a skill needs a larger export for downstream processing
- you want a preview plus a temporary stream URL

### Fallbacks

If MCP is unavailable:
1. fall back to `polymarket-cli` when appropriate
2. fall back to the Polymarket Data API as a final option

---

## Cache Policy

Recommended cache behavior:
- prefer cached metadata when freshness is not critical
- bypass cache when the user explicitly asks for the latest or real-time data
- treat smart-money classification as a separate cacheable enrichment layer
- avoid over-caching rapidly changing short-window trading snapshots

---

## Important Notes

1. `condition_id` is the canonical cross-system market key.
2. `wallet_address` should be normalized to lowercase for SQL comparisons.
3. `run_query` is no longer the best term for new docs; describe it as a legacy alias and prefer `run_query_preview`.
4. `open_query_stream` should be mentioned anywhere a skill may need larger result sets.
5. Skills should not document raw MCP session handling unless they are intentionally teaching low-level protocol behavior; ordinary skills should point to `mcp-client.js`.
