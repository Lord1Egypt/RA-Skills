---
name: indigo-assets
description: "Query real-time prices and data for Indigo Protocol iAssets, ADA, and INDY tokens."
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---

# iAsset Prices & Data

Query real-time prices and data for Indigo Protocol iAssets (iUSD, iBTC, iETH, iSOL), ADA, and INDY tokens.

## MCP Tools

| Tool | Description |
|------|-------------|
| `get_assets` | Get all Indigo iAssets with prices and interest data |
| `get_asset` | Get details for a specific iAsset (iUSD, iBTC, iETH, iSOL) |
| `get_asset_price` | Get the current price for a specific iAsset |
| `get_ada_price` | Get the current ADA price in USD |
| `get_indy_price` | Get the current INDY token price in ADA and USD |

## Sub-Skills

- [Asset Prices](sub-skills/asset-prices.md) — Query iAsset prices and details
- [Token Prices](sub-skills/token-prices.md) — Query ADA and INDY token prices

## References

- [MCP Tools Reference](references/mcp-tools.md) — Detailed tool parameters and return types
- [Asset Concepts](references/concepts.md) — iAssets, oracles, INDY token, and interest rates
