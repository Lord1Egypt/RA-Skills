# Scheduled backups

Two lightweight scheduling options are supported:
1. `cron`
2. `systemd timer`

## Cron example

### Option 1: Daily full backup (original behavior)
```cron
30 3 * * * cd "$HOME/.openclaw/workspace" && /usr/bin/bash scripts/openclaw-backup.sh --encrypt-config --upload >> "$HOME/.openclaw/workspace/logs/openclaw-backup.log" 2>&1
```

### Option 2: Smart incremental backup (recommended)
Sunday full backup, Monday-Saturday incremental:
```cron
# Sunday at 00:00: Level 0 (full)
0 0 * * 0 cd "$HOME/.openclaw/workspace" && BACKUP_STRATEGY=smart /usr/bin/bash scripts/openclaw-backup.sh --encrypt-config --upload >> "$HOME/.openclaw/workspace/logs/openclaw-backup.log" 2>&1

# Mon-Sat at 03:30: Level 1 (incremental)
30 3 * * 1-6 cd "$HOME/.openclaw/workspace" && BACKUP_STRATEGY=smart /usr/bin/bash scripts/openclaw-backup.sh --encrypt-config --upload >> "$HOME/.openclaw/workspace/logs/openclaw-backup.log" 2>&1
```

### Option 3: Weekly full + daily incremental
```cron
# Sunday at 03:30: Full backup
30 3 * * 0 cd "$HOME/.openclaw/workspace" && BACKUP_STRATEGY=weekly /usr/bin/bash scripts/openclaw-backup.sh --encrypt-config --upload >> "$HOME/.openclaw/workspace/logs/openclaw-backup.log" 2>&1

# Mon-Sat at 03:30: Incremental
30 3 * * 1-6 cd "$HOME/.openclaw/workspace" && BACKUP_STRATEGY=daily /usr/bin/bash scripts/openclaw-backup.sh --encrypt-config --upload >> "$HOME/.openclaw/workspace/logs/openclaw-backup.log" 2>&1
```

### Notes
- `BACKUP_STRATEGY=smart`: Sunday=full, weekdays=incremental (recommended)
- `BACKUP_STRATEGY=weekly`: Always full backup
- `BACKUP_STRATEGY=daily`: Auto-detects first run as full, subsequent as incremental
- Incremental backups use `tar --listed-incremental` for efficient change tracking
- Snapshot files stored in `backups/openclaw/.snapshots/`
- uploads to the user's own WebDAV target
- logs to `~/.openclaw/workspace/logs/openclaw-backup.log`

### Before enabling
- confirm `.env.backup` is configured
- confirm the backup password is available via env var, `.env.backup.secret`, or interactive setup where appropriate
- confirm a manual run succeeds first

## systemd timer

Example installation flow (adjust paths if needed):
```bash
mkdir -p ~/.config/systemd/user
cp "$HOME/.openclaw/workspace/ops/systemd/openclaw-backup.service" ~/.config/systemd/user/
cp "$HOME/.openclaw/workspace/ops/systemd/openclaw-backup.timer" ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now openclaw-backup.timer
```

## Logs and checks
```bash
crontab -l
journalctl --user -u openclaw-backup.service -n 100 --no-pager
tail -f "$HOME/.openclaw/workspace/logs/openclaw-backup.log"
```

## Retention reminder

The script already supports automatic cleanup:
- `LOCAL_KEEP`
- `REMOTE_KEEP`

Example:
```bash
LOCAL_KEEP=7 REMOTE_KEEP=7 bash scripts/openclaw-backup.sh --encrypt-config --upload
```
