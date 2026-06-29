# OpenClaw Gateway Guardian Failure Modes

This reference is for incident triage and guardian script maintenance.

## Patterns Worth Blocking

### Active work before restart

Evidence:

- `openclaw tasks list --json --status running` has tasks.
- `gateway stability --json` shows recent active/waiting/queued work.
- Logs contain `draining ... active task(s)` or `active embedded run(s)`.

Action:

- Block restart.
- Wait, cancel deliberately, or ask the user for force.

### Connection surface degraded

Evidence:

- `gateway disconnected: tick timeout`
- `gateway request timeout for connect`
- `handshake-timeout`
- `closed before connect`

Action:

- Split process liveness from WebSocket/RPC readiness.
- Check `gateway status`, `gateway call health`, and logs separately.
- Do not restart repeatedly if status/health are healthy.

### Slow deep RPC

Evidence:

- Log line like `models.list 28917ms`.
- CLI times out while Control UI or a simpler RPC still works.

Action:

- Avoid deep probes as readiness checks.
- Prefer fast `health`/`status` for liveness.
- Capture diagnose report.

### Background cron/model timeout

Evidence:

- `cron: job execution timed out`
- `LLM request timed out`
- `Profile ... timed out`
- `model fallback decision` with `timeout`

Action:

- Treat background maintenance as pressure, not a gateway death signal.
- Delay maintenance or let cooldown/backoff settle.
- Avoid restarting while it is active unless the user accepts interruption.

### Watchdog/reconnect loop

Evidence:

- Reconnects triggered while there is no user traffic.
- Watchdog uses last inbound message instead of connection establishment/activity.

Action:

- Track connection establishment separately from last inbound message.
- Prefer ping/keepalive or last activity, not message-only activity.

## Public Patterns Used As Design Input

- CLI-to-gateway RPC can timeout even when the underlying subsystem is alive.
- Watchdog reconnect logic can make a gateway unresponsive if it treats no inbound messages as inactivity.
- Event-loop pressure, provider latency, channel delivery, and update drift can look identical from the UI.
- The Gateway WebSocket protocol expects a fast first `connect` frame and supports retryable startup-sidecar unavailability; clients should retry within a budget instead of treating every connect delay as terminal.

## Non-Goals

- This skill does not guarantee that upstream model services respond.
- This skill does not provide hostile multi-tenant security.
- This skill does not fix OpenClaw core event-loop bugs by itself.
- This skill does not edit forbidden sqlite files or core config.
