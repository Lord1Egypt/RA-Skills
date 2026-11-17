# MetricDuck — Company Fundamentals MCP Server

## Overview

MetricDuck is an MCP server providing company fundamentals, screening, and comparison data. It overlaps with the Finnhub fundamentals territory Rally uses for Quality (40%) and Safety (25%) signals, and is a candidate supplementary source for Rally research runs.

- **MCP endpoint:** `https://mcp.metricduck.com/mcp`
- **Transport:** Streamable HTTP
- **Status:** Healthy (6/6 successful queries on 2026-07-20)
- **Auth:** Bearer token — `METRICDUCK_API_KEY` sent on every MCP `tools/call`
- **Account:** Required (free tier, no card; Google/GitHub OAuth). Registered by <user> 2026-07-20. Key stored in `~/.hermes/.env`.

## When to Use

| User intent | Tool |
|---|---|
| "Search for companies like X" | `search_companies` |
| "Fundamentals for AAPL" | `company_overview` |
| "Compare AAPL vs MSFT" | `compare_companies` |
| "Screen for high-ROE low-debt names" | `screen_companies` |

## Tools

### search_companies
Search companies by free-text query.

**Params:** `{ query: string, limit?: int }`
**Returns:** list of matching companies with identifiers.

### company_overview
Full fundamentals overview for a company.

**Params:** `{ ticker?: string, name?: string }`
**Returns:** fundamentals (margins, ROE, debt/equity, FCF, growth, etc.).

### compare_companies
Side-by-side comparison of multiple companies.

**Params:** `{ companies: [string], metrics?: [string] }`
**Returns:** aligned metric table across the named companies.

### screen_companies
Screen companies against fundamentals criteria.

**Params:** `{ criteria: {...} }`
**Returns:** companies passing the screen.

## Error Handling

| Failure | Detection | Response |
|---|---|---|
| MCP unreachable | HTTP error on endpoint | Skip MetricDuck, fall back to Finnhub / price-proxy |
| Auth failure | 401 from MCP | Verify `METRICDUCK_API_KEY` in `~/.hermes/.env`; do not parse `.env` — read `os.environ` |
| Empty result | No matches | Fall back to Finnhub `stock/metric` |

## Rally Integration

Added as a Quality/Safety fundamentals fallback in `references/market-data-sources.md`:

Degradation chain: **Finnhub → MetricDuck (via Reach MCP) → price-based proxy**.

If Reach/MCP is unavailable, Rally degrades to its existing direct chain without regression.
