---
name: mttsports-session
description: "Use when the task is specifically about `mttsports session`: starting the local daemon, reconnecting the current table, checking status, watching NDJSON events, or sending table actions. Decisions must be made only from `session watch` events, with fast no-thinking-mode behavior and no extra context packing."
---

# mttsports session

When this sub-skill is loaded, the task is already in the `mttsports session` domain.

## Watch Strategy Selection

Choose the watch strategy before doing any OpenClaw-specific setup.

| Agent capability | Action |
|---|---|
| The current agent runtime supports non-blocking background tasks, long-running subprocess supervision, or callback-style event handling | Use the runtime's native background-task capability for `mttsports session watch`. Keep the watch stream alive there, route `turn.changed` back into the active task, and **do not load bootstrap**. |
| The current agent runtime cannot keep `mttsports session watch` alive while the conversation continues, or cannot route callback events by itself | Use the packaged OpenClaw fallback below. Run the availability check and load [`bootstrap/SKILL.md`](bootstrap/SKILL.md) only if the packaged bin is missing. |

Native background support is the preferred path for agent environments such as Claude Code, Codex, or any other runtime that can manage background work directly.

## OpenClaw Fallback Availability Check

Run this section only when the current agent runtime does not support native background watch handling.

**Before starting the OpenClaw fallback router, always check whether the packaged bin already exists:**

```bash
command -v mttsports_watch_in_bg >/dev/null 2>&1 && echo "READY" || echo "MISSING"
```

| Result | Action |
|---|---|
| `READY` | Use `mttsports_watch_in_bg` directly. **Do not load bootstrap.** |
| `MISSING` | Read [`bootstrap/SKILL.md`](bootstrap/SKILL.md), verify installation, then continue |

## Launch Verification And Approval Handling

Every watch launch must be verified. Never assume the watcher is active just because a command was issued.

1. If the environment requires user approval to launch the watcher, and that approval is denied, times out, or never appears to the user, stop immediately and tell the user the watcher is not running.
2. If the watch launch command exits with an error, do not retry silently. Surface the exact failure mode to the user and explain whether approval, credentials, or runtime support is missing.
3. After launching a background watcher, confirm readiness within a short timeout using the runtime's own task status, PID check, or startup log.
4. If readiness confirmation fails, tell the user that `mttsports session watch` is not active yet and that no autonomous action loop is running.

## Core Rules

1. `mttsports session start` is the only entry point for the daemon and websocket lifecycle.
2. `watch`, `operate`, `status`, and `stop` all depend on the local daemon.
3. `mttsports session watch` is machine-facing NDJSON. Do not mix explanatory text into stdout.
4. Decisions must come only from `mttsports session watch` events. Do not append extra room history, summaries, or manually packed context.
5. **Do not run `mttsports session watch` as a blocking foreground command.** Use the agent's native background-task support when available. Use the packaged `mttsports_watch_in_bg` bin only for the OpenClaw fallback path.
6. Only fetch the OpenClaw session ID and use `mttsports_watch_in_bg` when the fallback path is actually needed. If `--session-id` is omitted, the packaged bin resolves the latest OpenClaw session automatically.
7. Use no-thinking mode for decisions: act quickly and do not emit long reasoning.
8. Before sending an action, make sure the daemon is running and the table context is known.
9. If the daemon is unhealthy, return to `mttsports session start`. Do not patch the websocket connection manually.
10. During continuous automated play, execute decisions directly by default instead of asking hand by hand.
11. Strategy boundaries and interaction style come from the shared rules in [`../SKILL.md`](../SKILL.md). `session` only covers execution-stage constraints.
12. If the watch event shows the current user as `managed=true`, treat it as a managed-recovery state first. Do not continue normal in-hand action flow until managed mode is cleared.
13. If the watcher failed to launch because approval was required and not granted, notify the user immediately instead of pretending the automation loop is live.

## Intent To Command

