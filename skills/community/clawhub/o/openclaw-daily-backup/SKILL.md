---
name: openclaw-daily-backup
description: This skill should be used when the user asks for daily backup, scheduled backup, restore, rollback, recovery, or routine protection of core OpenClaw workspace identity/config files.
homepage: https://github.com/X-RayLuan/soul-backup-skill
---

# OpenClaw Daily Backup

Backup and restore OpenClaw workspace SOUL files (SOUL.md, USER.md, AGENTS.md, IDENTITY.md, TOOLS.md, HEARTBEAT.md, BOOTSTRAP.md) with versioning, validation, and rollback capabilities.

## Purpose

Protect critical workspace configuration files from accidental deletion, corruption, or misconfiguration. Enable quick recovery and version history tracking.

## What Gets Backed Up

Core SOUL files from workspace root:
- `SOUL.md` — agent personality and mission
- `USER.md` — user profile and preferences
- `AGENTS.md` — agent instructions and workflows
- `IDENTITY.md` — agent identity configuration
- `TOOLS.md` — local tool configuration
- `HEARTBEAT.md` — periodic task configuration
- `BOOTSTRAP.md` — initialization instructions

## Usage

### Backup Current SOUL Files

```bash
# Create timestamped backup
node scripts/backup.mjs

# Create named backup
node scripts/backup.mjs --name "pre-migration"

# Backup with description
node scripts/backup.mjs --desc "Before major refactor"
```

### List Backups

```bash
# List all backups
node scripts/list.mjs

# Show detailed info
node scripts/list.mjs --verbose
```

### Restore from Backup

```bash
# Restore latest backup
node scripts/restore.mjs

# Restore specific backup by timestamp
node scripts/restore.mjs --timestamp 2026-03-05T00-51-30

# Restore specific backup by name
node scripts/restore.mjs --name "pre-migration"

# Dry run (preview without applying)
node scripts/restore.mjs --dry-run
```

### Validate Backup Integrity

```bash
# Validate all backups
node scripts/validate.mjs

# Validate specific backup
node scripts/validate.mjs --timestamp 2026-03-05T00-51-30
```

## Backup Structure

```
backups/
├── 2026-03-05T00-51-30/
│   ├── manifest.json          # Backup metadata
│   ├── SOUL.md
│   ├── USER.md
│   ├── AGENTS.md
│   ├── IDENTITY.md
│   ├── TOOLS.md
│   ├── HEARTBEAT.md
│   └── BOOTSTRAP.md
├── 2026-03-05T01-15-42/
│   └── ...
└── named/
    ├── pre-migration/
    │   └── ...
    └── stable-v1/
        └── ...
```

## Manifest Format

Each backup includes a `manifest.json`:

```json
{
  "timestamp": "2026-03-05T00:51:30.123Z",
  "name": "pre-migration",
  "description": "Before major refactor",
  "workspace": "/Users/m1/.openclaw/workspace-hunter",
  "files": {
    "SOUL.md": {
      "size": 1234,
      "hash": "sha256:abc123...",
      "exists": true
    },
    "USER.md": {
      "size": 567,
      "hash": "sha256:def456...",
      "exists": true
    }
  },
  "created_by": "hunter",
  "openclaw_version": "1.0.0"
}
```

## Recovery Workflow

### Standard Recovery

1. List available backups: `node scripts/list.mjs`
2. Preview restore: `node scripts/restore.mjs --timestamp <ts> --dry-run`
3. Apply restore: `node scripts/restore.mjs --timestamp <ts>`
4. Verify: Check workspace files manually

### Emergency Recovery

If workspace is corrupted and scripts won't run:

```bash
# Manual restore from backup directory
cd /Users/m1/.openclaw/workspace-hunter
cp -r soul-backup-skill/backups/LATEST_TIMESTAMP/* .
```

### Rollback After Bad Restore

Every restore creates an automatic pre-restore backup:

