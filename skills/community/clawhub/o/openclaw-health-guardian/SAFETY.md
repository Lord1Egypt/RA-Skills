# Safety & Security Information

## Why This Skill is Safe

This skill is a **legitimate system monitoring tool** for OpenClaw Gateway health. It does not:

- ❌ Access external networks (only localhost:18789)
- ❌ Execute arbitrary code
- ❌ Access sensitive user data
- ❌ Use `eval` or dynamic code execution
- ❌ Require sudo/root privileges

## What It Does

1. **Health Monitoring**: Checks if OpenClaw Gateway is responding on `127.0.0.1:18789`
2. **Auto-Recovery**: Restarts Gateway service if it's not responding
3. **Rate Limiting**: Prevents restart loops (max 5/hour, 180s cooldown)
4. **User Notification**: Opens Terminal via AppleScript if manual intervention needed

## System Commands Used

| Command | Purpose | Safety |
|---------|---------|--------|
| `launchctl` | Manage macOS LaunchAgent services | Standard macOS tool, user-level only |
| `curl` | Check Gateway HTTP endpoint | Localhost only, no external network |
| `osascript` | Open Terminal for user notification | User-initiated, no automation |

## Scan Warnings Explained

### 1. HARDCODED_USER_PATH ✅ FIXED
**Status**: Fixed in v1.1
- All hardcoded `/Users/pg` paths replaced with `$HOME` variable
- Script now uses `$(which openclaw)` for dynamic path resolution
- Portable across all macOS users

### 2. USE_OF_LAUNCHCTL_BOOTSTRAP_BOOTOUT ✅ EXPECTED
**Status**: Expected behavior, documented here
- This skill IS a service management tool
- It needs to manage LaunchAgent for health monitoring
- Only operates on `ai.openclaw.gateway` and `com.openclaw.healthcheck` services
- All operations are user-level (gui/$(id -u)/), not system-wide
- No arbitrary service manipulation

### 3. OSASCRIPT_TERMINAL_EXEC ✅ EXPECTED
**Status**: Expected behavior, documented here
- Only used when automatic recovery fails
- Displays diagnostic information to help user fix issues manually
- Does NOT execute arbitrary commands - just shows status output
- User must manually confirm any action in the opened terminal
- Pure notification mechanism, not automation

## File Locations

All files are in user home directory:
- `~/.openclaw/scripts/` - Health check script
- `~/.openclaw/state/` - Cooldown/rate limit state
- `~/.openclaw/logs/` - Log files
- `~/Library/LaunchAgents/` - macOS service configuration

## Verification

You can audit the code:
```bash
cat ~/.openclaw/workspace/skills/openclaw-health-guardian/scripts/openclaw-health-check.sh
```

All operations are transparent and logged to `~/.openclaw/logs/health-check.log`.
