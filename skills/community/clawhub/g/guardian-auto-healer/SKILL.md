---
name: guardian-auto-healer
description: OpenClaw 7x24 watchdog & auto-healer. Monitors gateway health, memory usage, zombie sessions, and disk space every 5 minutes with automatic restart when stuck. 
---

# Guardian — OpenClaw 7x24 Watchdog & Auto-Healer

## Overview

Deploy a lightweight watchdog that checks OpenClaw health every 5 minutes and auto-heals when problems are found. Runs as a cron job — zero manual intervention after setup.
Use when the user asks to set up health monitoring, auto-healing, watchdog, or crash recovery for OpenClaw. 

## Triggers

"watchdog", "guardian", "auto-heal", "auto-restart", "health monitor", "7x24 monitor", "crash recovery", "memory monitor", "OOM guard".

## Quick Start

Install and schedule with cron in one go:

1. **Copy the watchdog script** to the workspace (one-time):
   ```
   Copy scripts/watchdog.py → ~/.openclaw/workspace/guardian/watchdog.py
   ```
   (Use `cp -r` / `copy`; adjust the destination as needed. Keep the `guardian/` folder in workspace.)

2. **Schedule via cron** (5-minute interval):
   Use the `cron` tool to create a recurring `agentTurn` job:
   ```json
   {
     "schedule": { "kind": "every", "everyMs": 300000 },
     "payload": {
       "kind": "agentTurn",
       "message": "Run guardian watchdog: execute `python3 ~/.openclaw/workspace/guardian/watchdog.py`. Report issues only if gateway is down, memory exceeds threshold, or disk is low. Otherwise reply HEALTH_OK.",
       "timeoutSeconds": 60
     },
     "sessionTarget": "isolated",
     "name": "guardian:watchdog",
     "delivery": { "mode": "announce" }
   }
   ```

3. **Verify** — after the first run, check logs:
   ```
   cat ~/.openclaw/logs/guardian.log     # macOS/Linux
   type %USERPROFILE%\.openclaw\logs\guardian.log   # Windows
   ```

## What It Monitors

| Check | Threshold | Auto-Heal Action |
|-------|-----------|-----------------|
| Gateway alive | Unresponsive > 15s | `openclaw gateway restart` |
| Memory usage | Warn > 500 MB, Kill > 1 GB | Restart gateway on kill |
| Disk space | Free < 1 GB | Alert only (no auto-action) |

## Manual Run

To run a one-off check without waiting for cron:
```bash
python3 ~/.openclaw/workspace/guardian/watchdog.py
```

## Logs

All checks are recorded to `~/.openclaw/logs/guardian.log` with timestamps. Each run produces a delimited block like:

```
[2026-05-04 23:00:00] ============================
[2026-05-04 23:00:00] Guardian Watchdog check starting...
[2026-05-04 23:00:00] OK: Gateway is responsive.
[2026-05-04 23:00:00] OK: Memory usage 234 MB (500 MB warn, 1000 MB kill).
[2026-05-04 23:00:00] OK: Disk free space 45.2 GB.
[2026-05-04 23:00:00] RESULT: All systems healthy.
[2026-05-04 23:00:00] ============================
```

## Managing the Cron Job

- **List jobs**: `openclaw cron list`
- **Run now**: `openclaw cron run <job-id>` (find id from list)
- **Stop**: `openclaw cron update <job-id> --enabled false`
- **Remove**: `openclaw cron remove <job-id>`

## Troubleshooting

- **"openclaw CLI not found"**: The watchdog uses `shutil.which("openclaw")`. If the CLI is not in PATH, manually set the path in `watchdog.py` by editing `find_openclaw_cli()`.
- **Restart fails**: Gateway may need manual intervention. Check `openclaw gateway status` directly.
- **High memory but no restart**: Memory threshold only triggers restart at >1 GB. Below that, only warns.
- **Windows encoding**: The script writes logs in UTF-8. If reading logs produces garbled output, use `chcp 65001` first.
