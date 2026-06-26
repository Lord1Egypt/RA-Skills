# Cron Scheduler

A cross-platform skill for managing cron jobs on macOS and Linux.

## Features

- ✅ List all cron jobs
- ✅ Add new jobs with validation
- ✅ Remove jobs by line number or pattern
- ✅ Edit crontab directly
- ✅ Show next run times
- ✅ Backup and restore
- ✅ Service management (start/stop/status)
- ✅ Common templates

## Quick Start

```bash
# Navigate to the skill directory
cd ~/.openclaw/workspace/skills/cron-scheduler

# Make the script executable
chmod +x scripts/cron-helper.sh

# List your cron jobs
./scripts/cron-helper.sh list

# Add a daily backup job
./scripts/cron-helper.sh add "0 2 * * *" "~/scripts/backup.sh"

# View templates
./scripts/cron-helper.sh templates
```

## Requirements

- macOS or Linux
- `bash` shell
- `crontab` command (pre-installed)

## Installation

### Option 1: Direct execution
```bash
~/.openclaw/workspace/skills/cron-scheduler/scripts/cron-helper.sh <command>
```

### Option 2: Add to PATH
Add to your `~/.zshrc` or `~/.bashrc`:
```bash
export CRON_SCHEDULER="$HOME/.openclaw/workspace/skills/cron-scheduler/scripts"
export PATH="$CRON_SCHEDULER:$PATH"
```

Then use: `cron-helper.sh <command>`

### Option 3: Create an alias
```bash
alias cron='~/.openclaw/workspace/skills/cron-scheduler/scripts/cron-helper.sh'
```

## Commands

| Command | Description |
|---------|-------------|
| `list` | List all cron jobs |
| `add <schedule> <cmd>` | Add new cron job |
| `remove <line#>` | Remove job by line |
| `removep <pattern>` | Remove by pattern |
| `edit` | Open crontab editor |
| `next` | Show next run times |
| `backup` | Backup crontab |
| `restore [file]` | Restore from backup |
| `service <action>` | Start/stop/status |
| `templates` | Show common schedules |

## Examples

```bash
# Daily at 2am
cron-helper.sh add "0 2 * * *" "~/scripts/backup.sh"

# Every hour
cron-helper.sh add "0 * * * *" "~/sync.sh"

# Every 5 minutes
cron-helper.sh add "*/5 * * * *" "~/monitor.sh"

# Weekdays at 5pm
cron-helper.sh add "0 17 * * 1-5" "~/after-work.sh"
```

## Cron Format

```
* * * * *
| | | | |
| | | | +-- Day of week (0-6, Sunday=0)
| | | +---- Month (1-12)
| | +------ Day (1-31)
| +-------- Hour (0-23)
+---------- Minute (0-59)
```

## Backup Location

Backups are stored in: `~/.cron-backups/`

Files are named: `crontab_YYYYMMDD_HHMMSS.bak`

## Platform-Specific

- **macOS**: Uses `launchctl` for service control
- **Linux**: Uses `systemctl` for service control

## License

MIT License - See LICENSE file for details.

## Author

Created for OpenClaw skill system.
