---
name: a2a-server
description: 'Run an A2A inbound task listener that lets this OpenClaw instance receive tasks from other agents via the A2A API Gateway. Use when: (1) starting/stopping the A2A listener service, (2) receiving inbound A2A tasks from other agents, (3) checking if the listener is running. NOT for: sending tasks outbound (use a2a-client), registering this agent (use a2a-register).'
metadata: {"clawdbot":{"emoji":"📡","requires":{"anyBins":["python3"]},"os":["linux","darwin"]}}
---

# A2A Server — Inbound Task Listener

Run an A2A protocol listener that allows this OpenClaw instance to receive tasks routed from the A2A API Gateway. The listener runs as a background HTTP service.

## Sidecar Principle

This skill is strictly an **OpenClaw sidecar** — it receives tasks FROM the A2A API Gateway in whatever format the gateway sends them. The gateway's A2A protocol is the contract; OpenClaw's listener just speaks it. Never assume what the sending system looks like — it could be any agent that routes tasks through the gateway. The listener implements the gateway's expected endpoints as-is.

## Configuration

The listener reads configuration from a shared `a2a.conf` file (located in the `a2a-client` skill directory), with auto-detection fallbacks for local settings.

**Priority order:** CLI flags → env vars → `a2a.conf` → auto-detected defaults

| Setting | Auto-detected Default | Description |
|---------|-----------------------|-------------|
| Port | `8100` | Listen port (`LISTENER_PORT`) |
| Bind Address | Tailscale IP or first NIC | Local bind address (`BIND_ADDR`) |
| Agent Slug | `hostname -s` (lowercase) | Agent identifier (`AGENT_SLUG`) |
| Agent Name | Slug (capitalized) | Display name (`AGENT_NAME`) |
| Agent URL | `http://{bind_addr}:{port}` | Agent endpoint (`AGENT_URL`) |
| Capabilities | `chat,code,research` | Comma-separated (`AGENT_CAPABILITIES`) |
| Auth Type | `bearer` | Auth method (`AGENT_AUTH_TYPE`) |
| API Key | *empty* | Bearer token — **if empty, auth checks are disabled** (`A2A_GATEWAY_API_KEY`) |
| OpenClaw Command | *auto* | Shell command template; `{message}` and `{session_id}` placeholders (`A2A_OPENCLAW_COMMAND`) |
| OpenClaw URL | *empty* | HTTP API URL for chat completions (`A2A_OPENCLAW_URL`) |
| OpenClaw URL API Key | *empty* | Bearer token for HTTP API (`A2A_OPENCLAW_URL_API_KEY`) |
| OpenClaw Timeout | `60` | Max seconds to wait for response (`A2A_OPENCLAW_TIMEOUT`) |

Run `a2a-register/a2a-setup.sh` to configure interactively, or set env vars / create `a2a-client/a2a.conf`.

## When to Use

- **Start the listener** — When this OpenClaw instance needs to receive inbound A2A tasks
- **Stop the listener** — When shutting down or pausing inbound task reception
- **Check listener status** — When verifying the A2A service is running

## Endpoints

The listener (`a2a-listener.py`) handles these routes:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check — returns `{"status": "ok", "agent": "<slug>"}` |
| `GET` | `/v1/a2a/agents/{slug}` | Returns the agent card for this OpenClaw instance |
| `POST` | `/v1/a2a/tasks/send` | Receives an inbound A2A task (requires Bearer auth if API key is set) |

## Auth

Inbound tasks (`POST /v1/a2a/tasks/send`) require a Bearer token matching the configured `A2A_GATEWAY_API_KEY`. If no API key is configured, auth checks are disabled (with a warning at startup). Health checks and agent card lookups are unauthenticated.

## Tools

### start.sh — Start the Listener

```bash
./start.sh [--port PORT] [--bind ADDR]
```

Starts the A2A listener in the background. All other settings are read from `a2a.conf` or env vars.

```bash
# Start with defaults (from a2a.conf or auto-detected)
./start.sh

# Custom port and bind address
./start.sh --port 8200 --bind 0.0.0.0
```

Saves the PID to `a2a-listener.pid` for management. Logs to `a2a-listener.log`.

### stop.sh — Stop the Listener

```bash
./stop.sh
```

Gracefully stops the A2A listener using the PID file.

### a2a-listener.py — The Listener Process

Python HTTP server that implements the A2A protocol endpoints. Started by `start.sh`. Can also be run directly:

```bash
# Run directly (foreground)
python3 a2a-listener.py

# With custom settings via env vars
LISTENER_PORT=8200 BIND_ADDR=0.0.0.0 A2A_GATEWAY_API_KEY=your-key python3 a2a-listener.py
```

All configuration is loaded from `a2a.conf`, env vars, or auto-detected — no hardcoded values.

## OpenClaw Invocation — Real Responses

When an inbound task arrives, the listener invokes the local OpenClaw instance to produce a real response. The invocation method is configurable, with automatic fallback:

**Priority:** `A2A_OPENCLAW_COMMAND` → `A2A_OPENCLAW_URL` → auto-detect `openclaw` CLI → error

| Env Var | Description | Example |
|---------|-------------|--------|
| `A2A_OPENCLAW_COMMAND` | Shell command template; `{message}` and `{session_id}` are replaced | `openclaw agent -m "{message}" --session-id {session_id} --json` |
| `A2A_OPENCLAW_URL` | HTTP API URL to POST the task to | (any HTTP chat/completions endpoint) |
| `A2A_OPENCLAW_URL_API_KEY` | Bearer token for the HTTP URL | (optional, only used with `A2A_OPENCLAW_URL`) |
| `A2A_OPENCLAW_TIMEOUT` | Max seconds to wait for a response | `60` (default) |

### Auto-Detection

If neither `A2A_OPENCLAW_COMMAND` nor `A2A_OPENCLAW_URL` is set, the listener checks if the `openclaw` CLI is on `PATH`. If found, it runs:

```bash
openclaw agent -m "<message>" --session-id <session_id> --json
```

This uses OpenClaw's built-in agent runtime and returns real AI responses. The `--session-id` flag ensures continuity within a conversation thread.

### Response Format

On success:
```json
{"id": "task-123", "status": "completed", "result": {"kind": "text", "content": "<actual AI response>"}}
```

On failure (invocation error, timeout, etc.):
```json
{"id": "task-123", "status": "failed", "result": {"kind": "text", "content": "<error message>"}}
```

### Configuration Error

If no invocation method is available at all, the task response will have `status: "failed"` with a message explaining how to configure OpenClaw access.

## Typical Workflow

1. **Configure** → Run `a2a-register/a2a-setup.sh` or create `a2a.conf`
2. **Register** → Use the `a2a-register` skill to register this instance in the A2A API Gateway
3. **Start** → `./start.sh` to begin listening for inbound tasks
4. **Verify** → `curl http://YOUR_IP:8100/health` to confirm it's running
5. **Receive** — The gateway routes tasks to this listener automatically
6. **Stop** → `./stop.sh` when done
