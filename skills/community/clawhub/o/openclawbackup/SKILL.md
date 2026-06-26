---
name: openclaw-backup
version: 1.0.0
description: >
  Backup OpenClaw workspace, config, and state using the built-in `openclaw backup create` command.
  Also handles cleanup of old backups and health verification.
  Triggers:
    - "backup openclaw", "run backup", "backup now"
    - "check backup health", "verify backup"
    - "cleanup old backups", "remove old backups"
    - First run on new machine → run setup + prompt to create cron job
  Uses built-in `openclaw backup create` — no extra tools needed.
  Cron message: "backup openclaw" → runs scripts/backup.py
---

# openclaw-backup

> See [CHANGELOG.md](./CHANGELOG.md) for version history.

Automated daily backup skill using OpenClaw's built-in `backup create` command.

## Backup Destination

`~/openclaw_backups/` — timestamped `.tar.gz` archives.

## Quick Commands

```bash
# Run backup now
python3 scripts/backup.py

# Run backup with verification
python3 scripts/backup.py --verify

# Verify latest backup
python3 scripts/health_check.py

# Cleanup old backups (dry-run, then --execute to delete)
python3 scripts/cleanup_old_backups.py --days 90
python3 scripts/cleanup_old_backups.py --days 90 --execute

# Setup daily cron at 4 AM
python3 scripts/setup_cron.py
```

## First-Time Setup on New Machine

1. **Test backup:**
   ```bash
   cd skills/openclaw-backup
   python3 scripts/backup.py --verify
   ```

2. **Verify health:**
   ```bash
   python3 scripts/health_check.py
   ```

3. **Setup cron (important — do this!):**
   ```bash
   python3 scripts/setup_cron.py
   ```

   This schedules daily 4 AM HKT backup via OpenClaw cron.
   Without this, backups only run when you manually trigger them.

4. **Verify cron:**
   ```bash
   openclaw cron list
   ```

## Cron Setup (Already Configured)

The daily cron job runs automatically at 04:00 HKT.
Trigger message: `backup openclaw`
Session: isolated

Manage cron:
```bash
# List
openclaw cron list

# Remove
openclaw cron remove openclaw-backup:daily

# Re-add
python3 scripts/setup_cron.py
```

## What Gets Backed Up

- Config files (`~/.openclaw/*.json`)
- Credentials (encrypted by OpenClaw)
- Session history
- Workspace files
- Skills and settings

## Retention

Backups are kept indefinitely by default. Run cleanup periodically:

```bash
# Preview old backups
python3 scripts/cleanup_old_backups.py --days 90

# Delete if looks good
python3 scripts/cleanup_old_backups.py --days 90 --execute
```

Suggested schedule: quarterly.

## Portable — Copy to New Machine

Copy the entire `openclaw-backup/` skill folder to a new machine, then:

```bash
cd skills/openclaw-backup
python3 scripts/backup.py --verify    # test
python3 scripts/setup_cron.py          # schedule daily
python3 scripts/health_check.py        # verify
```

No extra dependencies — uses OpenClaw's built-in `backup create`.