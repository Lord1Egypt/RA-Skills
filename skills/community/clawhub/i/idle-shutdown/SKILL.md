---
name: gateway-idle-shutdown
description: Monitors OpenClaw Gateway user session idleness and automatically shuts down the Gateway after a configured idle period. Use when: (1) you need to detect idle state when no messages are exchanged between bot and user, (2) you want to set an idle timeout to shut down the Gateway and save resources, (3) you need to install/configure an idle monitoring systemd service, (4) you are managing the Gateway idle lifecycle. Trigger words: idle, shutdown, sleep, suspend, gateway monitor.
---

# Gateway Idle Shutdown

Monitors session activity between users and the bot, and automatically stops the OpenClaw Gateway when all sessions have been idle continuously beyond the configured threshold.

## How It Works

- Polls session transcript files (`~/.openclaw/agents/main/sessions/`) every 10 seconds for their last modification time (mtime)
- Preferentially matches QQBot/channel/direct related session files
- When the latest mtime is older than the threshold (default 120 seconds), executes `openclaw gateway stop`
- Logs are written to `~/.openclaw/logs/idle-shutdown.log`

## Benefits

- **Resource Savings** — Automatically stops the Gateway when no one is using it, freeing CPU and memory that would otherwise be wasted during idle periods.
- **Cost Reduction** — On metered or cloud-hosted environments, shutting down idle services reduces compute costs by avoiding charges for unused uptime.
- **Energy Efficiency** — Reduces power consumption by ensuring services only run when actually needed, lowering your carbon footprint.
- **Zero Manual Intervention** — Once configured, the watcher runs autonomously with systemd; you never need to remember to shut down the Gateway manually.
- **Seamless Lifecycle Integration** — The systemd watcher is bound to the Gateway service (BindsTo + PartOf), so it starts and stops in lockstep — no orphaned watcher processes and no stale state.
- **Configurable & Forgiving** — Idle threshold, polling interval, session directory, and binary path are all controlled via environment variables; the watcher retries on failure instead of exiting abruptly.
- **Lightweight Footprint** — A simple bash script with `sleep`-based polling uses negligible system resources, making it suitable for low-power devices and headless servers alike.

## Installation

```bash
# 1. Copy the script
cp scripts/idle-shutdown.sh ~/.openclaw/workspace/scripts/
chmod +x ~/.openclaw/workspace/scripts/idle-shutdown.sh

# 2. Create the systemd service file
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/openclaw-idle-watch.service << 'EOF'
[Unit]
Description=OpenClaw idle gateway shutdown watcher
After=openclaw-gateway.service
BindsTo=openclaw-gateway.service
PartOf=openclaw-gateway.service

[Service]
Type=simple
ExecStart=%h/.openclaw/workspace/scripts/idle-shutdown.sh
Restart=on-failure
RestartSec=10s
Environment=HOME=%h
# Adjust this PATH if your openclaw binary lives elsewhere
Environment=PATH=%h/.local/bin:%h/bin:/usr/local/bin:/usr/bin:/bin
Environment=OPENCLAW_BIN=openclaw

[Install]
WantedBy=default.target
EOF

# 3. Enable and start the service
systemctl --user daemon-reload
systemctl --user enable openclaw-idle-watch.service
systemctl --user start openclaw-idle-watch.service
```

## Configuration

Customize behavior via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `IDLE_SECONDS` | 120 | Idle threshold (seconds) |
| `POLL_SECONDS` | 10 | Polling interval (seconds) |
| `SESSIONS_DIR` | `~/.openclaw/agents/main/sessions` | Session directory |
| `LOG_FILE` | `~/.openclaw/logs/idle-shutdown.log` | Log file path |
| `OPENCLAW_BIN` | `openclaw` | openclaw binary path |

## Uninstallation

```bash
systemctl --user stop openclaw-idle-watch.service
systemctl --user disable openclaw-idle-watch.service
rm ~/.config/systemd/user/openclaw-idle-watch.service
rm ~/.openclaw/workspace/scripts/idle-shutdown.sh
```

## Service Lifecycle

- The watcher is bound to `openclaw-gateway.service` (BindsTo + PartOf)
- Gateway starts → Watcher starts automatically
- Gateway stops → Watcher stops automatically
- Watcher triggers on idle → Gateway is stopped → Watcher stops along with Gateway
