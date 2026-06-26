# session operate

## Scope

Use this reference for `mttsports session operate` commands, parameters, and valid value sources.

## Core Rules

1. Before sending any action, make sure the daemon is running and the table context is known.
2. Actions must be chosen from the current `watch` event only.
3. `bet`, `raise`, and `insurance buy` may only use legal parameters explicitly shown in the event payload or command help.
4. Keep responses minimal. Do not narrate the hand.

## Intent To Command

| Action | Recommended Command | Notes |
|---|---|---|
| Fold | `mttsports session operate fold --output json` | Direct action |
| Check | `mttsports session operate check --output json` | Direct action |
| Call | `mttsports session operate call --output json` | Direct action |
| Bet | `mttsports session operate bet --amount ... --output json` | Amount must be legal |
| Raise | `mttsports session operate raise --amount ... --output json` | Amount must be legal |
| All-in | `mttsports session operate allin --output json` | High-risk action |
| Buy insurance | `mttsports session operate insurance buy --pod ... --output json` | `--pod` format is fixed |

## Common Examples

```bash
mttsports session operate fold --output json
mttsports session operate check --output json
mttsports session operate call --output json
mttsports session operate raise --amount 400 --output json
mttsports session operate insurance buy --pod 1:1000:400 --pod 2:600:200 --output json
```

## Command Schema

### `mttsports session operate ...`

```json
{
  "ok": true,
  "accepted": true,
  "action_id": "action_xxx",
  "request_id": "req_xxx",
  "server_seq": 124,
  "payload": {},
  "error": ""
}
```

## Action Source

After receiving `turn.changed` from [`watch.md`](watch.md), pick the action from the event's `options`:

- `fold` -> `mttsports session operate fold`
- `check` -> `mttsports session operate check`
- `call` -> `mttsports session operate call`
- `bet` -> `mttsports session operate bet --amount ...`
- `raise` -> `mttsports session operate raise --amount ...`
- `allin` -> `mttsports session operate allin`

## Notes

1. The `--pod` format for `operate insurance buy` is `<pod_id>:<chips>:<premium>`.
2. If there is no clear `turn.changed` event or no valid `options`, do not send an action blindly.
3. If amount bounds are unclear, go back to [`watch.md`](watch.md) and inspect `min_call_chip`, `min_raise_chip`, and `max_raise_chip`.
