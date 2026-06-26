---
name: massive-financial-connector
description: Full Massive (Polygon) market-data connector with secure local key handling. Starts the official MCP server and supports endpoint discovery, endpoint docs, generic API calls, SQL-style table querying, and post-processing functions, plus quick scripts for common quote checks. Use for stock/options/forex/crypto/indices real-time or historical queries sourced from Massive.
---

# Massive Financial Connector

Use Massive/Polygon as the primary market-data source.

## Required environment

- Require `MASSIVE_API_KEY` in local environment.
- Never print, commit, or upload API keys.
- Accept both quoted and unquoted local env values.
- If auth fails with `Unknown API Key`, verify local shell env and active key status in Massive dashboard.

## Full capability mode (official MCP server)

Start the official Massive MCP server (all features from `mcp_massive`):

```bash
scripts/start-mcp-server.sh
```

This exposes the full MCP toolset:
- `search_endpoints`
- `get_endpoint_docs`
- `call_api`
- `query_data`

With these, you can cover the full repo workflow: endpoint discovery, docs lookup, generic market API access, storing/querying data with SQL, and post-processing functions.

## Quick commands (common checks)

Run from this skill directory:

```bash
scripts/get-last-trade.sh AAPL
scripts/get-prev-close.sh AAPL
scripts/get-agg-day.sh AAPL 2026-03-05
```

## Output rules

- Return concise numeric result first (e.g., last trade price), then timestamp/exchange metadata.
- If Massive is unavailable, state failure explicitly and ask whether to use a fallback source.
- For investment-style prompts, add a short non-advice disclaimer.

## Included scripts

- `scripts/start-mcp-server.sh`: launch official Massive MCP server (full functionality).
- `scripts/get-last-trade.sh <SYMBOL>`: latest trade snapshot.
- `scripts/get-prev-close.sh <SYMBOL>`: previous close and change context.
- `scripts/get-agg-day.sh <SYMBOL> <YYYY-MM-DD>`: daily OHLCV bar.
