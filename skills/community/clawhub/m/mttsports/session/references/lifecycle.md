# session lifecycle

## Scope

Use this reference for `mttsports session start/reconnect/status/stop` and the daemon plus websocket lifecycle.

## Core Rules

1. `mttsports session start` is the only entry point for the daemon and websocket lifecycle.
2. `watch`, `operate`, `status`, and `stop` all depend on the local daemon.
3. If a daemon already exists, a new `start` call should be treated as a new lifecycle: stop the old daemon first, then start a new one.
4. `mttsports session reconnect` triggers a table reconnect inside the current daemon without restarting it.
5. Use `session reconnect` only when the daemon is still online and the table state needs resynchronization.
6. If the daemon is unhealthy or the transport is disconnected, return to `mttsports session start` instead of rebuilding the websocket manually.

## Intent To Command

| Intent | Recommended Command | Notes |
|---|---|---|
| Start or restart the local session daemon | `mttsports session start ... --output json` | Restarts if a daemon already exists |
| Reconnect the current table | `mttsports session reconnect --output json` | Reconnects inside the current daemon without interrupting watch |
| Check daemon status | `mttsports session status --output json` | Preferred before sending actions |
| Stop the daemon | `mttsports session stop --output json` | Ends the local connection lifecycle |

## Common Examples

```bash
mttsports session start --room-key <room_key> --table-key <table_key> --table-server-id <id> --session-token <token> --output json
mttsports session reconnect --output json
mttsports session status --output json
mttsports session stop --output json
```

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

1. Before startup, make sure `room_key`, `table_key`, and `table_server_id` are all known.
2. `session reconnect` does not restart the daemon, so an existing `session watch` subscription should not be interrupted.
3. If the current daemon is offline, `session reconnect` is not appropriate. Use `session start` instead.
4. For decision-making next, move to [`watch.md`](watch.md).
5. For sending actions next, move to [`operate.md`](operate.md).
