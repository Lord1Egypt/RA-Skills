---
name: nex-reports
description: Automated report generation and scheduling meta-skill that aggregates data from multiple Nex tools into unified, actionable business briefings for day-to-day decision making. Create custom composite reports combining curated data from nex-healthcheck (infrastructure uptime and service health), nex-crm (sales pipeline status and hot prospects), nex-expenses (spending patterns and budget tracking), nex-deliverables (project progress and overdue items), nex-domains (domain expiry alerts and SSL certificate warnings), and nex-vault (contract expirations and renewal deadlines). Schedule reports to run fully automatically on recurring schedules (daily, weekly, monthly) using standard cron expressions and pre-built convenient presets (DAILY_MORNING at 8am, WEEKLY_MONDAY, WEEKLY_FRIDAY, MONTHLY_FIRST). Generate morning briefings for team standups, weekly summaries for stakeholder reviews, or monthly business reviews for strategic planning in multiple output formats (markdown for email with professional formatting, simple HTML, compact Telegram format with emojis, structured JSON for API integration). Route report delivery via Telegram for instant mobile notifications and team alerts or save generated reports to files for email distribution, client sharing, and documentation archives. Perfect for Belgian agency operators, business owners, and management teams who need daily or weekly snapshots of overall business health without manual data compilation overhead.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "📋"
    requires:
      bins:
        - python3
      env:
        - IMAP_HOST
        - IMAP_USER
        - IMAP_PASS
        - IMAP_PORT
        - TELEGRAM_TOKEN
        - TELEGRAM_CHAT_ID
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-reports.py"
      - "lib/*"
      - "setup.sh"
---

# Nex Reports

Scheduled Report Generator - Create, schedule, and deliver automated reports combining data from multiple Nex tools.

## When to Use

Use this skill when the user asks about:

- Creating automated reports (daily, weekly, monthly)
- Morning briefings or weekly summaries
- Scheduling reports for specific times
- Combining multiple data sources into one report
- Getting health checks, CRM pipeline, expenses, deliverables in one place
- Email notifications or Telegram updates
- Report templates and presets
- Overdue items, expiring domains, vault alerts in one view
- Custom automated reporting
- Report history or viewing past reports

Trigger phrases: "create a report", "morning briefing", "weekly summary", "schedule a report", "automated report", "report briefing", "compile data", "overzicht", "samenvatting", "dagrapport", "wekelijk rapport"

## Quick Start

```bash
bash setup.sh
```

This creates the data directory, initializes the database, and checks for nex-* command availability.

## Commands

### Create a Report

```bash
nex-reports create "Monday Morning" \
  --schedule "0 8 * * 1" \
  --modules health,crm,deliverables,domains \
  --output markdown \
  --output-target file
```

Schedule presets: `DAILY_MORNING`, `DAILY_EVENING`, `WEEKLY_MONDAY`, `WEEKLY_FRIDAY`, `MONTHLY_FIRST`

### Run a Report

```bash
nex-reports run "Monday Morning"
nex-reports run --all
```

### Manage Configs

```bash
nex-reports list
nex-reports show "Monday Morning"
nex-reports edit "Monday Morning" --modules health,crm,expenses
nex-reports delete "Monday Morning"
```

### View History

```bash
nex-reports history "Monday Morning" --limit 20
```

### Test Modules

```bash
nex-reports modules
nex-reports test health
```

## Available Modules

- **EMAIL** - Check unread emails via IMAP
- **CALENDAR** - Parse ICS calendar file
- **TASKS** - Read JSON taskboard file
- **HEALTH** - Run `nex-healthcheck check`
- **CRM** - Run `nex-crm pipeline`
- **EXPENSES** - Run `nex-expenses summary monthly`
- **DELIVERABLES** - Run `nex-deliverables overdue`
- **DOMAINS** - Run `nex-domains expiring`
- **VAULT** - Run `nex-vault alerts`
- **CUSTOM** - Run arbitrary shell command

## Output Formats

- **markdown** - Full markdown report for documents/email
- **html** - Simple HTML report
- **telegram** - Compact Telegram format with emojis
- **json** - JSON structured data

## Output Targets

- **file** - Save to disk (~/.nex-reports/reports/)
- **telegram** - Send to Telegram (requires TELEGRAM_TOKEN and TELEGRAM_CHAT_ID)
- **both** - Save and send to Telegram

## Configuration

Set via environment variables:

```bash
export IMAP_HOST=imap.gmail.com
export IMAP_USER=your.email@gmail.com
export IMAP_PASS=your-app-password
export IMAP_PORT=993

export TELEGRAM_TOKEN=your-bot-token
export TELEGRAM_CHAT_ID=your-chat-id
```

## Data Directory

Reports and database stored in: `~/.nex-reports/`

- `reports.db` - SQLite database
- `reports/` - Generated report files
- `templates/` - (Reserved for future use)

## Examples

Morning briefing combining health, CRM, and deliverables:

```bash
nex-reports create "Daily Standup" \
  --schedule "0 9 * * 1-5" \
  --modules health,crm,deliverables \
  --output telegram \
  --output-target telegram
```

Weekly summary to file (every Friday 5pm):

```bash
nex-reports create "Weekly Summary" \
  --schedule WEEKLY_FRIDAY \
  --modules health,crm,expenses,deliverables,domains,vault \
  --output markdown \
  --output-target file
```

Custom command in report:

```bash
nex-reports create "Git Status" \
  --schedule "0 10 * * *" \
  --modules custom \
  --output markdown
```

View the last run:

```bash
nex-reports show "Daily Standup"
```

## Scheduling

Reports are created with cron expressions. Use an external scheduler (systemd timer, crontab, etc.) to execute:

```bash
nex-reports run "Daily Standup"
```

on a schedule.

---

**Nex Reports by Nex AI** | [nex-ai.be](https://nex-ai.be)
