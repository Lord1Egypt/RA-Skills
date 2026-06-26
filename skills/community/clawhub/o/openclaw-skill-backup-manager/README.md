# backup-manager

OpenClaw skill for managing local and cloud backups.

## Features

- **List backups** — Time Machine, rsync snapshots, configured backups
- **Create backups** — rsync-based incremental backups
- **Check status** — Disk space, last run times, backup health
- **Restore** — Restore from any backup location (with confirmation)
- **Schedule** — Cron-based recurring backups
- **Cloud support** — rclone integration for S3, GDrive, etc.

## Installation

```bash
# Via ClawHub (recommended)
clawhub install backup-manager

# Manual
git clone https://github.com/openclaw/backup-manager.git
```

## Usage

```bash
# List backups
backup-manager list

# Create a backup
backup-manager create home /Users/pp /Volumes/Backup/home

# Check status
backup-manager status

# Restore from backup
backup-manager restore /Volumes/Backup/home /Users/pp

# Schedule daily backup at 2 AM
backup-manager schedule add daily-home '0 2 * * *'

# Cloud sync
backup-manager cloud sync mydrive /Users/pp/Backup
```

## Configuration

Config stored at: `~/.config/openclaw/backups.json`

## Requirements

- rsync
- tmutil (macOS)
- diskutil (macOS)
- jq
- rclone (optional, for cloud)

## License

MIT — See [LICENSE](LICENSE)
