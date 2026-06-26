# SOUL Backup Skill - Runbook

## Quick Reference

### Create Backup
```bash
cd /Users/m1/.openclaw/workspace-hunter/soul-backup-skill
node scripts/backup.mjs
node scripts/backup.mjs --name "pre-migration" --desc "Before major refactor"
```

### List Backups
```bash
node scripts/list.mjs
node scripts/list.mjs --verbose
```

### Restore Backup
```bash
node scripts/restore.mjs                              # Latest backup
node scripts/restore.mjs --timestamp 2026-03-05T00-51-30
node scripts/restore.mjs --name "pre-migration"
node scripts/restore.mjs --dry-run                    # Preview only
node scripts/restore.mjs --file SOUL.md               # Single file
```

### Validate Backups
```bash
node scripts/validate.mjs                             # All backups
node scripts/validate.mjs --timestamp 2026-03-05T00-51-30
```

## Recovery Scenarios

### Scenario 1: Accidental File Deletion

**Problem:** User accidentally deleted SOUL.md

**Recovery:**
```bash
cd /Users/m1/.openclaw/workspace-hunter/soul-backup-skill
node scripts/restore.mjs --file SOUL.md
```

**Verification:**
```bash
ls -lh /Users/m1/.openclaw/workspace-hunter/SOUL.md
cat /Users/m1/.openclaw/workspace-hunter/SOUL.md | head -20
```

### Scenario 2: Bad Configuration Change

**Problem:** Modified AGENTS.md with breaking changes, need to rollback

**Recovery:**
```bash
# Preview what will be restored
node scripts/restore.mjs --dry-run

# Find previous backup
node scripts/list.mjs

# Restore specific backup
node scripts/restore.mjs --timestamp <previous-backup-timestamp>
```

**Verification:**
```bash
git diff /Users/m1/.openclaw/workspace-hunter/AGENTS.md
```

### Scenario 3: Complete Workspace Corruption

**Problem:** Multiple SOUL files corrupted or deleted

**Recovery:**
```bash
# List available backups
cd /Users/m1/.openclaw/workspace-hunter/soul-backup-skill
node scripts/list.mjs --verbose

# Validate backup integrity
node scripts/validate.mjs --timestamp <latest-backup>

# Restore all files
node scripts/restore.mjs --timestamp <latest-backup>
```

**Verification:**
```bash
ls -lh /Users/m1/.openclaw/workspace-hunter/*.md
node scripts/validate.mjs --timestamp <restored-backup>
```

### Scenario 4: Rollback After Bad Restore

**Problem:** Restored wrong backup, need to undo

**Recovery:**
```bash
# Every restore creates pre-restore-TIMESTAMP backup
node scripts/list.mjs | grep pre-restore

# Restore the pre-restore backup
node scripts/restore.mjs --timestamp pre-restore-2026-03-05T01-20-00
```

**Verification:**
```bash
diff /Users/m1/.openclaw/workspace-hunter/SOUL.md soul-backup-skill/backups/pre-restore-*/SOUL.md
```

### Scenario 5: Corrupted Backup

**Problem:** Backup validation fails, need to find last good backup

**Recovery:**
```bash
# Validate all backups
node scripts/validate.mjs

# Find last valid backup (check output for ✅)
node scripts/list.mjs --verbose

# Restore from last good backup
node scripts/restore.mjs --timestamp <last-good-timestamp>
```

**Verification:**
```bash
node scripts/validate.mjs --timestamp <restored-backup>
```

## Failure Modes & Mitigation

### Failure Mode 1: Backup Script Fails

**Symptoms:**
- Error during backup creation
- Incomplete manifest.json
- Missing files in backup directory

**Mitigation:**
```bash
# Check disk space
df -h /Users/m1/.openclaw/workspace-hunter

# Check permissions
ls -ld /Users/m1/.openclaw/workspace-hunter/soul-backup-skill/backups

# Retry backup
node scripts/backup.mjs --name "retry-$(date +%s)"

# Validate new backup
node scripts/validate.mjs --timestamp <new-backup>
```

### Failure Mode 2: Restore Overwrites Wrong Files

**Symptoms:**
- Restored files don't match expected content
- Workspace in inconsistent state

**Mitigation:**
```bash
# ALWAYS use --dry-run first
node scripts/restore.mjs --dry-run

# Check pre-restore backup was created
node scripts/list.mjs | grep pre-restore | tail -1

# If restore went wrong, rollback immediately
node scripts/restore.mjs --timestamp <pre-restore-backup>
```

### Failure Mode 3: Hash Mismatch During Validation

