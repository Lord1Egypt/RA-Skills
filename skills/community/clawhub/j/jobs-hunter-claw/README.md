# Jobs Hunter Claw 🎯

Unified job hunting automation with Google Sheets — discover jobs, submit applications, and track your pipeline with activity logging.

**ClawHub:** https://clawhub.ai/QuantDeveloperUSA/jobs-hunter-claw

## Features

- **Job Discovery** — Add jobs from LinkedIn, Indeed, recruiter emails
- **Application Tracking** — Track status through the pipeline
- **Activity Logging** — Timestamped history of all events
- **Search & Filter** — Regex and fuzzy search across your pipeline
- **Google Sheets Integration** — Single source of truth with form UI
- **Cron Automation** — Periodic email scans, pipeline reviews

## Installation

### ClawHub (Recommended)

```bash
clawhub install jobs-hunter-claw
chmod +x /path/to/skills/jobs-hunter-claw/scripts/job-tracker.sh
```

### Git

```bash
git clone https://github.com/ABFS-Inc/jobs-hunter-claw.git
```

## Configuration

**Required:** Set your Google Sheet ID as an environment variable:

```bash
export JOB_TRACKER_SPREADSHEET_ID="your-google-sheet-id"
```

The ID is found in your Google Sheet URL:
```
https://docs.google.com/spreadsheets/d/[THIS-IS-THE-ID]/edit
```

## Quick Start

```bash
# Set spreadsheet ID
export JOB_TRACKER_SPREADSHEET_ID="your-sheet-id"

# Add a job
./scripts/job-tracker.sh add --company "Morgan Stanley" --role "AI Architect" --source LinkedIn

# List interviews
./scripts/job-tracker.sh list --status interview

# Log activity
./scripts/job-tracker.sh log JOB002 --event interview_scheduled --details "3rd round Monday"

# Search
./scripts/job-tracker.sh search "citi" --columns company
```

## Requirements

- [gog CLI](https://gogcli.sh) — Google Sheets access
- Google Sheet with Jobs, Activity Log tabs
- OpenClaw (for agent/cron features)

## Documentation

See [SKILL.md](SKILL.md) for complete documentation including:
- Detailed setup instructions
- Agent configuration
- Cron job examples
- CLI reference
- Validation rules

## License

MIT
