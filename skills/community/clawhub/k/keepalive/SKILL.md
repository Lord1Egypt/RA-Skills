---
name: openclaw-keepalive
description: |
  Keep OpenClaw gateway running 24/7 on a laptop or workstation. Use when: (1) user reports gateway disconnects or crashes, (2) user asks how to make OpenClaw run persistently, (3) user wants auto-start on boot, (4) user needs process monitoring or auto-restart, (5) user mentions "keep alive", "daemon", "service", "background", "startup", "24/7". Covers Windows/Linux/macOS with cross-platform scripts and configuration.
---

# OpenClaw Gateway Keepalive

Ensure the OpenClaw gateway process stays running across reboots, crashes, sleep, and network interruptions.

## Quick Start (Recommended)

Register as a system service with one command (all platforms):

```bash
openclaw gateway install
```

Effects:
- ✅ Auto-start on boot — no terminal needed
- ✅ Runs in background — survives terminal close
- ✅ Survives screen lock — independent of user session
- ✅ Auto-restart on crash — OS-level process supervision

Verify:

```bash
openclaw gateway status
```

Expected output:
- `Service: Scheduled Task (registered)` ✅
- `RPC probe: ok` ✅
- `Port: [127.0.0.1:18789]` ✅

## Commands

| Command | Description |
|---------|-------------|
| `openclaw gateway install` | Register as system service (one-time) |
| `openclaw gateway uninstall` | Remove system service |
| `openclaw gateway start` | Start gateway manually |
| `openclaw gateway stop` | Stop gateway |
| `openclaw gateway restart` | Restart gateway |
| `openclaw gateway status` | Check gateway status |
| `openclaw logs --follow` | Tail real-time logs |

## Platform Differences

### Windows
- Registers via **Task Scheduler** (schtasks)
- Service name: `OpenClaw Gateway`
- Survives screen lock and user session disconnect

### macOS
- Registers via **launchd** plist
- Supports `KeepAlive=true` for auto-restart

### Linux
- Registers via **systemd** service
- Supports `Restart=on-failure` policy

## Prevent Sleep (Critical)

The gateway requires the computer to stay awake. Configure power settings:

### Windows
```powershell
# List current power plans
powercfg /list

# Never sleep when plugged in
powercfg /change standby-timeout-ac 0

# Allow display off but keep system awake
powercfg /change monitor-timeout-ac 10
```

### macOS
```bash
# Prevent system sleep
sudo pmset -a sleep 0

# Prevent disk sleep
sudo pmset -a disksleep 0

# Allow display off but keep system running
sudo pmset -a displaysleep 10
```

### Linux
```bash
# Disable suspend
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

## Network Recovery

The gateway's WebSocket connection auto-reconnects after network interruptions using exponential backoff (1s → 2s → 4s → ...).

Manual restart if needed:
```bash
openclaw gateway restart
```

## Troubleshooting

### Gateway Unresponsive
```bash
openclaw gateway status    # Check process status
openclaw logs --follow     # View real-time logs
openclaw gateway restart   # Attempt restart
```

### Service Not Registered
```bash
openclaw gateway install   # Re-register
openclaw gateway status    # Verify
```

### Frequent Crashes
1. Check logs with `openclaw logs --follow` for crash cause
2. Ensure sufficient memory (Node.js process needs at least 512MB free)
3. Check for port conflicts (default: 18789)
4. Update to latest version

## Advanced: External Process Supervisors

If `gateway install` is not stable enough, use external tools:

### Option A: pm2 (Recommended, Cross-Platform)
```bash
npm install -g pm2
pm2 start openclaw -- gateway start
pm2 save
pm2 startup  # Generate startup command
```

### Option B: NSSM (Windows Only)
```bash
nssm install OpenClaw "C:\Program Files\nodejs\node.exe" "openclaw gateway start"
nssm set OpenClaw AppExit Default Restart
nssm start OpenClaw
```

### Option C: Windows Task Scheduler (Manual)
```powershell
# Create auto-start task with 1-minute restart on failure
schtasks /create /tn "OpenClaw Gateway" /tr "openclaw gateway start" /sc onstart /rl highest /f

# Or use Task Scheduler GUI for finer restart policies
```

## Healthcheck Scripts

Schedule these with cron or Task Scheduler for periodic health checks with auto-restart.

### Windows (healthcheck.cmd)

```cmd
@echo off
REM OpenClaw Gateway Healthcheck Script (Windows)
REM Run periodically via Task Scheduler or cron
REM Exit code 0 = healthy, 1 = failed to recover

echo [%date% %time%] Checking OpenClaw Gateway status...

openclaw gateway status >nul 2>&1
if %errorlevel% neq 0 (
    echo [%date% %time%] Gateway not responding. Attempting restart...
    openclaw gateway restart >nul 2>&1
    timeout /t 5 >nul
    openclaw gateway status >nul 2>&1
    if %errorlevel% neq 0 (
        echo [%date% %time%] CRITICAL: Gateway failed to restart!
        exit /b 1
    ) else (
        echo [%date% %time%] Gateway restarted successfully.
        exit /b 0
    )
) else (
    echo [%date% %time%] Gateway is running normally.
    exit /b 0
)
```

### Linux/macOS (healthcheck.sh)

```bash
#!/bin/bash
# OpenClaw Gateway Healthcheck Script (Linux/macOS)
# Usage: bash healthcheck.sh - can be scheduled via cron
# Example cron: */5 * * * * /path/to/healthcheck.sh >> /var/log/openclaw-healthcheck.log 2>&1

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Checking OpenClaw Gateway status..."

if openclaw gateway status > /dev/null 2>&1; then
    echo "[$TIMESTAMP] Gateway is running normally."
    exit 0
else
    echo "[$TIMESTAMP] Gateway not responding. Attempting restart..."
    openclaw gateway restart > /dev/null 2>&1
    sleep 5
    
    if openclaw gateway status > /dev/null 2>&1; then
        echo "[$TIMESTAMP] Gateway restarted successfully."
        exit 0
    else
        echo "[$TIMESTAMP] CRITICAL: Gateway failed to restart!"
        exit 1
    fi
fi
```

Save to a location of your choice and schedule:
- **Windows**: Task Scheduler → Run every 5 minutes
- **Linux/macOS**: `*/5 * * * * /path/to/healthcheck.sh >> /var/log/openclaw-healthcheck.log 2>&1`
