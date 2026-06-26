---
name: openclaw-backup
description: Automatically backup OpenClaw configuration to a private GitHub repository. Features API key sanitization, activity detection, and smart backup frequency (hourly when active, daily when inactive). One-click recovery support.
---

# OpenClaw Backup

## Overview

Automatically backup your complete OpenClaw configuration to a private GitHub repository. Features:

- 🔐 **API Key Sanitization** - Automatically replaces sensitive keys before committing
- 🔄 **Smart Backup Frequency** - Hourly when active, daily when inactive
- 📦 **Complete Backup** - Agents, extensions, workspace, memory, and more
- 🔧 **One-Click Recovery** - Comprehensive recovery guide included

## When to Use

- After initial OpenClaw setup, establish a backup mechanism
- Periodic backup status checks
- System migration or disaster recovery

## Quick Start

### 1. Prerequisites

- Git installed
- GitHub SSH Key configured (recommended) or Personal Access Token
- GitHub private repository created (e.g., `openclaw-backup`)

### 2. Install Skill

Copy this skill to your OpenClaw workspace:

```bash
# Ensure skills directory exists
mkdir -p ~/.openclaw/workspace/skills

# Copy skill (assuming downloaded to current directory)
cp -r openclaw-backup ~/.openclaw/workspace/skills/
```

### 3. Run Installation Script

```bash
# One-click configuration
bash ~/.openclaw/workspace/skills/openclaw-backup/scripts/install.sh
```

Follow the prompts to enter:
- GitHub repository URL (e.g., `git@github.com:yourname/openclaw-backup.git`)
- Git username and email

### 4. Configure Auto Backup

After installation, a cron job will be created in OpenClaw to check for backup needs every hour.

## Usage

### Manual Backup

```bash
~/.openclaw/backup.sh backup
```

### Auto Backup (Based on Activity)

```bash
~/.openclaw/backup.sh auto
```

### Check Activity Status

```bash
~/.openclaw/check-activity.sh
# Output: active or inactive
```

### Restore from Backup

```bash
~/.openclaw/backup.sh restore
```

Follow the prompts:
1. Clone the backup repository
2. Edit `openclaw.json` to fill in real API keys
3. Restart Gateway

## Backup Contents

| Included | Description |
|----------|-------------|
| ✅ openclaw.json | Main configuration (API keys sanitized) |
| ✅ agents/ | All agent session history |
| ✅ extensions/ | All plugins |
| ✅ workspace-*/ | Agent workspaces |
| ✅ memory/ | Agent memory databases |
| ✅ credentials/ | Credential configurations |
| ✅ feishu/ | Feishu configurations |
| ✅ wecom/ | WeChat Work configurations |

| Excluded | Reason |
|----------|--------|
| ❌ logs/ | Log files, can be regenerated |

## Smart Backup Strategy

| Status | Condition | Backup Frequency |
|--------|-----------|------------------|
| 🟢 Active | Activity within last hour | Every 1 hour |
| 🔴 Inactive | No new activity | Every 24 hours |

## Security Notes

⚠️ **Important Security Warnings**:

1. **Must use a private repository** - Backups contain sensitive configurations
2. **API Keys are sanitized** - But other configs may still contain sensitive info
3. **Manual API key entry required on restore** - Keys are replaced in backup files

## File Structure

```
~/.openclaw/
├── backup.sh              # Main backup script
├── check-activity.sh      # Activity status checker
├── .gitignore             # Git ignore configuration
└── workspace/
    └── memory/
        └── heartbeat-state.json  # Records backup state
```

## Troubleshooting

### Push Failed

```bash
# Check SSH connection
ssh -T git@github.com

# Force push (use with caution)
cd ~/.openclaw && git push origin main --force
```

### Configuration Lost After Restore

Ensure:
1. Edit `openclaw.json` to fill in real API keys
2. Restart Gateway: `openclaw gateway restart`

## Customization

### Custom Backup Frequency

Edit `heartbeat-state.json`:

```json
{
  "backup": {
    "activeInterval": 3600000,
    "inactiveInterval": 86400000
  }
}
```

### Add More Exclusions

Edit `~/.openclaw/.gitignore`:

```gitignore
# Custom exclusions
secrets/
*.pem
```

## Author

OpenClaw Community

## Version

- v1.0.0 - Initial release with auto backup and smart frequency