**Symptoms:**
- validate.mjs reports hash mismatch
- File corruption detected

**Mitigation:**
```bash
# Identify corrupted backup
node scripts/validate.mjs

# Find previous good backup
node scripts/list.mjs --verbose

# Restore from previous good backup
node scripts/restore.mjs --timestamp <previous-good>

# Create new backup immediately
node scripts/backup.mjs --name "recovered-$(date +%s)"
```

### Failure Mode 4: All Backups Lost

**Symptoms:**
- backups/ directory deleted or corrupted
- No valid backups found

**Mitigation:**
```bash
# Check if git has backup history
cd /Users/m1/.openclaw/workspace-hunter
git log --all --full-history -- soul-backup-skill/backups/

# Restore from git if available
git checkout <commit-hash> -- soul-backup-skill/backups/

# If no git history, check Time Machine (macOS)
tmutil listbackups
tmutil restore /Users/m1/.openclaw/workspace-hunter/soul-backup-skill/backups

# Last resort: manual recreation
# User must manually recreate SOUL files from memory/documentation
```

## Validation Checklist

Before deploying to production:

- [ ] Create test backup: `node scripts/backup.mjs --name "test"`
- [ ] Validate backup: `node scripts/validate.mjs --name test`
- [ ] Test dry-run restore: `node scripts/restore.mjs --name test --dry-run`
- [ ] Test actual restore: `node scripts/restore.mjs --name test`
- [ ] Verify files restored correctly: `diff -r backups/named/test/ ../`
- [ ] Test rollback: `node scripts/restore.mjs --timestamp pre-restore-*`
- [ ] Test single file restore: `node scripts/restore.mjs --name test --file SOUL.md`
- [ ] Test corrupted backup detection: (manually corrupt a file, run validate)
- [ ] Document backup location in team wiki
- [ ] Set up automated daily backups (cron/heartbeat)

## Automation Setup

### Daily Backup (Cron)

```bash
# Add to crontab: crontab -e
0 2 * * * cd /Users/m1/.openclaw/workspace-hunter/soul-backup-skill && /usr/local/bin/node scripts/backup.mjs --name "daily-$(date +\%Y-\%m-\%d)" >> /tmp/soul-backup.log 2>&1
```

### Pre-Deployment Hook (Git)

```bash
# Add to .git/hooks/pre-push
#!/bin/bash
cd /Users/m1/.openclaw/workspace-hunter/soul-backup-skill
/usr/local/bin/node scripts/backup.mjs --name "pre-deploy-$(git rev-parse --short HEAD)"
```

### Weekly Validation (Cron)

```bash
# Add to crontab: crontab -e
0 3 * * 0 cd /Users/m1/.openclaw/workspace-hunter/soul-backup-skill && /usr/local/bin/node scripts/validate.mjs >> /tmp/soul-validate.log 2>&1
```

## Monitoring

### Health Check Script

```bash
#!/bin/bash
# Check backup health
cd /Users/m1/.openclaw/workspace-hunter/soul-backup-skill

# Count backups
BACKUP_COUNT=$(node scripts/list.mjs 2>/dev/null | grep -c "📅\|📌")

if [ "$BACKUP_COUNT" -lt 1 ]; then
  echo "❌ No backups found"
  exit 1
fi

# Validate latest backup
node scripts/validate.mjs 2>&1 | grep -q "✅ All backups valid"
if [ $? -ne 0 ]; then
  echo "❌ Backup validation failed"
  exit 1
fi

echo "✅ Backup health OK ($BACKUP_COUNT backups)"
exit 0
```

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Backup script fails silently | High | Low | Add validation step after every backup |
| Restore overwrites wrong files | High | Medium | Always use --dry-run first, auto pre-restore backup |
| All backups corrupted | Critical | Very Low | Store backups in git, enable Time Machine |
| Disk space exhaustion | Medium | Low | Monitor disk usage, prune old backups monthly |
| User forgets to backup before changes | Medium | High | Add pre-push git hook, daily automated backups |
| Hash collision (SHA-256) | Low | Negligible | Accept risk (2^-256 probability) |
| Backup directory deleted | High | Low | Git-track backups/, enable Time Machine |

## Emergency Contacts

- Primary: Ray Luan (workspace owner)
- Backup location: `/Users/m1/.openclaw/workspace-hunter/soul-backup-skill/backups/`
- Git repo: (if tracked)
- Time Machine: (if enabled)

## Version History

- v1.0.0 (2026-03-05): Initial release
  - backup.mjs, restore.mjs, list.mjs, validate.mjs
  - SHA-256 integrity checking
  - Pre-restore automatic backups
  - Named backup support
