---
name: indigo-redemption
description: "Manage redemptions and Redemption Order Book (ROB) positions on Indigo Protocol."
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---

# Indigo Redemption & ROB

Skill for managing redemptions and Redemption Order Book (ROB) positions on Indigo Protocol.

## Prerequisites

- Node.js 20+
- `@indigoprotocol/indigo-mcp` server running

## MCP Server

```bash
npx @indigoprotocol/indigo-mcp
```

## Tools

| Tool | Description |
|------|-------------|
| `get_order_book` | Get open ROB positions from the order book, optionally filtered by asset or owners |
| `get_redemption_orders` | Get redemption orders, optionally filtered by timestamp or price range |
| `get_redemption_queue` | Get aggregated redemption queue for a specific iAsset, sorted by max price ascending |
| `open_rob` | Open a new ROB position with ADA and a max price limit |
| `cancel_rob` | Cancel an existing ROB position |
| `adjust_rob` | Adjust ADA amount in an ROB position; optionally update max price |
| `claim_rob` | Claim received iAssets from an ROB position |
| `redeem_rob` | Redeem iAssets against one or more ROB positions |

## Sub-skills

- [Order Book](sub-skills/order-book.md) — Query ROB order book and redemption orders
- [Redemption Queue](sub-skills/redemption-queue.md) — Aggregated redemption queue per iAsset
- [ROB Management](sub-skills/rob-manage.md) — Open, cancel, adjust, claim, and redeem ROB positions

## References

- [MCP Tools Reference](references/mcp-tools.md) — Detailed tool parameters and return types
- [Redemption Concepts](references/concepts.md) — ROB mechanics, order book, and redemption queue
