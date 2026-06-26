---
name: indigo-analytics
description: "Query TVL, protocol statistics, APR rewards, and DEX yield data for the Indigo Protocol."
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---

# Protocol Analytics

Query TVL, protocol statistics, APR rewards, and DEX yield data for the Indigo Protocol on Cardano.

## MCP Tools

| Tool | Description |
|------|-------------|
| `get_tvl` | Get the total value locked in Indigo Protocol |
| `get_protocol_stats` | Get protocol-wide statistics and metrics |
| `get_apr_rewards` | Get APR reward rates across Indigo pools |
| `get_apr_by_key` | Get APR reward rate for a specific pool key |
| `get_dex_yields` | Get current DEX yield data for Indigo iAsset pairs |

## Sub-Skills

- [TVL & Stats](sub-skills/tvl-stats.md) — Total value locked and protocol statistics
- [APR Rewards](sub-skills/apr-rewards.md) — APR reward rates for pools
- [DEX Yields](sub-skills/dex-yields.md) — DEX yield data for iAsset pairs

## References

- [MCP Tools Reference](references/mcp-tools.md) — Detailed tool parameters and return types
- [Analytics Concepts](references/concepts.md) — TVL, APR/APY, pool types, and data sources
