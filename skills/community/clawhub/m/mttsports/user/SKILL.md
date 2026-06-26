---
name: mttsports-user
description: "Use when the task is specifically about `mttsports user`: currently querying the logged-in user's balance. Keep outputs structured and treat this command group as expandable for future user-facing account operations."
---

# mttsports user

When this sub-skill is loaded, the task is already in the `mttsports user` domain.

## Core Rules

1. The user domain currently covers balance lookup only, but the command group should be treated as expandable.
2. Confirm login state before running it, preferably with `mttsports auth status --output json`.
3. Prefer `--output json` so scripts or agents can continue from the result.

## Intent To Command

| 意图 | 推荐命令 | 备注 |
|---|---|---|
| Query the current user's balance | `mttsports user balance --output json` | The only subcommand for now |

## Common Examples

```bash
mttsports auth status --output json
mttsports user balance --output json
```

## Command Schema

### `mttsports user balance`

```json
{
  "address": "0x1234...",
  "balance": "100.5",
  "symbol": "MTT"
}
```

## Notes

1. If the user is not logged in, do not guess the wallet address or balance source. Complete login first.
2. If the user domain expands later, keep `user` as the top-level group instead of folding the commands back into `auth` or `room`.
