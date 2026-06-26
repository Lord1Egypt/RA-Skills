---
metadata:
  {
    "openclaw":
      {
        "emoji": "🛠️",
        "requires": { "bins": ["node"] }
      },
  }
---
name: openclaw-health-guardian
description: Deploy OpenClaw health monitoring with auto-restart, cooldown (180s), and rate limiting (5/hour). Use when: (1) setting up OpenClaw health checks, (2) auto-restarting failed Gateway, (3) monitoring OpenClaw status, (4) deploying health daemon on macOS.
---
metadata:
  {
    "openclaw":
      {
        "emoji": "🛠️",
        "requires": { "bins": ["node"] }
      },
  }
---

# OpenClaw Health Guardian

Auto-monitor and recover OpenClaw Gateway with intelligent rate limiting.

## Quick Start

**Install health guardian:**
```bash
bash ~/.openclaw/skills/openclaw-health-guardian/scripts/install.sh
```

**Verify installation:**
```bash
launchctl list | grep openclaw
```

## When to Use

- Gateway frequently stops responding
- Need automatic recovery without manual intervention
- Running OpenClaw on macOS with LaunchAgent support
- Want cooldown protection against restart loops

## Features

| Feature | Value | Description |
|---------|-------|-------------|
| Check Interval | 5 minutes | LaunchAgent StartInterval |
| Cooldown | 180 seconds | Minimum between restarts |
| Rate Limit | 5/hour | Max restarts per hour |
| HTTP Timeout | 5 seconds | curl --max-time |
| Auto Notify | Terminal popup | AppleScript alert on failure |

## Workflow

1. **Install guardian**
   ```bash
   bash ~/.openclaw/skills/openclaw-health-guardian/scripts/install.sh
   ```

2. **Verify service running**
   ```bash
   launchctl list | grep com.openclaw.healthcheck
   ```

3. **Monitor logs**
   ```bash
   tail -f ~/.openclaw/logs/health-check.log
   ```

4. **Test manually** (optional)
   ```bash
   bash ~/.openclaw/scripts/openclaw-health-check.sh
   ```

## Commands

| Command | Purpose |
|---------|---------|
| `launchctl list \| grep openclaw` | Check service status |
| `tail -f ~/.openclaw/logs/health-check.log` | View real-time logs |
| `bash ~/.openclaw/scripts/openclaw-health-check.sh` | Manual check |
| `launchctl unload ~/Library/LaunchAgents/com.openclaw.healthcheck.plist` | Stop service |
| `launchctl load ~/Library/LaunchAgents/com.openclaw.healthcheck.plist` | Start service |

## File Structure

After installation:
```
~/.openclaw/
├── scripts/
│   └── openclaw-health-check.sh    # Main script
├── state/
│   ├── last_restart                # Timestamp
│   ├── restart_count               # Hourly counter
│   └── hour_marker                 # Hour tracking
└── logs/
    ├── health-check.log            # Main log
    ├── health-check-daemon.log     # Daemon stdout
    └── health-check-daemon-error.log # Daemon stderr

~/Library/LaunchAgents/
└── com.openclaw.healthcheck.plist  # LaunchAgent config
```

## Log Examples

**Normal:**
```
[2026-03-16 10:28:47] No issues found. OpenClaw is healthy!
```

**Cooldown triggered:**
```
[2026-03-16 10:30:05] 冷却期内 (120s/180s)，跳过重启操作
```

**Rate limit triggered:**
```
[2026-03-16 10:30:05] 本小时已达重启上限(5次)，跳过
```

**Restart executed:**
```
[2026-03-16 10:30:02] 已记录重启事件 (冷却: 180s, 限流: 5/小时)
[2026-03-16 10:30:05] Gateway restart completed successfully
```

## Uninstall

```bash
# Stop and remove service
launchctl unload ~/Library/LaunchAgents/com.openclaw.healthcheck.plist
rm ~/Library/LaunchAgents/com.openclaw.healthcheck.plist

# Remove scripts and logs
rm ~/.openclaw/scripts/openclaw-health-check.sh
rm -rf ~/.openclaw/state/
rm ~/.openclaw/logs/health-check*.log
```

## Requirements

- macOS 10.14+
- OpenClaw installed
- User home directory write permissions

## References

- `references/technical-details.md` - Implementation details
- `references/troubleshooting.md` - Common issues
