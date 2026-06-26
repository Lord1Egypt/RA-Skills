---
name: indigo-cdp
description: "Manage Collateralized Debt Positions (CDPs) on the Indigo Protocol."
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---

# Indigo CDP & Loan Management

Manage Collateralized Debt Positions (CDPs) on the Indigo Protocol.

## Prerequisites

- `@indigoprotocol/indigo-mcp` server running

## MCP Tools

- `open_cdp` — Open a new CDP
- `deposit_cdp` — Deposit collateral into a CDP
- `withdraw_cdp` — Withdraw collateral from a CDP
- `close_cdp` — Close a CDP and reclaim collateral
- `mint_cdp` — Mint iAssets against a CDP
- `burn_cdp` — Burn iAssets to reduce CDP debt
- `analyze_cdp_health` — Check CDP health and liquidation risk
- `liquidate_cdp` — Liquidate an unhealthy CDP
- `redeem_cdp` — Redeem iAssets against a CDP
- `freeze_cdp` — Freeze a CDP
- `merge_cdps` — Merge multiple CDPs into one
- `leverage_cdp` — Open a leveraged CDP position via ROB
- `get_all_cdps` — List all CDPs
- `get_cdps_by_owner` — List CDPs by owner
- `get_cdps_by_address` — List CDPs by address

## Sub-skills

- [CDP Basics](sub-skills/cdp-basics.md) — Open, deposit, withdraw, close
- [Mint & Burn](sub-skills/cdp-mint-burn.md) — Mint and burn iAssets
- [CDP Health](sub-skills/cdp-health.md) — Analyze health, liquidation risk
- [Liquidation](sub-skills/cdp-liquidation.md) — Liquidate, redeem, freeze, merge
- [Leverage](sub-skills/cdp-leverage.md) — Leveraged CDP via ROB

## References

- [MCP Tools Reference](references/mcp-tools.md) — Detailed tool parameters and return types
- [CDP Concepts](references/concepts.md) — Collateral ratios, liquidation, iAssets, and more
