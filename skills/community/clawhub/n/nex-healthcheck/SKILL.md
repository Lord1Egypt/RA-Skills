---
name: nex-healthcheck
description: Multi-service health and uptime monitoring dashboard for websites, APIs, infrastructure, and applications across multiple systems. Monitor website availability and HTTP response codes with configurable status code validation, check SSL certificate expiration dates with advance warnings (30-day warning, 7-day critical threshold), verify DNS resolution and nameserver health for domain infrastructure. Monitor Docker container status and container-level health checks, track systemd service status on both local and remote machines via SSH, and perform network connectivity tests (TCP port connectivity, ICMP ping, SSH command execution with response validation). Configure flexible health checks including HTTP/HTTPS endpoint monitoring with custom ports, TCP port connectivity without HTTP, DNS resolution verification against multiple record types (A, AAAA, MX, NS), and complex remote checks through SSH including systemctl status queries and docker ps commands on remote infrastructure. Optional Telegram notifications alert you immediately when services degrade or certificates approach expiration with contextual information. View historical incident data with start/end times and duration, uptime percentages for specific date ranges, and SLA tracking for compliance reporting and incident analysis. Designed for DevOps engineers, system administrators, agency operators, and IT teams managing multiple production systems and critical services.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "💓"
    requires:
      bins:
        - python3
        - dig
        - ssh
      env:
        - HEALTHCHECK_TELEGRAM_TOKEN
        - HEALTHCHECK_TELEGRAM_CHAT
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-healthcheck.py"
      - "lib/*"
      - "setup.sh"
---

# Nex HealthCheck

Multi-service health dashboard and monitoring tool. Monitor websites, APIs, SSL certificates, Docker containers, systemd services, infrastructure health, and more. All checks run locally. Optional Telegram notifications.

## When to Use

Use this skill when the user asks about:

- Service uptime, health status, or monitoring
- Website or API availability checks
- SSL certificate expiry dates or renewal
- Docker container status or health
- Systemd service status
- Server or infrastructure health checks
- Disk usage or space monitoring
- Ping or network connectivity
- Incident history or downtime events
- Uptime statistics and SLA tracking
- Health dashboards or status pages

Trigger phrases: "is everything healthy?", "what went down this week?", "when does my SSL cert expire?", "check if ollama is running", "monitor my services", "uptime stats", "disk usage", "service health", "infrastructure status"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory, installs the CLI tool, and initializes the database.

## Available Commands

The CLI tool is `nex-healthcheck`. All commands output plain text.

### Check Services

Run health checks on monitored services:

```bash
nex-healthcheck check              # Run all enabled checks
nex-healthcheck check --service "nex-ai.be"
nex-healthcheck check --group "production"
nex-healthcheck check --tag "pi"
```

### Add Service

Add a service to monitor:

```bash
nex-healthcheck add --name "nex-ai.be" --type http --target "https://nex-ai.be" --expected 200
nex-healthcheck add --name "HAL-9000" --type tcp --target "192.168.1.100" --port 2222
nex-healthcheck add --name "SSL nex-ai.be" --type ssl_cert --target "nex-ai.be"
nex-healthcheck add --name "Pi Docker Ollama" --type docker --target "ollama" --ssh-host "pi@192.168.1.100"
nex-healthcheck add --name "Pi Disk" --type disk --target "/" --ssh-host "pi@192.168.1.100" --group "pi-infra"
nex-healthcheck add --name "Cloudflare DNS" --type dns --target "nex-ai.be"
nex-healthcheck add --name "Life Logger" --type systemd --target "nex-life-logger" --ssh-host "pi@192.168.1.100"
nex-healthcheck add --name "Health API" --type ssh_cmd --ssh-host "user@server" --target "curl http://localhost:8000/health" --expected "ok"
```

Check types:
- `http`: HTTP GET request, check status code
- `tcp`: TCP socket connection test
- `dns`: DNS resolution check (requires dig/nslookup)
- `ssl_cert`: SSL certificate expiry check
- `docker`: Docker container status (requires docker CLI or SSH)
- `systemd`: Systemd service status (requires systemctl or SSH)
- `ssh_cmd`: Run arbitrary command via SSH
- `ping`: ICMP ping check
- `disk`: Disk usage check

### List Services

```bash
nex-healthcheck list              # Show all monitored services
```

### Remove Service

