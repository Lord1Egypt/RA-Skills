---
name: indigo-staking
description: "Query and manage INDY token staking positions on Indigo Protocol."
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---

# INDY Staking

Query and manage INDY token staking positions on Indigo Protocol. View staking info, browse positions, and open, adjust, or close staking positions.

## MCP Tools

| Tool | Description |
|------|-------------|
| `get_staking_info` | Get general INDY staking information and parameters |
| `get_staking_positions` | Get all active staking positions |
| `get_staking_positions_by_owner` | Get staking positions for a specific owner |
| `get_staking_position_by_address` | Get a staking position by its address |
| `open_staking_position` | Open a new INDY staking position |
| `adjust_staking_position` | Adjust an existing staking position |
| `close_staking_position` | Close an existing staking position |
| `distribute_staking_rewards` | Distribute pending staking rewards |

## Sub-Skills

- [Staking Queries](sub-skills/staking-query.md) — Query staking info and positions
- [Staking Management](sub-skills/staking-manage.md) — Open, adjust, and close positions
- [Staking Rewards](sub-skills/staking-rewards.md) — Distribute staking rewards

## References

- [MCP Tools Reference](references/mcp-tools.md) — Detailed tool parameters and return types
- [Staking Concepts](references/concepts.md) — INDY staking mechanics, rewards, and governance
