# Aave MCP Reference

`graph-aave-mcp` — 40 tools across 16 Graph subgraphs + Aave V4 API. Distributed
as a separate npm package; this skill only references it for routing.

## V2/V3 Tools (Graph Subgraphs)
Requires GRAPH_API_KEY. 16 tools covering 7 chains.

| Tool | Description |
|------|-------------|
| list_aave_chains | Supported chains with subgraph IDs |
| get_aave_reserves | All active markets — TVL, APY, LTV |
| get_aave_reserve | Deep detail on one asset |
| get_reserve_rate_history | Historical APY, utilization |
| get_user_positions | User's deposits, borrows, health factor |
| get_liquidations | Recent liquidation events |
| get_flash_loans | Flash loan transactions |
| get_governance_proposals | Aave governance |

## V4 Tools (Aave API — no key needed)
16 tools via api.aave.com.

| Tool | Description |
|------|-------------|
| get_v4_hubs | Liquidity hubs (Core, Plus, Prime) |
| get_v4_spokes | Cross-chain spokes (9 types) |
| get_v4_reserves | Per-spoke reserves with APYs |
| get_v4_user_positions | Cross-chain positions, health factor |
| get_v4_user_summary | Aggregated portfolio |
| get_v4_exchange_rate | Token prices via Chainlink |
| get_v4_swap_quote | CoW Protocol swap pricing |
| get_v4_claimable_rewards | Merkl and points rewards |

## Install (separate package, optional)

`graph-aave-mcp` is published as an independent npm package on a separate
release schedule. This skill does **not** install it — installation lives
entirely upstream, where the maintainer publishes pinned versions, a
changelog, and audit instructions:

- npm: https://www.npmjs.com/package/graph-aave-mcp
- GitHub: https://github.com/PaulieB14/graph-aave-mcp

The upstream README describes how to register it with your MCP runtime and
how to provide a `GRAPH_API_KEY`. Audit the package, pin a known version,
and only run it if you trust the publisher.
