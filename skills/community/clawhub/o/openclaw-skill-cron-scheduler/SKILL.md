---
name: cron-scheduler
description: Manage cron jobs on macOS/Linux - list, add, remove, backup, and schedule recurring tasks
triggers:
  - "cron"
  - "cron job"
  - "schedule task"
  - "recurring task"
  - "crontab"
commands:
  list:
    usage: cron-scheduler list
    description: List all cron jobs for current user
  add:
    usage: cron-scheduler add "<schedule>" "<command>"
    description: Add a new cron job with schedule validation
  remove:
    usage: cron-scheduler remove <line_number>
    description: Remove a cron job by line number
  remove-pattern:
    usage: cron-scheduler removep <pattern>
    description: Remove cron jobs matching a pattern
  edit:
    usage: cron-scheduler edit
    description: Open crontab in default editor
  next:
    usage: cron-scheduler next
    description: Show next run times for all jobs
  backup:
    usage: cron-scheduler backup
    description: Backup current crontab to ~/.cron-backups/
  restore:
    usage: cron-scheduler restore [backup_file]
    description: Restore crontab from backup (lists available if no file)
  service:
    usage: cron-scheduler service <start|stop|status>
    description: Enable/disable or check cron service status
  templates:
    usage: cron-scheduler templates
    description: Show common cron job schedule templates
---

# Cron Scheduler Skill

A comprehensive skill for managing cron jobs on both macOS and Linux systems.

## Features

1. **List Jobs** - View all cron jobs for the current user
2. **Add Job** - Create new cron jobs with schedule validation
3. **Remove Job** - Delete jobs by line number or pattern
4. **Edit Crontab** - Open crontab in your default editor
5. **Next Runs** - See when each job will execute next
6. **Backup/Restore** - Safely backup and restore crontab configurations
7. **Service Control** - Start/stop/status of cron daemon
8. **Templates** - Common schedule patterns for quick setup

## Requirements

- `crontab` command (pre-installed on macOS/Linux)
- `bash` shell
- Optional: `cronnext` for accurate next-run predictions (Linux)

## Installation

```bash
# Make the script executable
chmod +x ~/.openclaw/workspace/skills/cron-scheduler/scripts/cron-helper.sh

# Optional: Add to PATH
echo 'export PATH="$HOME/.openclaw/workspace/skills/cron-scheduler/scripts:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Usage

### List all cron jobs
```bash
cron-scheduler list
# or
cron-scheduler l
```

### Add a new cron job
```bash
# Daily backup at 2am
cron-scheduler add "0 2 * * *" "~/scripts/backup.sh"

# Every hour
cron-scheduler add "0 * * * *" "~/scripts/hourly-task.sh"

# Every 5 minutes
cron-scheduler add "*/5 * * * *" "~/scripts/monitor.sh"
```

### Remove cron jobs
```bash
# By line number (use 'list' first to see line numbers)
cron-scheduler remove 3

# By pattern (matches anywhere in the line)
cron-scheduler removep "backup"
```

### Edit crontab directly
```bash
cron-scheduler edit
# or
cron-scheduler e
```

### Show next run times
```bash
cron-scheduler next
# or
cron-scheduler n
```

### Backup and restore
```bash
# Create backup
cron-scheduler backup

# List available backups
cron-scheduler restore

# Restore specific backup
cron-scheduler restore ~/.cron-backups/crontab_20240315_143022.bak
```

### Manage cron service
```bash
# Check status
cron-scheduler service status

# Start cron (may require sudo)
cron-scheduler service start

# Stop cron (may require sudo)
cron-scheduler service stop
```

### View templates
```bash
cron-scheduler templates
# or
cron-scheduler t
```

## Cron Schedule Format

```
┌──────────── minute (0 - 59)
│ ┌────────── hour (0 - 23)
│ │ ┌──────── day of month (1 - 31)
│ │ │ ┌------ month (1 - 12)
│ │ │ │ ┌---- day of week (0 - 6, Sunday=0)
* * * * *
```

### Common Examples

| Schedule | Description |
|----------|-------------|
| `0 0 * * *` | Daily at midnight |
| `0 2 * * *` | Daily at 2am |
| `0 * * * *` | Every hour |
| `*/5 * * * *` | Every 5 minutes |
| `0 9 * * 1-5` | Weekdays at 9am |
| `0 0 * * 0` | Weekly on Sunday |
| `0 0 1 * *` | Monthly on 1st |

## Platform Support

- **macOS**: Uses `launchctl` for service management
- **Linux**: Uses `systemctl` for service management

## Safety Features

- Temporary files used for atomic crontab modifications
- Backup created before any destructive operations
- Confirmation prompt before restore
- Schedule validation before adding jobs
