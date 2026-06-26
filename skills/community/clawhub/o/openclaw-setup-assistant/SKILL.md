# OpenClaw Setup Assistant

Automated VPS setup, security hardening, and multi-agent configuration for OpenClaw deployments.

Use when: setting up OpenClaw on a new VPS, hardening security, configuring multi-agent architecture, or deploying messaging integrations.

## What it does

This skill guides you through a complete production-ready OpenClaw deployment:

1. **System Setup** — Install OpenClaw, configure Node.js, set up the gateway
2. **Security Hardening** — UFW firewall, SSH key-only auth, fail2ban, dedicated non-root user, sandbox mode
3. **Agent Configuration** — SOUL.md persona, MEMORY.md persistence, daily notes, heartbeats
4. **Multi-Agent Architecture** — Coordinator + specialized worker agents with isolated workspaces
5. **Messaging Integration** — Telegram, Discord, WhatsApp, Slack — connected and tested
6. **Automation** — Cron jobs, heartbeat monitoring, automated backups, health checks
7. **Documentation** — Generates setup-specific docs for future reference

## Usage

```
Setup OpenClaw on my VPS at 192.168.1.100 with Claude and Telegram integration
```

```
Harden my existing OpenClaw installation with full security
```

```
Configure a 3-agent architecture: main coordinator, research agent, and content agent
```

## Requirements

- Ubuntu 22.04+ or Debian 12+ VPS
- SSH access (root or sudo user)
- AI provider API key (Anthropic, OpenAI, or Google)
- Messaging platform bot token (optional)

## Security Checklist

The skill ensures:
- [ ] UFW firewall enabled (ports 22, 80, 443 only)
- [ ] SSH key-only authentication (password disabled)
- [ ] fail2ban installed and configured
- [ ] Non-root dedicated user for OpenClaw
- [ ] Gateway bound to localhost only (not exposed)
- [ ] Sandbox mode enabled in openclaw.json
- [ ] Automated daily backups configured

## Tags
openclaw, vps-setup, security, multi-agent, deployment, telegram, discord, automation
