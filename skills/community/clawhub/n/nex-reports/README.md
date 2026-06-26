# Nex Reports

**Scheduled Report Generator** - Create, schedule, and deliver automated reports combining data from multiple Nex tools and services.

A meta-skill that chains other tools (nex-healthcheck, nex-crm, nex-expenses, nex-deliverables, nex-domains, nex-vault) and compiles results into formatted reports delivered via Telegram or saved to disk.

## Features

- **Multiple Data Sources** - Combine health checks, CRM pipeline, expenses, deliverables, domains, vault alerts in one report
- **Flexible Scheduling** - Cron expressions or preset schedules (daily, weekly, monthly)
- **Multiple Formats** - Markdown, HTML, Telegram, or JSON output
- **Multiple Targets** - Save to file, send to Telegram, or both
- **Email Integration** - Check unread emails via IMAP
- **Calendar Support** - Parse ICS files for upcoming events
- **Task Tracking** - Read JSON taskboard files for open tasks
- **Custom Commands** - Run arbitrary shell commands in reports
- **Run History** - Track all report runs and their results
- **Easy Management** - Create, edit, delete, and test reports via CLI

## Installation

```bash
bash setup.sh
```

This will:
1. Check for Python 3.9+
2. Create data directory (~/.nex-reports/)
3. Install CLI command (nex-reports)
4. Initialize SQLite database
5. Check for optional nex-* tools

## Quick Start

### List available modules

```bash
nex-reports modules
```

### Create your first report

```bash
nex-reports create "Monday Morning" \
  --schedule "0 8 * * 1" \
  --modules health,crm,deliverables,domains \
  --output markdown
```

### Run the report

```bash
nex-reports run "Monday Morning"
```

### View the report

```bash
nex-reports show "Monday Morning"
```

## Commands

### Creating Reports

```bash
nex-reports create <name> \
  --schedule <cron or preset> \
  --modules <module1,module2,...> \
  --output <format> \
  --output-target <target>
```

Schedule presets: `DAILY_MORNING`, `DAILY_EVENING`, `WEEKLY_MONDAY`, `WEEKLY_FRIDAY`, `MONTHLY_FIRST`

Output formats: `markdown`, `html`, `telegram`, `json`

Output targets: `file`, `telegram`, `both`

### Managing Reports

```bash
nex-reports list                    # List all reports
nex-reports show <name>             # Show config and last run
nex-reports edit <name> [options]   # Edit report
nex-reports delete <name>           # Delete report
nex-reports history <name> [--limit] # View run history
```

### Running Reports

```bash
nex-reports run <name>    # Run specific report
nex-reports run --all     # Run all enabled reports
```

### Testing

```bash
nex-reports modules       # List all modules
nex-reports test <module> # Test single module
```

## Available Modules

| Module | Description | Requires |
|--------|-------------|----------|
| EMAIL | Check unread emails | IMAP credentials |
| CALENDAR | Parse ICS calendar file | ICS file path |
| TASKS | Read JSON taskboard | taskboard.json file |
| HEALTH | System health check | nex-healthcheck |
| CRM | Sales pipeline | nex-crm |
| EXPENSES | Monthly expenses | nex-expenses |
| DELIVERABLES | Overdue items | nex-deliverables |
| DOMAINS | Expiring domains | nex-domains |
| VAULT | Security alerts | nex-vault |
| CUSTOM | Arbitrary command | Shell command string |

## Configuration

Set environment variables to configure integrations:

```bash
# IMAP (for EMAIL module)
export IMAP_HOST=imap.gmail.com
export IMAP_USER=you@gmail.com
export IMAP_PASS=app-password
export IMAP_PORT=993

# Telegram
export TELEGRAM_TOKEN=your-bot-token
export TELEGRAM_CHAT_ID=your-chat-id
```

## Data Storage

All data stored in `~/.nex-reports/`:

- `reports.db` - SQLite database (configs, run history)
- `reports/` - Generated report files
- `templates/` - (Reserved for future use)

## Examples

### Daily Standup (Telegram)

```bash
nex-reports create "Daily Standup" \
  --schedule "0 9 * * 1-5" \
  --modules health,crm,deliverables \
  --output telegram \
  --output-target telegram
```

Runs every weekday at 9 AM, sends to Telegram.

### Weekly Executive Summary (Markdown)

```bash
nex-reports create "Weekly Executive" \
  --schedule WEEKLY_FRIDAY \
  --modules health,crm,expenses,deliverables,domains,vault \
  --output markdown \
  --output-target file
```

Runs every Friday, saves markdown to file.

### Custom Health Report

```bash
nex-reports create "Git Status Report" \
  --schedule "0 10 * * *" \
  --modules custom \
  --output markdown
```

Then configure custom command for module.

## Scheduling

Reports are created with cron expressions, but nex-reports doesn't run them automatically. Set up your system scheduler:

### Using crontab (Unix/Linux/Mac)

```bash
# Add to crontab -e
0 9 * * * /home/user/.local/bin/nex-reports run "Daily Standup"
```

### Using systemd timer (Linux)

Create `/etc/systemd/user/nex-reports-daily.service`:

```ini
[Unit]
Description=Nex Reports Daily Standup

[Service]
Type=oneshot
ExecStart=%h/.local/bin/nex-reports run "Daily Standup"
```

Create `/etc/systemd/user/nex-reports-daily.timer`:

```ini
[Unit]
Description=Nex Reports Daily Standup Timer

[Timer]
OnCalendar=Mon-Fri 09:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:

```bash
systemctl --user enable --now nex-reports-daily.timer
```

### Using Windows Task Scheduler

Create a scheduled task running:

```
python C:\path\to\nex-reports\nex-reports.py run "My Report"
```

## Database Schema

### report_configs

Stores report configurations:

- `id` - Primary key
- `name` - Unique report name
- `schedule` - Cron expression
- `modules` - JSON list of module configs
- `output_format` - Output format (telegram, markdown, html, json)
- `output_target` - Where to send (file, telegram, both)
- `enabled` - Whether to run automatically
- `last_run` - ISO timestamp of last execution
- `created_at`, `updated_at` - Timestamps

### report_runs

Tracks report execution history:

- `id` - Primary key
- `config_id` - Reference to report_configs
- `started_at` - Execution start time
- `completed_at` - Execution completion time
- `status` - success, partial (some modules failed), or failed
- `output_path` - Path to saved report file
- `module_results` - JSON results from all modules
- `errors` - JSON dict of module errors

## Dependencies

- Python 3.9+
- Standard library only (imaplib, sqlite3, json, subprocess)
- Optional nex-* tools for specific modules

## License

MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Free for any use without conditions or attribution.

---

**Nex Reports by Nex AI** | [nex-ai.be](https://nex-ai.be)
