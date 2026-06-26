# openclaw.session_cleanup_v1

## Overview

Stabilize OpenClaw instances that degrade after long runtimes because sessions, agents, browser control workers, and websocket connections are not reclaimed aggressively enough.

## Diagnose

Treat the following signals as the main trigger pattern:

- `Sessions: 16 active` or any value above 10 on a small VPS
- `Agents: 6` or higher on a 1 vCPU / 2 GB host
- `browser control service timeout`
- `gateway 1006 abnormal closure`

Interpretation:

- stale agent sessions are not being reclaimed
- browser instances remain alive too long
- gateway websocket pressure keeps increasing
- the runtime is operating past the safe memory envelope

## Immediate Actions

Run:

```bash
openclaw sessions
openclaw sessions prune
openclaw status
```

If the runtime is still unhealthy, escalate to:

```bash
openclaw sessions clear
openclaw status
```

Target after cleanup:

- sessions: `1-3`
- gateway: reachable
- browser: healthy

## Runtime Guardrails

For a `1 vCPU / 2 GB RAM` machine, use these defaults:

- sessions: `<= 5`
- session TTL: `30m`
- agents: `3`
- browser instances: `1`
- swap: `2G`

Example runtime config:

```json
{
  "runtime": {
    "maxSessions": 5,
    "sessionTTL": "30m",
    "maxAgents": 3,
    "maxBrowsers": 1
  }
}
```

## Automation

Install a periodic prune job:

```cron
*/30 * * * * openclaw sessions prune >/dev/null 2>&1
```

Meaning:

- every 30 minutes, remove inactive sessions

## Browser Constraints

Treat browser control as the heaviest resource consumer on small hosts.

Recommended launch mode:

```bash
openclaw browser start --single
```

## Swap

If the VPS has no swap, add `2G`:

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
free -h
```

Confirm that `Swap` reports `2G`.

## Watchdog

Use a systemd probe to restart the gateway when it stops responding.

Service template:

```ini
[Unit]
Description=Restart OpenClaw if gateway unreachable

[Service]
Type=oneshot
ExecStart=/usr/bin/openclaw gateway probe || /usr/bin/systemctl restart openclaw-gateway
```

Timer template:

```ini
[Timer]
OnBootSec=5m
OnUnitActiveSec=10m

[Install]
WantedBy=timers.target
```

## Stability Targets

Healthy steady state on a small VPS:

- `Sessions: 1-3`
- `Agents: 3`
- `Gateway reachable`
- `browser running`
- `Memory store: stable`

## Decision Policy

Use this sequence:

1. Prune stale sessions first.
2. Reduce session and agent ceilings.
3. Enforce single-browser mode.
4. Add swap if absent.
5. Install watchdog only after runtime limits are in place.

## Packaged Files

- [`templates/openclaw.json`](../templates/openclaw.json): starting runtime config
- [`templates/openclaw-watchdog.service`](../templates/openclaw-watchdog.service): systemd service unit
- [`templates/openclaw-watchdog.timer`](../templates/openclaw-watchdog.timer): systemd timer unit
- [`scripts/install-cron-prune.sh`](../scripts/install-cron-prune.sh): cron installer
- [`scripts/install-watchdog.sh`](../scripts/install-watchdog.sh): watchdog installer
- [`scripts/render-openclaw-config.sh`](../scripts/render-openclaw-config.sh): config renderer