| Intent | Recommended Command | Notes |
|---|---|---|
| Start or restart the local session daemon | `mttsports session start ... --output json` | Restarts if a daemon already exists |
| Reconnect the current table inside the current daemon | `mttsports session reconnect --output json` | No daemon restart, watch stays alive |
| Check daemon status | `mttsports session status --output json` | Preferred before sending actions |
| Start the watch stream in the background | Native runtime-managed `mttsports session watch`, or `mttsports_watch_in_bg --channel ... --target ... [--session-id ...]` for the OpenClaw fallback | Prefer native background task support; run the availability check first only for the fallback path |
| Send a table action | `mttsports session operate <action> ... --output json` | Must be decided from the current `watch` event only |
| Stop the watch stream | Use the runtime's task stop or cancel flow, or `kill -TERM $(cat <pid_file_from_launch_result>)` for the OpenClaw fallback | Match the stop method to the chosen watch strategy |
| Stop the daemon | `mttsports session stop --output json` | Ends the local connection lifecycle |

## Common Examples

```bash
# Start the daemon
mttsports session start --room-key <room_key> --table-key <table_key> --table-server-id <id> --session-token <token> --output json

# Reconnect the table while the daemon is still online
mttsports session reconnect --output json

# Check status
mttsports session status --output json
```

### Preferred Example: Native Background Task Support

If the current agent runtime can supervise background work directly, keep `mttsports session watch` alive with that native mechanism and route only the watch events back into the active task.

Readiness requirements:

1. Start the watch command as a non-blocking managed background task.
2. Confirm the background task is alive before assuming the loop is active.
3. If launch approval is required and not granted, tell the user the watch loop did not start.

### OpenClaw Fallback Example

Use this only when native background support is not available.

```bash

# Start the packaged watch router in the background
# Confirm availability first; see "OpenClaw Fallback Availability Check" above
OPENCLAW_SESSION_ID=$(openclaw sessions list --limit 1 --output json | python3 -c "import sys,json; print(json.load(sys.stdin)['results'][0]['sessionId'])")

mttsports_watch_in_bg \
  --session-id "$OPENCLAW_SESSION_ID" \
  --channel discord \
  --target "channel:<id>"

# Send actions after Claude receives turn.changed
mttsports session operate raise --table-key <table_key> --amount 400 --output json
mttsports session operate insurance buy --table-key <table_key> --pod 1:1000:400 --pod 2:600:200 --output json

# Stop the OpenClaw fallback watch router
kill -TERM $(cat /path/from/pid_file)

# Stop the daemon
mttsports session stop --output json
```

The packaged launcher prints JSON with `pid`, `pid_file`, and `log_file`. If readiness confirmation fails, or the launcher exits with an approval-related or install-related error, tell the user the watcher is not active and inspect the `log_file`.

## Command Schema

### `mttsports session start` / `mttsports session status`

```json
{
  "ok": true,
  "schema": "session.status",
  "session_id": "session_xxx",
  "payload": {
    "room_key": "room_xxx",
    "table_key": "table_xxx"
  }
}
```

### `mttsports session reconnect`

```json
{
  "ok": true,
  "schema": "session.status",
  "session_id": "session_xxx",
  "payload": {
    "room_key": "room_xxx",
    "table_key": "table_xxx"
  }
}
```

### `mttsports session watch`

```json
{
  "schema": "table.event",
  "type": "turn.changed",
  "ts": "2026-04-02T12:34:56Z",
  "seq": 123,
  "room_key": "room_xxx",
  "table_key": "table_xxx",
  "turn_changed": {}
}
```

Use only the current `watch` event when deciding. Do not append extra background or long reasoning.

## Currently Supported Watch Events

Only two push event types are currently used for in-hand decision making:

### `turn.changed`

Source: `NotifyOperateStart`, and it is emitted to `watch` only when `IsSelf=true`.

Purpose: it means it is now your turn to act. This is the primary decision event.

Additional interpretation:

- `turn.stage_histories` / `turn.stageHistories` contains the action history for each stage in the current hand.
- Within each stage, `user_op_results` / `userOpResults` is ordered chronologically.
- The last item is the latest known action.
- Prefer using that recent action history together with the chip constraints instead of looking only at `options`.

Key fields:

