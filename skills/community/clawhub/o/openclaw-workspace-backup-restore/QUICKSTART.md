# Quick Start Guide

Get started with SOUL Backup Skill in 5 minutes.

## Installation

```bash
# Navigate to your OpenClaw workspace
cd ~/.openclaw/workspace-YOUR-AGENT

# Clone the skill
git clone https://github.com/YOUR-USERNAME/soul-backup-skill.git

# Navigate to skill directory
cd soul-backup-skill
```

## Your First Backup

Create a backup of your current SOUL files:

```bash
node scripts/backup.mjs
```

You should see output like:

```
🔍 Starting SOUL backup...

✅ Backed up: SOUL.md (2194 bytes)
✅ Backed up: USER.md (343 bytes)
✅ Backed up: AGENTS.md (747 bytes)
✅ Backed up: IDENTITY.md (636 bytes)
✅ Backed up: TOOLS.md (860 bytes)
✅ Backed up: HEARTBEAT.md (168 bytes)
⚠️  Skipped: BOOTSTRAP.md (not found)

📦 Backup complete!
   Location: /path/to/backups/2026-03-05T00-51-30
   Files backed up: 6
   Files skipped: 1
```

## View Your Backups

```bash
node scripts/list.mjs
```

Output:

```
📦 Found 1 backup(s)

📅 2026-03-05T00-51-30
   Created: Mar 5, 2026, 12:51:30 AM
   Files: 6 (4.83 KB)

💡 Latest backup: 2026-03-05T00-51-30
   To restore: node scripts/restore.mjs --timestamp 2026-03-05T00-51-30
```

## Test Restore (Dry Run)

Preview what would be restored without making changes:

```bash
node scripts/restore.mjs --dry-run
```

Output:

```
🔍 Restore Preview

   Backup: 2026-03-05T00-51-30
   Created: 2026-03-04T16:51:30.808Z

Files to restore:
✅ overwrite: SOUL.md (2194 bytes)
✅ overwrite: USER.md (343 bytes)
✅ overwrite: AGENTS.md (747 bytes)
✅ overwrite: IDENTITY.md (636 bytes)
✅ overwrite: TOOLS.md (860 bytes)
✅ overwrite: HEARTBEAT.md (168 bytes)
⚠️  Skip: BOOTSTRAP.md (not in backup)

🔍 Dry run complete. No files were modified.
   Would restore: 6 files
   Would skip: 1 files
```

## Validate Backup Integrity

Check that your backup is valid:

```bash
node scripts/validate.mjs
```

Output:

```
📦 Validating 1 backup(s)...

🔍 Validating: 2026-03-05T00-51-30
   ⚠️  BOOTSTRAP.md: marked as not existing (expected)
   ✅ Valid backup (1 warning(s))

📊 Validation Summary
   Total backups: 1
   Total errors: 0
   Total warnings: 1

✅ All backups valid
```

## Common Use Cases

### Before Making Changes

```bash
# Create a named backup before refactoring
node scripts/backup.mjs --name "pre-refactor" --desc "Before SOUL.md rewrite"
```

### After Accidental Deletion

```bash
# Restore a single file
node scripts/restore.mjs --file SOUL.md
```

### Rollback Bad Changes

```bash
# List backups to find the right one
node scripts/list.mjs

# Restore specific backup
node scripts/restore.mjs --timestamp 2026-03-05T00-51-30
```

## Next Steps

- Read [SKILL.md](SKILL.md) for complete documentation
- Check [RUNBOOK.md](RUNBOOK.md) for recovery scenarios
- Set up [automated daily backups](README.md#automation)

## Need Help?

- **Issues:** [GitHub Issues](https://github.com/YOUR-USERNAME/soul-backup-skill/issues)
- **Discord:** [OpenClaw Community](https://discord.com/invite/clawd)
- **Docs:** [OpenClaw Documentation](https://docs.openclaw.ai)
