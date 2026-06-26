---
name: looloo-discovery
description: Use this skill when the user wants to discover new LooLoo tokens, inspect token activity, or review current positions from OpenClaw.
---

# LooLoo Discovery

Use the bundled `openclaw-looloo` plugin tools instead of calling the raw API directly.

## Use this skill for

- scanning new internal-market tokens
- reviewing one token's recent trades and top holders
- checking the authenticated wallet's current positions

## Workflow

1. Call `discover_new_tokens` for a market-wide scan.
2. If the user narrows to one token, call `get_token_summary`.
3. If the user asks about their wallet, call `get_positions`.
4. Summarize the strongest signals briefly and keep raw JSON available if needed.

## Notes

- Phase 1 only supports the `internal` market.
- OpenClaw should return notifications through the user's existing chat channel.
- Do not imply guaranteed profits; frame results as discovery and execution support.
