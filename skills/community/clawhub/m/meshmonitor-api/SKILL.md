---
name: meshmonitor
description: Use the MeshMonitor REST API to inspect Meshtastic mesh state, nodes, channels, telemetry, messages, traceroutes, packets, solar data, and network-wide stats. Use when the user wants data from a MeshMonitor instance, wants a MeshMonitor-backed dashboard/report, wants help querying mesh history, or wants a reusable MeshMonitor API integration/skill created or updated.
---

# meshmonitor

Use this skill for **MeshMonitor API work**.

## What this skill assumes

- MeshMonitor exposes its REST API at `/api/v1`
- API auth uses a Bearer token
- Swagger docs are usually available at `/api/v1/docs/`
- The installer/user will provide the base URL and token at runtime

## First move

1. Confirm the MeshMonitor base URL.
2. Confirm you have a valid API token.
3. Test auth with a lightweight request before doing anything bigger.

Use the helper script:

```bash
python3 scripts/meshmonitor_api.py --base-url http://HOST:PORT --token 'mm_v1_...' info
```

If auth fails, stop and ask for a fresh token. Do **not** guess token format.

## Supported API areas

This skill is designed to use as much of the API as practical. Prefer these endpoint groups when available:

- `info` → API/version metadata
- `nodes` → list nodes, inspect node, position history
- `channels` → channel configuration
- `telemetry` → telemetry history and summaries
- `messages` → mesh messages/history
- `traceroutes` → route/path history
- `network` → network-wide statistics/topology summaries
- `packets` → raw packet logs
- `solar` → forecast/solar views when enabled

## Workflow

### 1) Validate docs + auth

- Read the live OpenAPI/Swagger if available.
- Run a single authenticated request.
- If docs and live behavior disagree, trust live behavior and note the mismatch.

### 2) Prefer read-heavy discovery first

Before building reports or automation:

- inspect API info
- list nodes
- inspect one known node
- sample messages/telemetry/network endpoints

This tells you which features are populated on the actual instance.

### 3) Produce structured outputs

When the user asks for a report, return concise structured sections such as:

- active nodes
- stale/offline nodes
- recent traffic
- telemetry anomalies
- route findings
- network health

### 4) Be careful with time filters

Many MeshMonitor endpoints are history-oriented. Prefer explicit params like:

- `since`
- `before`
- `limit`
- `active`
- `sinceDays`

When unsure, start with conservative limits.

## Files in this skill

- `references/api-notes.md` → known API groups and verified live behavior notes
- `scripts/meshmonitor_api.py` → helper CLI for authenticated calls, endpoint discovery, message sending, and report generation

Read `references/api-notes.md` when you need a quick endpoint map.

## Helper CLI coverage

The helper now has first-class commands for:

- `info`
- `nodes`
- `node`
- `position-history`
- `channels`
- `channel`
- `telemetry`
- `telemetry-count`
- `telemetry-node`
- `messages`
- `message`
- `send-message`
- `traceroutes`
- `traceroute`
- `network`
- `topology`
- `packets`
- `packet`
- `solar`
- `solar-range`
- `docs`
- `raw`
- `health-summary`
- `node-report`
- `traffic-report`
- `topology-report`

## Recommended usage patterns

### Quick health check

```bash
python3 scripts/meshmonitor_api.py --base-url http://HOST:PORT --token 'TOKEN' health-summary
```

### Inspect a node

```bash
python3 scripts/meshmonitor_api.py --base-url http://HOST:PORT --token 'TOKEN' node-report '!a1b2c3d4'
```

### Browse mesh traffic

```bash
python3 scripts/meshmonitor_api.py --base-url http://HOST:PORT --token 'TOKEN' traffic-report --limit 20
```

### Inspect topology

```bash
python3 scripts/meshmonitor_api.py --base-url http://HOST:PORT --token 'TOKEN' topology-report
```

### Send a message

```bash
python3 scripts/meshmonitor_api.py --base-url http://HOST:PORT --token 'TOKEN' send-message --channel 0 'hello from the API'
```

### Explore live API surface

```bash
python3 scripts/meshmonitor_api.py --base-url http://HOST:PORT --token 'TOKEN' docs
```

## Troubleshooting

### Unauthorized / invalid token

- MeshMonitor tokens are per-user and can be revoked by regeneration.
- Test with the exact bearer token the user provides.
- If the token fails, ask for a fresh token from MeshMonitor user settings.

### Docs page works but API fails

- The docs page is usually public/static.
- The API still requires Bearer auth.
- Verify the `Authorization: Bearer ...` header is present.

### Endpoint exists in docs but returns empty data

That usually means the instance has the feature but no stored data yet. Report that clearly instead of treating it as a hard failure.

## Deliverables this skill is good at

- mesh health summaries
- node inventories
- message/telemetry digests
- troubleshooting whether MQTT / routing / node visibility is working
- reusable scripts or automations that call MeshMonitor cleanly
