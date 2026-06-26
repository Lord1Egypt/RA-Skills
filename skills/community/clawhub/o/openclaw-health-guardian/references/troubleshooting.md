# Troubleshooting Guide

## Service Not Running

### Symptom
```bash
$ launchctl list | grep healthcheck
# No output
```

### Solution
```bash
# Reload service
launchctl unload ~/Library/LaunchAgents/com.openclaw.healthcheck.plist 2>/dev/null
launchctl load ~/Library/LaunchAgents/com.openclaw.healthcheck.plist

# Verify
launchctl list | grep healthcheck
```

## Script Not Found

### Symptom
```
Error: openclaw command not found
```

### Solution
Script automatically searches multiple paths:
- `/opt/homebrew/bin/openclaw`
- `~/.nvm/versions/node/v22.22.0/bin/openclaw`
- `/usr/local/bin/openclaw`

If still not found:
```bash
# Add to ~/.zshrc or ~/.bash_profile
export PATH="$PATH:/path/to/openclaw"
```

## Too Many Restarts

### Symptom
```
本小时已达重启上限(5次)，跳过
```

### Solution
This is expected behavior. Check root cause:
```bash
# View recent logs
tail -50 ~/.openclaw/logs/health-check.log

# Check Gateway manually
openclaw status
curl -s http://127.0.0.1:18789
```

Common causes:
- Port conflict (18789 in use)
- Disk space full
- Configuration error

## Cooldown Blocking

### Symptom
```
冷却期内 (120s/180s)，跳过重启操作
```

### Solution
Wait for cooldown or force restart manually:
```bash
# Clear cooldown state
rm ~/.openclaw/state/last_restart

# Manual restart
openclaw gateway restart
```

## Logs Not Updating

### Symptom
Log file exists but no new entries.

### Solution
```bash
# Check daemon logs for errors
tail ~/.openclaw/logs/health-check-daemon-error.log

# Verify script permissions
ls -la ~/.openclaw/scripts/openclaw-health-check.sh

# Should show: -rwxr-xr-x
```

## High CPU Usage

### Symptom
System slow, high CPU from health check.

### Solution
```bash
# Stop service temporarily
launchctl unload ~/Library/LaunchAgents/com.openclaw.healthcheck.plist

# Check for infinite loops in logs
grep -c "Starting OpenClaw health check" ~/.openclaw/logs/health-check.log

# If count is very high, there may be a loop
# Reset state
rm -rf ~/.openclaw/state/
mkdir -p ~/.openclaw/state
```

## Terminal Popup Keeps Appearing

### Symptom
Terminal window opens frequently with health check alerts.

### Solution
This means automatic recovery is failing. Check:
```bash
# 1. Gateway status
openclaw status

# 2. Port availability
lsof -i :18789

# 3. Manual start
openclaw gateway start

# 4. If all fails, check logs
tail -100 ~/.openclaw/logs/health-check.log
```

## Uninstall Incomplete

### Symptom
Service still running after uninstall.

### Solution
```bash
# Force unload
launchctl bootout gui/$(id -u)/com.openclaw.healthcheck 2>/dev/null

# Remove all files
rm -f ~/Library/LaunchAgents/com.openclaw.healthcheck.plist
rm -f ~/.openclaw/scripts/openclaw-health-check.sh
rm -rf ~/.openclaw/state/
rm -f ~/.openclaw/logs/health-check*.log

# Verify removal
launchctl list | grep healthcheck  # Should be empty
```

## Reset All State

If you want to reset all counters and start fresh:

```bash
# Stop service
launchctl unload ~/Library/LaunchAgents/com.openclaw.healthcheck.plist

# Clear state
rm -rf ~/.openclaw/state/
mkdir -p ~/.openclaw/state

# Clear logs (optional)
rm ~/.openclaw/logs/health-check*.log

# Restart service
launchctl load ~/Library/LaunchAgents/com.openclaw.healthcheck.plist
```

## Debug Mode

To run script with verbose output:

```bash
# Run manually with trace
bash -x ~/.openclaw/scripts/openclaw-health-check.sh 2>&1 | tee debug.log
```

## Contact

If issues persist:
1. Collect logs: `~/.openclaw/logs/health-check*.log`
2. Check OpenClaw version: `openclaw --version`
3. Check macOS version: `sw_vers`