```bash
nex-healthcheck remove --name "service-name"
```

### Status

```bash
nex-healthcheck status            # Quick status from last checks
```

### History

```bash
nex-healthcheck history --name "service-name" --days 7
nex-healthcheck history --name "service-name" --days 30
```

### Incidents

```bash
nex-healthcheck incidents          # Show active incidents
nex-healthcheck incidents --all    # Show all incidents (active + resolved)
```

### Uptime Statistics

```bash
nex-healthcheck uptime --days 30
nex-healthcheck uptime --days 7
```

### Dashboard

```bash
nex-healthcheck dashboard         # Full dashboard view
```

### Send Dashboard via Telegram

```bash
nex-healthcheck notify            # Send current status to Telegram
```

Requires `HEALTHCHECK_TELEGRAM_TOKEN` and `HEALTHCHECK_TELEGRAM_CHAT` environment variables.

### Configuration

```bash
nex-healthcheck config --set-token "YOUR_BOT_TOKEN"
nex-healthcheck config --set-chat "YOUR_CHAT_ID"
```

## Example Interactions

**User:** "Is everything healthy?"
**Agent runs:** `nex-healthcheck dashboard`
**Agent:** Shows full health dashboard with all services grouped by category.

**User:** "When does my SSL cert expire?"
**Agent runs:** `nex-healthcheck check --tag "ssl"`
**Agent:** Shows SSL certificate expiry dates for all monitored certificates.

**User:** "What went down this week?"
**Agent runs:** `nex-healthcheck incidents --all`
**Agent:** Shows all incidents from the past week with start/end times.

**User:** "Check if Ollama is running on the Pi"
**Agent runs:** `nex-healthcheck check --name "Pi Docker Ollama"`
**Agent:** Reports the container status.

**User:** "Show me uptime for the last month"
**Agent runs:** `nex-healthcheck uptime --days 30`
**Agent:** Displays uptime percentage, check success rate, and average response time.

**User:** "Monitor my nex-ai.be website"
**Agent runs:** `nex-healthcheck add --name "nex-ai.be" --type http --target "https://nex-ai.be" --expected 200 --group "production"`
**Agent:** Confirms service added. Then `nex-healthcheck check --service "nex-ai.be"` to verify.

**User:** "Check disk usage on my server"
**Agent runs:** `nex-healthcheck add --name "Server Disk" --type disk --target "/" --ssh-host "user@192.168.1.50"` then `nex-healthcheck check --name "Server Disk"`
**Agent:** Reports disk usage percentage and free space.

**User:** "Show me an incident history"
**Agent runs:** `nex-healthcheck incidents --all`
**Agent:** Lists all past incidents with duration and status.

## Output Parsing

All CLI output is plain text, structured for easy parsing:

- Traffic light emojis: 🟢 OK, 🟡 WARNING, 🔴 CRITICAL, ⚪ UNKNOWN
- Grouped by category/service group
- Timestamps in ISO-8601 format
- Every command output ends with `[Nex HealthCheck by Nex AI | nex-ai.be]`

When presenting output to the user, strip the footer line and present the information naturally.

## Important Notes

- All check data is stored locally at `~/.nex-healthcheck/`. No data is sent externally.
- Remote checks (Docker, systemd, disk on remote hosts) require SSH access. Configure with `--ssh-host user@host`.
- SSL cert checks warn at 30 days, critical at 7 days before expiry.
- Disk checks warn at 80% usage, critical at 90%.
- Default check interval is 5 minutes. Customize with `--interval` when adding a service.
- Telegram notifications require environment variables: `HEALTHCHECK_TELEGRAM_TOKEN` and `HEALTHCHECK_TELEGRAM_CHAT`.
- For periodic automated checks, use systemd timer (see setup.sh for optional service files).

## Troubleshooting

- **"dig and nslookup not found"**: Install `bind-utils` (RHEL/CentOS) or `dnsutils` (Debian/Ubuntu) for DNS checks.
- **"docker: command not found"**: Install Docker or use SSH to a remote Docker host with `--ssh-host`.
- **SSH failures**: Ensure passwordless SSH is configured, or use SSH key authentication.
- **Database not found**: Run `bash setup.sh` to initialize.

## Credits

Built by Nex AI (https://nex-ai.be) - Digital transformation for Belgian SMEs.
Author: Kevin Blancaflor