```json
{
  "schema": "table.event",
  "type": "turn.changed",
  "room_key": "room_xxx",
  "table_key": "table_xxx",
  "turn_changed": {
    "turn": {
      "user_id": 12345,
      "options": ["fold", "check", "call", "raise", "allin"],
      "min_call_chip": "2",
      "min_raise_chip": "4",
      "max_raise_chip": "200",
      "last_greatest_raise_chip": "4",
      "time_ms": 15000,
      "extra_time_ms": 0,
      "total_op_time_ms": 15000,
      "is_self": true,
      "seq": 123,
      "desc": "operate_start",
      "stage_histories": [
        {
          "round_stage": "pre_flop",
          "user_op_results": [
            {
              "user_id": 12345,
              "action": "blind",
              "chip": "1"
            },
            {
              "user_id": 67890,
              "action": "raise",
              "chip": "4"
            }
          ]
        }
      ]
    },
    "round": {
      "id": 888,
      "stage": "pre_flop",
      "public_cards": []
    },
    "pod": {
      "total_chip": "6",
      "min_raise_chip": "4",
      "min_call_chip": "2"
    }
  }
}
```

The event itself is not the action. After receiving `turn.changed`, call the matching `mttsports session operate` subcommand:

- `fold` -> `mttsports session operate fold`
- `check` -> `mttsports session operate check`
- `call` -> `mttsports session operate call`
- `bet` -> `mttsports session operate bet --amount ...`
- `raise` -> `mttsports session operate raise --amount ...`
- `allin` -> `mttsports session operate allin`

If `stage_histories` is present:

1. Check the last `user_op_results` item in the current stage first and treat it as the latest opponent action.
2. Evaluate that action together with `min_call_chip`, `min_raise_chip`, and `last_greatest_raise_chip` instead of relying only on the available button options.

### `round.result`

Source: `NotifyRoundResult`.

Purpose: the current hand has finished settling. Do not send more actions for this hand. Wait for the next `turn.changed`.

Key fields:

```json
{
  "schema": "table.event",
  "type": "round.result",
  "room_key": "room_xxx",
  "table_key": "table_xxx",
  "round_result": {
    "round": {
      "public_cards": ["Ah", "Kd", "7c", "2s", "2d"],
      "quick_end": false
    },
    "self_result": {
      "user_id": 12345,
      "chip": "120",
      "win_round": true,
      "change_chip": "+18",
      "change_type": "win",
      "card_type": "two_pair"
    }
  }
}
```

When this event arrives:

1. Treat the current round as finished.
2. Do not send any more `operate` actions for this hand.
3. Keep `watch` running and wait for the next `turn.changed`.

## Non-Decision Events

`watch` may also emit a small set of non-decision events. These should not drive table actions:

- `session.opened`: session established successfully
- `table.snapshot`: full-table snapshot after reconnect
- `error`: session or call error
- `session.closing`: session is closing

These events are for connection-state awareness, not in-hand action decisions.

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

### `mttsports session stop`

```json
{
  "ok": true,
  "payload": {
    "stopping": true
  }
}
```

## Notes

1. Action decisions must come only from `session watch` events. Do not stuff room history, extra summaries, or manually added context into the decision input.
2. Keep decisions fast. Avoid long reasoning and context expansion.
3. `bet`, `raise`, and `insurance buy` may only use legal parameters that are already present in the event payload or command help.
4. The `--pod` format for `operate insurance buy` is `<pod_id>:<chips>:<premium>`.
5. `session reconnect` is only for cases where the daemon is still online but the table state needs to be resynced. If the daemon is offline, use `session start` instead.
6. If the goal is continuous play instead of a single operation, go back to the "Autonomous Play" and "Autonomous Strategy" sections in [`../SKILL.md`](../SKILL.md).
7. If the current user is still `managed=true`, run `mttsports session operate stop-managed --output json` first, then wait for the next watch event or refreshed snapshot before resuming normal actions.

## References

- [`references/lifecycle.md`](references/lifecycle.md) - `start/reconnect/status/stop` and the daemon lifecycle
- [`references/watch.md`](references/watch.md) - `session watch` event schema, decision events, and non-decision events
- [`references/operate.md`](references/operate.md) - `session operate` commands, parameters, and constraints
