# Polymarket MCP Reference

`graph-polymarket-mcp` — 31 tools combining 8 Graph subgraphs + REST APIs.
Distributed as a separate npm package; this skill only references it for routing.

## When to Use This vs Token API

**Prefer Token API** (`/v1/polymarket/*`) for common queries — markets, OHLCV, activity, positions, P&L, leaderboards, platform stats. Simpler REST, no npm install.

**Use this MCP** for advanced queries only:
- Live orderbook depth, live spreads (real-time CLOB data)
- Disputed markets, UMA resolution lifecycle
- Trader winrate, drawdown, profit factor (subgraph-specific P&L stats)
- CTF events (splits, merges, redemptions) per trader

## REST API Tools (no key needed)
| Tool | Description |
|------|-------------|
| search_markets | Search markets by text |
| get_market_info | Market metadata |
| list_polymarket_events | Browse events |
| get_live_prices | Current token prices |
| get_live_spread | Bid/ask spread |
| get_live_orderbook | Full order book |
| get_price_history | Historical prices |
| get_last_trade | Most recent trade |
| get_clob_market | CLOB market details |
| search_markets_enriched | Search + auto-enrich with prices and resolution |

## Graph Subgraph Tools (needs GRAPH_API_KEY)
| Tool | Subgraph | Description |
|------|----------|-------------|
| get_market_data | Main | Markets, conditions, trader counts |
| get_account_pnl | Beefy P&L | Trader winRate, profitFactor, maxDrawdown |
| get_top_traders | Beefy P&L | Top traders by profit |
| get_market_open_interest | Open Interest | USDC locked per market |
| get_market_resolution | Resolution | UMA oracle lifecycle, disputes |
| get_trader_profile | Traders | Per-trader CTF events |
| get_orderbook_trades | Orderbook | Order fills, volume |

## Install (separate package, optional)

`graph-polymarket-mcp` is published as an independent npm package on a
separate release schedule. This skill does **not** install it —
installation lives entirely upstream, where the maintainer publishes
pinned versions, a changelog, and audit instructions:

- npm: https://www.npmjs.com/package/graph-polymarket-mcp
- GitHub: https://github.com/PaulieB14/graph-polymarket-mcp

The upstream README describes how to register it with your MCP runtime and
how to provide a `GRAPH_API_KEY`. Audit the package, pin a known version,
and only run it if you trust the publisher.

## Note
Polymarket is migrating to CTF Exchange V2 + new collateral token (Polymarket USD).
Some subgraph tools may need updating after migration completes (~late April 2026).
