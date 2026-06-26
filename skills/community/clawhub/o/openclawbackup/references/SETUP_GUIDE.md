# openclaw-backup Setup Guide

Portable setup for any machine running OpenClaw. All paths are auto-detected.

---

## Quick Start (New Machine)

```bash
# 1. Navigate to the skill directory
cd <path-to-openclaw-backup>

# 2. Test backup (creates archive in ~/openclaw_backups)
python3 scripts/backup.py --verify

# 3. Verify the backup was created correctly
python3 scripts/health_check.py

# 4. Setup daily cron at 4 AM HKT — IMPORTANT!
python3 scripts/setup_cron.py

# 5. Verify cron
openclaw cron list
```

Done.

---

## What Each Script Does

| Script | Purpose |
|--------|---------|
| `backup.py` | Run `openclaw backup create` — creates timestamped archive |
| `health_check.py` | Verify archive integrity + list all backups |
| `cleanup_old_backups.py` | Delete old archives (default: dry-run) |
| `setup_cron.py` | Add daily 4 AM cron job via OpenClaw cron |

---

## Script Details

### backup.py

```bash
# Create backup with verification
python3 scripts/backup.py --verify

# Preview only (dry run)
python3 scripts/backup.py --dry-run

# Just create (no verify)
python3 scripts/backup.py
```

Output goes to `~/openclaw_backups/YYYY-MM-DDTHH-MM-SS.000Z-openclaw-backup.tar.gz`

### health_check.py

```bash
# Check latest backup
python3 scripts/health_check.py

# Verify specific archive
python3 scripts/health_check.py --archive /path/to/archive.tar.gz
```

### cleanup_old_backups.py

```bash
# Preview all backups (default dry-run)
python3 scripts/cleanup_old_backups.py

# Preview archives older than 90 days
python3 scripts/cleanup_old_backups.py --days 90

# Actually delete archives older than 90 days
python3 scripts/cleanup_old_backups.py --days 90 --execute
```

### setup_cron.py

```bash
python3 scripts/setup_cron.py
```

Adds cron job:
- Name: `openclaw-backup:daily`
- Time: `0 4 * * *` (04:00 HKT daily)
- Message trigger: `backup openclaw`
- Session: isolated

---

## Cron Setup (Manual)

If you prefer to set up cron manually:

```bash
openclaw cron add \
  --name "openclaw-backup:daily" \
  --message "backup openclaw" \
  --cron "0 4 * * *" \
  --tz "Asia/Hong_Kong" \
  --session isolated \
  --description "Daily OpenClaw backup to ~/openclaw_backups"
```

Remove:
```bash
openclaw cron remove openclaw-backup:daily
```

---

## Path Detection

| Path | Default |
|------|---------|
| Backup directory | `~/openclaw_backups/` |
| OpenClaw state | `~/.openclaw/` (auto-detected by `openclaw backup create`) |

Override backup dir with environment variable:
```bash
export OPENCLAW_BACKUP_DIR=/your/custom/path
```

---

## Portability

Copy the entire `openclaw-backup/` skill folder to a new machine.

On the new machine:
1. Run `python3 scripts/backup.py --verify` to test
2. Run `python3 scripts/setup_cron.py` to schedule daily backup
3. Run `python3 scripts/health_check.py` to verify

Cron jobs must be re-created on each machine (they live in OpenClaw's gateway, not in the skill folder).

---

## Retention Tip

Backups are kept indefinitely by default. Run cleanup quarterly:

```bash
# Preview old backups
python3 scripts/cleanup_old_backups.py --days 90

# Delete if looks good
python3 scripts/cleanup_old_backups.py --days 90 --execute
```

---

## Troubleshooting

### "openclaw: command not found"

OpenClaw CLI is not in PATH. Try:
```bash
which openclaw
# or find it:
find ~ -name "openclaw" -type f 2>/dev/null | head -5
```

### "No backups found"

Run backup first:
```bash
python3 scripts/backup.py --verify
```

### "Permission denied" on backup directory

Create the directory:
```bash
mkdir -p ~/openclaw_backups
chmod 755 ~/openclaw_backups
```

### Cron not running

Check cron status:
```bash
openclaw cron list
```

Manually trigger a backup:
```bash
python3 scripts/backup.py --verify
```

---

## File Structure

```
openclaw-backup/
├── SKILL.md                    ← Skill trigger file
├── SETUP_GUIDE.md              ← This file
└── scripts/
    ├── backup.py               ← Run the backup
    ├── health_check.py         ← Verify backup health
    ├── cleanup_old_backups.py  ← Remove old backups
    └── setup_cron.py           ← Add daily cron
```