```bash
# Restore creates: backups/pre-restore-2026-03-05T01-20-00/
# To rollback:
node scripts/restore.mjs --timestamp pre-restore-2026-03-05T01-20-00
```

## Automation

### Cron Schedule (Recommended)

Add to OpenClaw heartbeat or system cron:

```bash
# Daily backup at 2 AM
0 2 * * * cd /Users/m1/.openclaw/workspace-hunter/soul-backup-skill && node scripts/backup.mjs --name "daily-$(date +\%Y-\%m-\%d)"

# Weekly backup on Sunday
0 3 * * 0 cd /Users/m1/.openclaw/workspace-hunter/soul-backup-skill && node scripts/backup.mjs --name "weekly-$(date +\%Y-W\%V)"
```

### Pre-Deployment Hook

```bash
# Before deploying changes
cd /Users/m1/.openclaw/workspace-hunter/soul-backup-skill
node scripts/backup.mjs --name "pre-deploy-$(git rev-parse --short HEAD)"
```

## Validation Checks

The validate script checks:
- Manifest integrity (valid JSON, required fields)
- File existence (all files listed in manifest exist)
- Hash verification (SHA-256 checksums match)
- Workspace path consistency
- Timestamp format validity

## Failure Scenarios & Recovery

### Scenario 1: Accidental SOUL.md Deletion

```bash
# Immediate recovery
node scripts/restore.mjs --file SOUL.md

# Or full restore
node scripts/restore.mjs
```

### Scenario 2: Bad Configuration Change

```bash
# Preview what will be restored
node scripts/restore.mjs --dry-run

# Restore previous version
node scripts/restore.mjs --timestamp <previous-backup>
```

### Scenario 3: Corrupted Backup

```bash
# Validate all backups
node scripts/validate.mjs

# Find last good backup
node scripts/list.mjs --verbose

# Restore from last good backup
node scripts/restore.mjs --timestamp <last-good>
```

### Scenario 4: Complete Workspace Loss

```bash
# Recreate workspace directory
mkdir -p /Users/m1/.openclaw/workspace-hunter

# Clone backup skill
cd /Users/m1/.openclaw/workspace-hunter
git clone <backup-repo-url> soul-backup-skill

# Restore latest backup
cd soul-backup-skill
node scripts/restore.mjs
```

## Best Practices

1. **Backup before major changes**: Always create a named backup before refactoring SOUL files
2. **Validate regularly**: Run `validate.mjs` weekly to catch corruption early
3. **Keep 30 days of backups**: Prune old backups monthly
4. **Test restore process**: Practice recovery quarterly
5. **Document custom changes**: Use `--desc` flag to explain why backup was created
6. **Version control**: Consider committing backup directory to git for off-machine redundancy

## Security Notes

- Backups contain sensitive configuration (API keys in TOOLS.md, user info in USER.md)
- Store backup directory with same permissions as workspace
- Do not commit backups to public repositories
- Consider encrypting backup directory if workspace contains secrets

## Dependencies

- Node.js 18+
- No external npm packages (uses built-in crypto, fs, path)

## Troubleshooting

**"Backup directory not found"**
- Run `mkdir -p backups` in skill directory

**"Permission denied"**
- Check workspace directory permissions: `ls -la ..`
- Ensure backup script has execute permissions: `chmod +x scripts/*.mjs`

**"Hash mismatch during validation"**
- File was modified after backup creation
- Backup may be corrupted — use previous backup

**"Restore failed: file conflicts"**
- Use `--force` flag to overwrite existing files
- Or manually move conflicting files before restore

## Future Enhancements

- [ ] Compression (gzip backups to save space)
- [ ] Remote backup sync (S3, Dropbox, rsync)
- [ ] Differential backups (only changed files)
- [ ] Backup retention policy (auto-prune old backups)
- [ ] Encrypted backups (GPG encryption)
- [ ] Web UI for backup management
- [ ] Slack/Telegram notifications on backup/restore
