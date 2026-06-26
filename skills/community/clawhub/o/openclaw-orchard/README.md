# OrchardOS — OpenClaw Plugin

Agentic project and task management for OpenClaw.

## Features
- SQLite-backed task board (projects → tasks → runs → comments)
- REST API at `/orchard/projects`, `/orchard/tasks`
- Agent tools: `orchard_task_add`, `orchard_task_list`, `orchard_task_done`, `orchard_task_block`, `orchard_task_comment`, `orchard_wake`
- Queue runner: auto-dispatches `ready` tasks as subagents
- Web dashboard at `/orchard/ui`

## Install

```bash
openclaw plugins install clawhub:openclaw-orchard
openclaw gateway restart
```

## Config (optional)

Orchard works as an OpenClaw plugin once installed and enabled. Configure the `orchard` plugin entry in `openclaw.json` only if you want to tune behavior such as:

- `dbPath`
- debug/safe-mode flags
- concurrency and task-rate limits
- executor / architect / reporter role settings
- queue cadence (`queueIntervalMs`)
- context injection
- standalone UI server settings

## Debug / safe mode

If Orchard is jamming the system, start with a non-spawning mode.

### Local env override mode

For local debugging, Orchard supports optional environment-variable overrides. These are convenience/debug controls, not required credentials.

Supported env vars:
- `ORCHARD_DEBUG`
- `ORCHARD_DEBUG_VERBOSE`
- `ORCHARD_DEBUG_LOG_ONLY`
- `ORCHARD_DEBUG_DRY_RUN`
- `ORCHARD_DISABLE_ALL_SPAWNS`
- `ORCHARD_DISABLE_EXECUTOR_SPAWNS`
- `ORCHARD_DISABLE_QA_SPAWNS`
- `ORCHARD_DISABLE_ARCHITECT_SPAWNS`
- `ORCHARD_PRESERVE_SESSIONS`
- `ORCHARD_CIRCUIT_BREAKER_ENABLED`
- `ORCHARD_CIRCUIT_BREAKER_FAILURE_THRESHOLD`
- `ORCHARD_CIRCUIT_BREAKER_COOLDOWN_MS`
- `ORCHARD_QUEUE_INTERVAL_MS`
- `ORCHARD_DB_PATH`

Example local shell setup:

```bash
export ORCHARD_DEBUG=1
export ORCHARD_DEBUG_VERBOSE=1
export ORCHARD_DEBUG_LOG_ONLY=1
export ORCHARD_PRESERVE_SESSIONS=1
export ORCHARD_DISABLE_ARCHITECT_SPAWNS=1
export ORCHARD_QUEUE_INTERVAL_MS=900000
openclaw gateway restart
```

A sample file is included at `orchard/.env.example`.
More local-debug guidance lives in `orchard/docs/local-debugging.md`.

If Orchard is jamming the system, start with a non-spawning mode:

```json
{
  "plugins": {
    "entries": {
      "orchard": {
        "config": {
          "debug": {
            "enabled": true,
            "verbose": true,
            "logOnly": true,
            "preserveSessions": true
          }
        }
      }
    }
  }
}
```

Useful flags:
- `debug.logOnly`: record dispatches and runs, but do not spawn executor/QA/architect subagents
- `debug.disableExecutorSpawns`: let Orchard operate, but suppress executor spawns only
- `debug.disableQaSpawns`: skip QA subagents
- `debug.disableArchitectSpawns`: stop empty-queue and scheduled architect wakeups
- `debug.disableAllSpawns`: hard stop on all Orchard-originated spawns
- `debug.verbose`: emit extra queue/dispatch diagnostics to logs
- `debug.preserveSessions`: keep spawned sessions around for inspection instead of deleting them immediately
- `debug.circuitBreaker.enabled`: stop repeated failure storms automatically
- `debug.circuitBreaker.failureThreshold`: open the breaker after N failures
- `debug.circuitBreaker.cooldownMs`: how long to pause dispatch after opening the breaker
+
Debug API:
- `GET /orchard/debug/state` returns live queue state, debug flags, queue pause state, and circuit-breaker status
- `POST /orchard/debug/control` supports `pauseQueue`, `resumeQueue`, `openCircuit`, `closeCircuit`, `resetCircuit`, and `tickProject`

Recommended recovery profile while debugging:
- turn `debug.enabled: true`
- turn `debug.logOnly: true`
- set `roles.architect.enabled: false`
- optionally raise `queueIntervalMs` so Orchard ticks less aggressively

## Agent tools

Use these directly inside any OpenClaw agent session:

- `orchard_task_add` — add a task to a project
- `orchard_task_list` — list tasks (filter by project_id, status)
- `orchard_task_done` — mark task done with summary
- `orchard_task_block` — mark task blocked with reason
- `orchard_task_comment` — add a comment to a task
- `orchard_wake` — trigger queue runner immediately

## UI access

### Local machine

Use the standalone Orchard UI server:

- `http://127.0.0.1:18790/`
- `http://localhost:18790/`

Do **not** use the main gateway UI path for normal Orchard browsing.
The gateway routes under port `18789` require a bearer token and are mainly for API access.

Security note:
- the standalone UI server is safest on `127.0.0.1`
- it forwards the browser's `Authorization` header to the local OpenClaw gateway
- non-loopback binds are refused unless `uiServer.allowUnsafeBind: true` is set explicitly
- do not widen `uiServer.bindAddress` unless you intentionally want LAN exposure and understand the tradeoff

### Remote machine over SSH tunnel

If Orchard is running on another machine, forward the standalone UI port locally:

```bash
ssh -N -L 18790:127.0.0.1:18790 <user>@<host>
```

Example:

```bash
ssh -N -L 18790:127.0.0.1:18790 leo@10.50.0.10
```

Then open:

- `http://127.0.0.1:18790/`
- `http://localhost:18790/`

### API access

Orchard API routes on the main gateway use the standard OpenClaw bearer-token auth model.

Examples:
- `http://127.0.0.1:18789/orchard/projects`
- `http://127.0.0.1:18789/orchard/debug/state`

### Standalone UI smoke check

A focused end-to-end smoke check for the standalone UI is included:

```bash
cd /home/leo/.openclaw/workspace/orchard
npm run smoke:standalone-ui
```

Optional overrides:

```bash
npm run smoke:standalone-ui -- --token <gateway-token>
npm run smoke:standalone-ui -- --base-url http://10.50.0.10:18790 --token <gateway-token>
```

The smoke check verifies:
- standalone HTML shell loads
- no gateway token is embedded into the served HTML
- token-entry/localStorage auth flow is present
- unauthenticated `/orchard/projects` is rejected with 401
- authenticated fetches to projects, project detail, tasks, task detail, runs, activity, and settings succeed through the standalone proxy
- live Orchard data is available for sidebar project list, progress bars, board columns, session pill counts, and refresh hooks

## REST API

All routes require `Authorization: Bearer <gateway-token>`.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/orchard/projects` | List projects |
| POST | `/orchard/projects` | Create project |
| GET | `/orchard/projects/:id/tasks` | List tasks |
| POST | `/orchard/projects/:id/tasks` | Add task |
| GET | `/orchard/tasks/:id` | Get task |
| PUT | `/orchard/tasks/:id` | Update task |
| POST | `/orchard/tasks/:id/comments` | Add comment |
| GET | `/orchard/tasks/:id/runs` | Get run history |
| POST | `/orchard/wake` | Trigger queue runner |
```
