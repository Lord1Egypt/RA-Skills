---
name: indigo-dex
description: "Interact with decentralized exchanges on Cardano through the Indigo Protocol ecosystem."
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---

# DEX Integration

Skill for interacting with decentralized exchanges on Cardano through the Indigo Protocol ecosystem. Query available tokens, get swap estimates via SteelSwap, explore Iris liquidity pools, and check wallet balances via Blockfrost.

## MCP Tools

- `get_steelswap_tokens` — List all tokens available for swapping on SteelSwap
- `get_steelswap_estimate` — Get a swap estimate (price, slippage, route) for a token pair on SteelSwap
- `get_iris_liquidity_pools` — Retrieve liquidity pool data from Iris
- `get_blockfrost_balances` — Get wallet token balances via Blockfrost

## Sub-Skills

- [SteelSwap](sub-skills/steelswap.md) — Token listing and swap estimates
- [Iris Pools](sub-skills/iris-pools.md) — Liquidity pool data from Iris
- [Balances](sub-skills/balances.md) — Wallet balances via Blockfrost

## References

- [MCP Tools Reference](references/mcp-tools.md) — Detailed tool parameters and return types
- [DEX Concepts](references/concepts.md) — SteelSwap, Iris, Blockfrost, price impact, routing

## Example Prompts

- "What tokens are available to swap on SteelSwap?"
- "Get a swap estimate for 100 ADA to iUSD on SteelSwap"
- "Show me the current Iris liquidity pools"
- "What are the token balances for this wallet address?"
