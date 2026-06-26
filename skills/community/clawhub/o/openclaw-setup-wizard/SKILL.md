---
name: openclaw-setup-wizard
description: Interactive OpenClaw setup wizard that diagnoses, configures, and optimizes a fresh or existing OpenClaw installation. Use when a user asks to set up OpenClaw, configure providers, connect chat channels, install skills, set up cron jobs, harden security, or troubleshoot their OpenClaw environment. Covers first-time setup, multi-provider configuration, channel connection, skill installation, backup setup, and health verification.
---

# OpenClaw Setup Wizard

One-command diagnostic and guided setup for OpenClaw installations.

## Quick Start

Run the diagnostic first to assess the current state:

```bash
bash scripts/diagnose.sh
```

This produces a JSON report covering: gateway status, provider config, channels, skills, cron jobs, security, and system resources.

## Workflow

1. **Diagnose** — Run `scripts/diagnose.sh` to get current system state
2. **Plan** — Based on diagnosis, identify what needs setup/fixing
3. **Configure** — Use `openclaw` CLI commands (never edit JSON directly)
4. **Verify** — Re-run diagnosis to confirm fixes
5. **Harden** — Run `scripts/harden.sh` for security best practices

## Diagnosis Output

The diagnose script checks 12 areas:
- OpenClaw version and gateway status
- Provider configuration (API keys, models, fallbacks)
- Channel connections (Telegram, Discord, Slack, etc.)
- Installed skills count and list
- Cron jobs status
- Memory/disk/CPU usage
- Backup configuration
- Security posture (token strength, file permissions)
- Network connectivity
- Node.js and dependency versions
- LaunchAgent/systemd service status
- Recent error logs

## Common Setup Tasks

### First-Time Setup
1. Run `diagnose.sh` → identify missing components
2. Configure primary LLM provider: `openclaw models set <model>`
3. Add fallback: `openclaw models fallbacks add <model>`
4. Connect chat channel (see references/channels.md)
5. Install essential skills: `clawhub install <skill>`
6. Set up backup cron
7. Run `harden.sh`

### Multi-Provider Setup
See references/providers.md for provider-specific configuration including API key setup, model selection, and fallback chains.

### Channel Connection
See references/channels.md for step-by-step guides for each supported channel (Telegram, Discord, Slack, WhatsApp, etc.)

### Security Hardening
Run `scripts/harden.sh` which checks and fixes:
- Gateway token strength (warns if default/weak)
- Config file permissions (should be 600)
- API key exposure in logs
- Firewall recommendations
- SSH hardening (if applicable)

### Troubleshooting
See references/troubleshooting.md for common issues and fixes.
