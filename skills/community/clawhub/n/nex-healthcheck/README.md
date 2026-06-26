# Nex HealthCheck

Multi-service health dashboard and monitoring tool. Monitor websites, APIs, SSL certificates, Docker containers, systemd services, infrastructure health, and more.

## Features

- **HTTP/HTTPS monitoring**: Check website availability and status codes
- **TCP/UDP checks**: Test port availability
- **DNS resolution**: Verify DNS records resolve correctly
- **SSL certificate monitoring**: Track expiry dates with alerts at 30 and 7 days
- **Docker container monitoring**: Check container status via local or remote Docker
- **Systemd service monitoring**: Monitor service status
- **SSH command execution**: Run custom checks on remote servers
- **Ping/ICMP checks**: Test connectivity
- **Disk usage monitoring**: Check disk space usage
- **Incident tracking**: Automatic incident detection and history
- **Uptime statistics**: Calculate uptime percentages over time
- **Telegram notifications**: Send alerts and dashboards to Telegram
- **Service grouping**: Organize services by group or tag
- **Dashboard view**: Full health overview with status summary

## Requirements

- Python 3.9+
- `dig` or `nslookup` for DNS checks (optional)
- Docker CLI for Docker checks (optional)
- SSH access for remote checks (optional)

## Installation

```bash
bash setup.sh
```

This will:
1. Create `~/.nex-healthcheck/` data directory
2. Create SQLite database for checks and incidents
3. Create `~/.local/bin/nex-healthcheck` wrapper script
4. (Linux only) Install optional systemd timer for periodic checks

## Quick Start

```bash
# Add a service
nex-healthcheck add --name "My Website" --type http --target "https://example.com" --expected 200

# Run all checks
nex-healthcheck check

# View status
nex-healthcheck dashboard

# View incidents
nex-healthcheck incidents
```

## All Commands

See SKILL.md for complete documentation.

```bash
nex-healthcheck check [--service NAME] [--group GROUP] [--tag TAG]
nex-healthcheck add --name NAME --type TYPE --target TARGET [options]
nex-healthcheck list
nex-healthcheck remove --name NAME
nex-healthcheck status
nex-healthcheck history --name NAME [--days N]
nex-healthcheck incidents [--all]
nex-healthcheck uptime [--days N]
nex-healthcheck dashboard
nex-healthcheck notify
nex-healthcheck config [--set-token TOKEN] [--set-chat CHAT_ID]
```

## Check Types

| Type | Purpose | Example |
|------|---------|---------|
| `http` | HTTP/HTTPS requests | Websites, APIs |
| `tcp` | TCP port connectivity | SSH, custom ports |
| `dns` | DNS resolution | Verify DNS records |
| `ssl_cert` | SSL certificate expiry | Track certificate dates |
| `docker` | Container status | Check running containers |
| `systemd` | Service status | Check systemd services |
| `ssh_cmd` | Execute remote command | Custom checks |
| `ping` | ICMP connectivity | Network reachability |
| `disk` | Disk usage | Free space monitoring |

## Environment Variables

```bash
HEALTHCHECK_DATA=/path/to/data           # Data directory (default: ~/.nex-healthcheck)
HEALTHCHECK_TELEGRAM_TOKEN=your_token    # Telegram bot token
HEALTHCHECK_TELEGRAM_CHAT=your_chat_id   # Telegram chat ID
```

## Database Location

All data is stored locally:
- Database: `~/.nex-healthcheck/healthcheck.db`
- Logs: `~/.nex-healthcheck/healthcheck.log`

## Remote Checks via SSH

For Docker, systemd, disk, and SSH command checks on remote servers:

```bash
nex-healthcheck add --name "Remote Ollama" --type docker --target "ollama" \
  --ssh-host "user@192.168.1.100"

nex-healthcheck add --name "Remote Disk" --type disk --target "/" \
  --ssh-host "user@192.168.1.100"
```

Ensure passwordless SSH is configured using SSH keys.

## Telegram Notifications

Set up Telegram notifications:

```bash
export HEALTHCHECK_TELEGRAM_TOKEN="123456789:ABCDEFGHIJKLMNOPQRSTUVWxyz"
export HEALTHCHECK_TELEGRAM_CHAT="987654321"

nex-healthcheck notify  # Send current dashboard
```

## License

MIT-0 License. See LICENSE.txt for details.

## Author

Built by Nex AI - Digital transformation for Belgian SMEs.
https://nex-ai.be
