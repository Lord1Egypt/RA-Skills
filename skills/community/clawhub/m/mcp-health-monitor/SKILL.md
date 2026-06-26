---
name: mcp-health-monitor
version: 1.0.0
description: Auto-monitor MCP servers and AI services with health checks, auto-restart on failure, and Telegram alerts
author: reikys
license: MIT
tags: [mcp, monitoring, health-check, automation, devops]
triggers:
  - "mcp health check"
  - "service monitor"
  - "health monitor setup"
  - "monitor mcp servers"
---

# MCP Health Monitor

Automated health monitoring for MCP servers and AI services. Detects failures, auto-restarts services via `launchctl`, and sends Telegram alerts on incidents. Silent when everything is healthy.

## Supported Check Types

| Type | Method | Auto-Restart |
|------|--------|--------------|
| HTTP Health | `curl` endpoint check | Yes (via launchctl) |
| Process | `pgrep` process detection | Yes (via launchctl) |
| Process-only | `pgrep` detection | No (expects external spawn) |

## Quick Start

### 1. Install the healthcheck script

```bash
# Copy the script to your preferred location
cp scripts/healthcheck.sh ~/.local/bin/mcp-healthcheck.sh
chmod +x ~/.local/bin/mcp-healthcheck.sh
```

### 2. Configure environment variables

Create or update your `.env` file (path configurable via `ENV_FILE`):

```bash
# Required for Telegram alerts (optional — script works without them)
TELEGRAM_BOT_TOKEN=your-bot-token-here
TELEGRAM_CHAT_ID=your-chat-id-here
```

### 3. Configure services to monitor

Edit the `SERVICES` array in `healthcheck.sh`. Each entry follows this format:

```
name|check_type|target|launchctl_label
```

**Fields:**
- `name` — Display name for logs and alerts
- `check_type` — `http` (HTTP endpoint) or `process` (pgrep pattern)
- `target` — URL for http checks, or process grep pattern for process checks
- `launchctl_label` — macOS launchctl service label for auto-restart (use `none` to skip restart)

**Default configuration:**

```bash
SERVICES=(
  "Claw-Empire|http|http://127.0.0.1:8790/api/health|com.claw-empire.server"
  "Hermes-Gateway|process|hermes_cli.main gateway|ai.hermes.gateway"
  "mem0-MCP|process|mem0_mcp/server.py|none"
  "Brave-Search-MCP|process|brave-search-mcp-server|none"
  "Context7-MCP|process|context7-mcp|none"
)
```

### 4. Set up automated scheduling (macOS LaunchAgent)

Create `~/Library/LaunchAgents/com.mcp-health-monitor.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.mcp-health-monitor</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>~/.local/bin/mcp-healthcheck.sh</string>
  </array>
  <key>StartInterval</key>
  <integer>300</integer>
  <key>StandardOutPath</key>
  <string>~/.local/logs/mcp-healthcheck-stdout.log</string>
  <key>StandardErrorPath</key>
  <string>~/.local/logs/mcp-healthcheck-stderr.log</string>
  <key>RunAtLoad</key>
  <true/>
</dict>
</plist>
```

Load the agent:

```bash
launchctl load ~/Library/LaunchAgents/com.mcp-health-monitor.plist
```

### 5. Linux alternative (systemd timer or cron)

```bash
# crontab -e
*/5 * * * * /path/to/mcp-healthcheck.sh
```

For systemd, replace `launchctl stop/start` calls in the script with `systemctl restart`.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ENV_FILE` | No | Path to `.env` file (default: `$HOME/.env`) |
| `LOG_FILE` | No | Path to log file (default: `$HOME/.local/logs/mcp-healthcheck.log`) |
| `TELEGRAM_BOT_TOKEN` | No | Telegram Bot API token for alerts |
| `TELEGRAM_CHAT_ID` | No | Telegram chat/group ID for alerts |
| `HTTP_TIMEOUT` | No | HTTP check timeout in seconds (default: `5`) |
| `RESTART_DELAY` | No | Seconds to wait between stop and start (default: `3`) |

## Log Format

Structured log entries:

```
[2026-03-30 14:00:00] [Claw-Empire] [OK] healthy (HTTP 200)
[2026-03-30 14:00:00] [mem0-MCP] [FAIL] not running (process not found)
[2026-03-30 14:00:00] [SYSTEM] [ALERT] 1 failures detected — sending notification
```

## Telegram Alert Format

Alerts are only sent when failures are detected. No notification on all-healthy runs.

```
🚨 *MCP Health Check Alert*
2026-03-30 14:00:00

Failures detected (1):
* mem0-MCP (process not found)

Services with launchctl labels were auto-restarted.
Process-only services await external respawn.
```

## Customization

### Adding a new service

Append to the `SERVICES` array:

```bash
SERVICES+=(
  "My-Custom-MCP|process|my-custom-mcp-server|com.my-custom.mcp"
)
```

### HTTP check with custom port

```bash
SERVICES+=(
  "My-API|http|http://127.0.0.1:3000/health|com.my-api.server"
)
```

### Disable auto-restart for a service

Set the launchctl label to `none`:

```bash
"My-Service|process|my-service-pattern|none"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Telegram alerts not sending | Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in your `.env` |
| `launchctl` restart fails | Check the service label matches your `.plist` file name |
| False positives on process checks | Adjust the `pgrep` pattern to be more specific |
| Log file growing too large | Set up `logrotate` or periodic cleanup via cron |
