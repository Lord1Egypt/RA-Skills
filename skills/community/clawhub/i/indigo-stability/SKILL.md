---
name: indigo-stability
description: "Manage Stability Pool positions on the Indigo Protocol."
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---

# Indigo Stability Pools

Manage Stability Pool positions on the Indigo Protocol.

## Prerequisites

- `@indigoprotocol/indigo-mcp` server running

## MCP Tools

- `get_stability_pools` — List all stability pools
- `get_stability_pool_accounts` — List accounts in a stability pool
- `get_sp_account_by_owner` — Get stability pool account by owner
- `create_sp_account` — Create a new stability pool account
- `adjust_sp_account` — Adjust deposit in a stability pool account
- `close_sp_account` — Close a stability pool account
- `process_sp_request` — Process a pending stability pool request
- `annul_sp_request` — Cancel a pending stability pool request

## Sub-skills

- [Pool Queries](sub-skills/sp-query.md) — Pool state, accounts, owner lookup
- [Pool Management](sub-skills/sp-manage.md) — Create, adjust, close accounts
- [Request Processing](sub-skills/sp-requests.md) — Process and cancel requests

## References

- [MCP Tools Reference](references/mcp-tools.md) — Detailed tool parameters and return types
- [Stability Pool Concepts](references/concepts.md) — Pool mechanics, rewards, and request lifecycle
