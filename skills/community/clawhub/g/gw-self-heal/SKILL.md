---
name: gateway-watchdog
description: Self-healing watchdog for OpenClaw gateway. Auto-backup openclaw.json before changes, health-check the gateway process, and auto-rollback to last known good config on failure. Use when setting up gateway resilience, self-recovery, auto-restart, config backup, or when the user mentions watchdog, self-heal, gateway down, or config recovery.
---

# Gateway Watchdog

Automated self-healing system for OpenClaw gateway failures including config corruption, process crashes, and auth failures.

## How It Works

Three-layer protection:

1. **Config Guard** — Auto-backup `openclaw.json` on every successful health check
2. **Process Watchdog** — Detect gateway process death → auto-restart
3. **Auth Health Check** — Detect running-but-broken state → rollback config → restart

## Setup

Run the setup script to install the watchdog:

```bash
bash scripts/setup-watchdog.sh
```

This will:
- Create the watchdog script at `~/.openclaw/watchdog.sh`
- Register it as a cron job (every minute)
- Take an initial config backup

## Manual Commands

```bash
# Check watchdog status
bash scripts/watchdog-status.sh

# Force backup current config
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# View watchdog logs
cat ~/.openclaw/watchdog.log | tail -20

# Disable watchdog
crontab -l | grep -v watchdog | crontab -
```

## Recovery Levels

| Level | Condition | Action | Auto? |
|-------|-----------|--------|-------|
| 1 | Process dead, config OK | Restart gateway | ✅ |
| 2 | Process alive, health check fail | Rollback config + restart | ✅ |
| 3 | No valid backup exists | Log alert, notify if possible | ⚠️ Manual |

## Config Backup Strategy

- **Auto-backup**: On every successful health check, current config overwrites `.bak`
- **Pre-change backup**: Before any `openclaw.json` edit, copy to `.bak.prev`
- **Broken config preserved**: Failed configs saved as `.broken.<timestamp>` for debugging

## Logs

All watchdog activity logged to `~/.openclaw/watchdog.log` with timestamps.

## Platform Support

- **macOS**: cron-based (launchd alternative in `references/launchd.md`)
- **Linux**: cron or systemd (see `references/systemd.md`)
- **Docker**: Use HEALTHCHECK directive (see `references/docker.md`)
