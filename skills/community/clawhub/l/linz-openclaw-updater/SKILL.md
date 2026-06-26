---
name: openclaw-updater
description: Automatically check for and install OpenClaw updates. Use when the user wants to update OpenClaw to the latest version, schedule automatic updates, or check the current version. Triggers on phrases like "update openclaw", "upgrade openclaw", "check for updates", "auto-update openclaw".
---

# OpenClaw Updater

Automatically check for and install OpenClaw updates with backup and rollback support.

## Overview

This skill provides automated OpenClaw update capabilities:
- Check current vs latest version
- Perform safe updates with automatic backups
- Schedule periodic auto-updates via cron
- Dry-run mode to preview updates

## Quick Start

### Check Current Version

```bash
openclaw --version
```

### Check for Updates (Dry Run)

```bash
bash ~/.openclaw/workspace/skills/openclaw-updater/scripts/update-openclaw.sh --dry-run
```

### Perform Update

```bash
bash ~/.openclaw/workspace/skills/openclaw-updater/scripts/update-openclaw.sh
```

### Force Reinstall

```bash
bash ~/.openclaw/workspace/skills/openclaw-updater/scripts/update-openclaw.sh --force
```

## Setting Up Auto-Updates

### Daily Auto-Update via Cron

Add to crontab for daily update checks at 3 AM:

```bash
0 3 * * * /bin/bash ~/.openclaw/workspace/skills/openclaw-updater/scripts/update-openclaw.sh >> ~/.openclaw/logs/cron-update.log 2>&1
```

Or use OpenClaw's built-in cron:

```json
{
  "name": "openclaw-auto-update",
  "schedule": { "kind": "cron", "expr": "0 3 * * *" },
  "payload": {
    "kind": "systemEvent",
    "text": "Run OpenClaw auto-updater: bash ~/.openclaw/workspace/skills/openclaw-updater/scripts/update-openclaw.sh"
  },
  "sessionTarget": "main"
}
```

## How It Works

1. **Version Check**: Compares installed version against npm registry
2. **Backup**: Creates timestamped backup of config and workspace
3. **Update**: Runs `npm install -g @openclaw/core@latest`
4. **Verify**: Confirms new version is installed
5. **Cleanup**: Maintains only last 5 backups

## Logs and Backups

- **Logs**: `~/.openclaw/logs/auto-update.log`
- **Backups**: `~/.openclaw/backups/openclaw-backup-YYYYMMDD-HHMMSS.tar.gz`

## Troubleshooting

### Node.js Version Issues

OpenClaw requires Node.js >= 22.16.0. If you see version warnings:

```bash
# Check current Node version
node --version

# Update Node.js (using n or nvm)
n install 22.16.0
# or
nvm install 22.16.0 && nvm use 22.16.0
```

### Update Fails

1. Check logs: `cat ~/.openclaw/logs/auto-update.log`
2. Verify npm permissions: `npm config get prefix`
3. Try with sudo if needed: `sudo npm install -g @openclaw/core@latest`

### Rollback

If update causes issues, restore from backup:

```bash
cd ~
tar -xzf ~/.openclaw/backups/openclaw-backup-YYYYMMDD-HHMMSS.tar.gz
```

## Script Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Check for updates without installing |
| `--force` | Force update even if versions match |
| `--help` | Show usage information |

## Resources

### scripts/
- `update-openclaw.sh` - Main update script with backup/restore capabilities
