# mcp-health-monitor

Automated health monitoring for MCP servers and AI services.

## Features

- **HTTP health endpoint checks** — Verify services respond with 200 OK
- **Process detection** — Check if expected processes are running via `pgrep`
- **Auto-restart** — Restart failed services via macOS `launchctl` (configurable per service)
- **Telegram alerts** — Send notifications only on failure (silent when healthy)
- **Structured logging** — Timestamped, service-scoped log entries
- **Configurable** — Add/remove services by editing a simple array

## Installation

```bash
# Clone or download
cp scripts/healthcheck.sh ~/.local/bin/mcp-healthcheck.sh
chmod +x ~/.local/bin/mcp-healthcheck.sh

# Configure (optional — for Telegram alerts)
echo 'TELEGRAM_BOT_TOKEN=your-token' >> ~/.env
echo 'TELEGRAM_CHAT_ID=your-chat-id' >> ~/.env
```

## Usage

### Manual run

```bash
./scripts/healthcheck.sh
```

### Scheduled (macOS LaunchAgent)

See `SKILL.md` for a complete LaunchAgent plist example that runs every 5 minutes.

### Scheduled (Linux cron)

```bash
*/5 * * * * ~/.local/bin/mcp-healthcheck.sh
```

## Configuration

### Services

Edit the `SERVICES` array in `healthcheck.sh`:

```bash
SERVICES=(
  "Service-Name|http|http://localhost:8080/health|com.my.service"
  "Another-Service|process|my-process-name|none"
)
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENV_FILE` | `$HOME/.env` | Path to environment file |
| `LOG_FILE` | `$HOME/.local/logs/mcp-healthcheck.log` | Log file path |
| `HTTP_TIMEOUT` | `5` | HTTP check timeout (seconds) |
| `RESTART_DELAY` | `3` | Delay between stop and start (seconds) |
| `TELEGRAM_BOT_TOKEN` | — | Telegram Bot API token |
| `TELEGRAM_CHAT_ID` | — | Telegram chat ID |

## Default Monitored Services

| Service | Check Type | Auto-Restart |
|---------|-----------|--------------|
| Claw-Empire | HTTP (`/api/health`) | Yes |
| Hermes Gateway | Process | Yes |
| mem0 MCP | Process | No |
| Brave Search MCP | Process | No |
| Context7 MCP | Process | No |

## License

MIT
