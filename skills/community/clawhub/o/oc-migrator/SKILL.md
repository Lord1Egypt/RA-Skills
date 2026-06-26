---
name: openclaw-migrator
description: "Full OpenClaw backup, restore, and migration between machines. Export your entire setup (config, workspace, memory, skills, cron jobs) into a single encrypted archive. Restore on any machine with one command. Use when: migrating to new hardware, setting up a backup machine, disaster recovery, or cloning your agent setup."
version: 1.0.0
author: 管家 (AI Butler)
---

# OpenClaw Migrator

Backup, restore, and migrate your entire OpenClaw setup between machines. One command to export, one command to restore.

## Why

- Moving to a new Mac/server? Don't lose your agent's memory and personality.
- Want a hot standby? Clone your setup to a second machine.
- Disaster recovery? Restore from encrypted backup in minutes.

## Commands

```bash
# Full export (creates encrypted .tar.gz.enc)
bash scripts/migrate.sh export

# Full export without encryption
bash scripts/migrate.sh export --no-encrypt

# Restore from backup
bash scripts/migrate.sh restore <backup-file>

# List what would be exported (dry run)
bash scripts/migrate.sh export --dry-run

# Export only specific components
bash scripts/migrate.sh export --only config,memory,skills
```

## What Gets Exported

| Component | Path | Included |
|-----------|------|----------|
| Global config | ~/.openclaw/openclaw.json | ✅ |
| Agent config | ~/.openclaw/agents/ | ✅ |
| Workspace files | ~/.openclaw/workspace/*.md | ✅ |
| Memory | ~/.openclaw/workspace/memory/ | ✅ |
| Knowledge | ~/.openclaw/workspace/knowledge/ | ✅ |
| Learnings | ~/.openclaw/workspace/.learnings/ | ✅ |
| Scripts | ~/.openclaw/workspace/scripts/ | ✅ |
| Skills (workspace) | ~/.openclaw/workspace/skills/ | ✅ |
| Cron jobs | via `openclaw cron list --json` | ✅ |
| Conversations | ~/.openclaw/workspace/memory/conversations/ | Optional |

## What Gets Excluded

- Node modules, build artifacts
- Log files (regenerated)
- Session data (ephemeral)
- Gateway PID files

## Restore Process

1. Install OpenClaw on new machine
2. Run `bash scripts/migrate.sh restore <backup-file>`
3. Restart gateway: `openclaw gateway restart`
4. Verify: `openclaw status`

## Security

- Exports are encrypted with AES-256-CBC by default
- Password prompted at export time (or via MIGRATE_PASSWORD env var)
- Auth profiles with API keys are included — handle backups securely
- Encrypted backups safe for cloud storage (S3, Google Drive, etc.)

## Platform Support
- macOS ✅ (primary)
- Linux ✅
- Cross-platform migration (macOS → Linux, Linux → macOS) ✅
