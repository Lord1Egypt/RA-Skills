# backup-manager Skill

Manage local and cloud backups — list status, create backups, restore, monitor health.

## Installation

This skill is automatically available in OpenClaw. The backup-manager CLI is located at:
```
~/.openclaw/workspace/skills/backup-manager/backup-manager
```

## Commands

### List Backups
```bash
backup-manager list
```
Lists all backups including Time Machine, configured backups, and rsync snapshots.

### Create Backup
```bash
backup-manager create <name> <source> <destination>
```
Creates a new backup from source to destination.

**Examples:**
```bash
# Backup home directory
backup-manager create home /Users/pp /Volumes/Backup/home

# Backup documents
backup-manager create documents ~/Documents /Volumes/Backup/docs

# Backup to network location
backup-manager create server ~/Documents /mnt/server/backup
```

### Check Status
```bash
backup-manager status
```
Shows backup status including:
- Time Machine status
- Last backup times
- Disk space availability
- Configured backup destinations

### Restore from Backup
```bash
backup-manager restore <source> <destination>
```
Restores files from a backup location to a destination.

**Examples:**
```bash
backup-manager restore /Volumes/Backup/home /Users/pp
```

### Schedule Backups
```bash
# List scheduled backups
backup-manager schedule list

# Add a schedule (cron expression)
backup-manager schedule add <backup-name> "<cron>"

# Remove a schedule
backup-manager schedule remove <backup-name>
```

**Cron Examples:**
```bash
# Daily at 2 AM
backup-manager schedule add daily-home '0 2 * * *'

# Weekly on Sundays at 3 AM
backup-manager schedule add weekly-docs '0 3 * * 0'

# Every 6 hours
backup-manager schedule add frequent '0 */6 * * *'
```

### Cloud Backup (rclone)
```bash
# Check cloud status
backup-manager cloud status

# Sync to cloud
backup-manager cloud sync <remote-name> <local-path>
```

**Rclone Examples:**
```bash
# Configure a remote (run once)
rclone config

# Sync local folder to Google Drive
backup-manager cloud sync mydrive /Users/pp/Backup

# Sync to S3
backup-manager cloud sync s3-backup /Users/pp/Backup
```

## Configuration

The configuration file is stored at:
```
~/.config/openclaw/backups.json
```

**Structure:**
```json
{
  "backups": [
    {
      "name": "home",
      "source": "/Users/pp",
      "destination": "/Volumes/Backup/home",
      "last_run": "2024-01-15T02:00:00-08:00"
    }
  ],
  "schedules": [
    {
      "name": "schedule-1",
      "backup_name": "home",
      "cron": "0 2 * * *"
    }
  ],
  "cloud": {
    "rclone": {
      "enabled": false,
      "remote": ""
    }
  }
}
```

## Requirements

The skill uses these macOS/Unix tools (installed by default on macOS):
- **rsync** - File synchronization
- **tmutil** - Time Machine (macOS)
- **diskutil** - Disk management (macOS)
- **jq** - JSON parsing
- **rclone** - Cloud sync (optional, install via `brew install rclone`)

If a tool is missing, the skill handles it gracefully and provides warnings.

## Features

1. **Time Machine Integration** - Detects and manages Time Machine backups
2. **Rsync Backups** - Efficient incremental backups using rsync
3. **Cron Scheduling** - Schedule recurring backups via cron
4. **Cloud Support** - rclone integration for cloud backups (S3, GDrive, etc.)
5. **Config Management** - JSON-based configuration with backup history

## Notes

- Backups are incremental by default (rsync -a)
- The skill prompts for confirmation before restoring
- Use absolute paths for reliability
- Ensure backup destinations have sufficient disk space
