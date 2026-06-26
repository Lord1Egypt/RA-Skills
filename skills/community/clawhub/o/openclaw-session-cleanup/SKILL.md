---
name: openclaw-session-cleanup
description: Diagnose and stabilize long-running OpenClaw deployments that accumulate stale sessions, unreaped agents, browser-control timeouts, gateway websocket 1006 closures, or memory pressure on small VPS hosts. Use when OpenClaw shows too many active sessions, browser control service timeout, gateway abnormal closure, or needs a cleanup/watchdog/sane runtime limits playbook.
homepage: https://github.com/NeoCh3n/openclaw-session-cleanup-skill
user-invocable: true
metadata: {"openclaw":{"emoji":"🧹","homepage":"https://github.com/NeoCh3n/openclaw-session-cleanup-skill","requires":{"bins":["bash","openclaw"]}}}
---

# OpenClaw Session Cleanup

Use this skill when the runtime becomes unstable after long uptime, especially on small hosts such as `1 vCPU / 2 GB RAM`.

## Trigger Pattern

Treat these as the main signals:

- `Sessions: 10+ active`
- `Agents: 5+`
- `browser control service timeout`
- `gateway 1006 abnormal closure`
- repeated gateway disconnects or slow recovery after idle periods

## What To Do

1. Inspect the current runtime state.
2. Prune stale sessions first.
3. If the runtime stays unhealthy, clear sessions.
4. Reduce runtime ceilings for sessions, agents, and browsers.
5. Add recurring cleanup and a watchdog when the host is expected to run for days.

## Immediate Commands

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

Healthy target after cleanup:

- `Sessions: 1-3`
- `Agents: 3`
- `Gateway reachable`
- `browser running`

## Safe Runtime Defaults

For `1 vCPU / 2 GB RAM`, prefer:

- `maxSessions = 5`
- `sessionTTL = 30m`
- `maxAgents = 3`
- `maxBrowsers = 1`
- `swap = 2G`

Use the starter config at `{baseDir}/templates/openclaw.json`.

## Automation

Install periodic pruning:

```bash
bash "{baseDir}/scripts/install-cron-prune.sh"
```

Install watchdog unit files:

```bash
bash "{baseDir}/scripts/install-watchdog.sh"
```

Render a tuned runtime config:

```bash
bash "{baseDir}/scripts/render-openclaw-config.sh"
```

## Browser Constraint

Treat browser control as the heaviest resource consumer on a small VPS.

Recommended mode:

```bash
openclaw browser start --single
```

## Swap

If the host has no swap, add `2G`:

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
free -h
```

## References

- Detailed runbook: `{baseDir}/docs/openclaw.session_cleanup_v1.md`
- Runtime template: `{baseDir}/templates/openclaw.json`
- Watchdog service: `{baseDir}/templates/openclaw-watchdog.service`
- Watchdog timer: `{baseDir}/templates/openclaw-watchdog.timer`
