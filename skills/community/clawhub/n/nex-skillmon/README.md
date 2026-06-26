# Nex SkillMon

**Skill Health & Cost Monitor** - Meta-tool for OpenClaw power users. Monitor and optimize your entire skill ecosystem.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT--0-green)
![Python](https://img.shields.io/badge/python-3.9+-blue)

## Overview

Nex SkillMon is a comprehensive monitoring and analytics tool for OpenClaw skill users. Track which skills you have installed, monitor their API costs, detect stale/unused skills, check for security vulnerabilities, and manage your entire skill ecosystem.

Perfect for users with dozens of installed skills who need visibility into:
- Which skills are being used and which are dormant
- API costs and token usage per skill
- Security flags and integrity changes
- Available updates and deprecated skills
- Overall skill ecosystem health

## Features

### Core Monitoring
- **Skill Discovery**: Automatically discover and scan all installed skills
- **Health Scoring**: Comprehensive health metric (0-100) for each skill based on usage, errors, and staleness
- **Usage Tracking**: Track trigger count, duration, token usage, and success rate per skill
- **Cost Analytics**: Monitor estimated API costs with breakdown by skill and model

### Security & Integrity
- **Security Flags**: Check for flagged skills on ClawHub API
- **File Integrity**: Detect unauthorized modifications with SHA256 hashing
- **Vulnerability Checks**: Monitor for known vulnerabilities and deprecated skills
- **Alert Management**: Unacknowledged alerts for critical issues

### Cost Management
- **Real-time Cost Tracking**: Estimate costs based on tokens and model pricing
- **Budget Alerts**: Set monthly budgets and receive notifications when exceeded
- **Cost Trends**: Analyze spending patterns over time
- **Cost Breakdown**: View costs by skill, model, and time period

### Stale Skill Detection
- **Identify Unused Skills**: Find skills not triggered in 30+ days
- **Last Usage Tracking**: See when each skill was last executed
- **Staleness Scoring**: Factor staleness into overall health score

### Update Management
- **Update Detection**: Check for newer versions on ClawHub
- **Changelog Tracking**: View what's new in available updates
- **Version Comparison**: Semantic version parsing and comparison

## Installation

### Quick Start

```bash
# Clone or navigate to skill directory
cd nex-skillmon

# Run setup
bash setup.sh

# Scan your installed skills
nex-skillmon scan

# View health dashboard
nex-skillmon health
```

### System Requirements

- **Python 3.9+** (no external dependencies - stdlib only)
- **Linux, macOS, or Windows**
- **~2MB disk space** for database and logs

### Data Location

All data is stored locally in your home directory:

```
~/.nex-skillmon/
├── skillmon.db          # SQLite database
├── logs/
│   └── nex-skillmon.log # Application logs
└── .env                 # Configuration (optional)
```

## Usage

### Dashboard & Monitoring

```bash
# Health dashboard with scores and trends
nex-skillmon health

# Run comprehensive health checks on all skills
nex-skillmon check

# Check specific skill
nex-skillmon check --skill "nex-life-logger"

# Show detailed skill information
nex-skillmon show "skill-name"
```

### Cost & Usage

```bash
# Cost overview (this month)
nex-skillmon cost

# Cost trend (weekly breakdown)
nex-skillmon cost --period weekly

# Usage statistics
nex-skillmon usage

# Usage for specific skill
nex-skillmon usage --skill "nex-crm"

# Budget management
nex-skillmon budget                    # Check budget
nex-skillmon budget --set 50           # Set monthly budget (€50)
```

### Security & Updates

```bash
# Security alerts
nex-skillmon alerts

# All alerts (including acknowledged)
nex-skillmon alerts --all

# Acknowledge an alert
nex-skillmon acknowledge 42

# Check for updates
nex-skillmon updates

# Security scan
nex-skillmon security
```

### Skill Management

```bash
# List all skills
nex-skillmon list

# List active skills only
nex-skillmon list --status active

# Show stale skills (30+ days unused)
nex-skillmon stale

# Show flagged skills
nex-skillmon list --flagged

# Scan for new skills
nex-skillmon scan
```

### Reporting & Export

```bash
# Export as JSON
nex-skillmon export --format json --period monthly

# Export as markdown
nex-skillmon export --format markdown

# Configuration
nex-skillmon config
nex-skillmon config --set SKILLS_BASE_DIR /custom/skills/path
```

## Dashboard Example

```
Skill Health Dashboard
---
Score  Skill              Triggers  Cost/mo  Last Used    Status
 95    nex-life-logger    1,245     €2.34    2 hours ago  OK
 90    nex-crm             342      €0.89    1 day ago    OK
 85    nex-einvoice          47     €0.12    3 days ago   OK
 60    nex-healthcheck       89     €0.00    5 days ago   OK
 30    telegram-bot          12     €0.45    28 days ago  STALE
 10    old-skill              0     €0.00    45 days ago  STALE
  0    flagged-plugin         3     €1.20    2 days ago   FLAGGED
---
Total skills: 7 | Active: 4 | Stale: 2 | Flagged: 1
This month: €5.00 | Budget: €50.00 (10% used)
```

## Configuration

### Environment Variables

Set in `~/.nex-skillmon/.env`:

```bash
# Custom skills directory
SKILLS_BASE_DIR=/path/to/skills

# ClawHub API URL
CLAWHUB_API_URL=https://api.clawhub.dev

# Logging level
LOG_LEVEL=INFO

# Currency (EUR, USD, GBP, JPY)
CURRENCY=EUR
```

### Cost Tracking

Built-in costs for common models:

| Model | Cost |
|-------|------|
| gpt-4o | $0.0025 per 1k tokens |
| gpt-4o-mini | $0.00015 per 1k tokens |
| claude-3-sonnet | €0.003 per 1k tokens |
| claude-haiku | €0.00025 per 1k tokens |
| gemini-1.5-pro | $0.00125 per 1k tokens |

Add custom models via `lib/config.py`.

### Health Score Calculation

Health score (0-100) is calculated based on:

- **Staleness** (30+ days unused): -40 points
- **Error Rate**: -20 points max
- **Security Flags**: -25 points
- **Recent Activity**: +10-20 points

## Database Schema

### skills
- `id`, `name` (unique), `version`, `install_date`, `last_updated`, `last_triggered`
- `trigger_count`, `skill_path`, `file_hash`, `description`, `author`, `homepage`
- `status` (active/disabled/flagged/removed), `tags`, `notes`, `created_at`

### usage_log
- `id`, `skill_id` (FK), `triggered_at`, `duration_ms`, `tokens_used`, `model_used`
- `estimated_cost`, `success` (bool), `error_message`

### cost_summary
- `id`, `skill_id` (FK), `period` (daily/weekly/monthly), `period_start`
- `total_triggers`, `total_tokens`, `total_cost`, `avg_duration_ms`, `success_rate`

### security_checks
- `id`, `skill_id` (FK), `check_type`, `severity`, `details`, `checked_at`, `acknowledged`

## Performance

Optimized for fast queries:

- **Indices** on frequently queried columns (status, skill_id, triggered_at, etc.)
- **Lazy loading** of usage logs to reduce memory footprint
- **Efficient aggregation** of costs and statistics
- **Fast health score** calculation with minimal database overhead

## Privacy & Security

- **Local Storage**: All data stored locally on your machine
- **No Cloud Sync**: Optional ClawHub API integration (check for flags/updates)
- **No Tracking**: No telemetry or usage tracking
- **Data Isolation**: Each user has separate data directory

## Troubleshooting

### "Skills directory not found"

Set `SKILLS_BASE_DIR` environment variable:

```bash
export SKILLS_BASE_DIR=/path/to/openclaw/skills
```

### "Python 3 not found"

Install Python 3.9+ from https://python.org

### API calls failing

Disable ClawHub checks by setting:

```bash
export CLAWHUB_API_URL=""
```

## Development

### File Structure

```
nex-skillmon/
├── SKILL.md                 # Skill definition
├── README.md                # This file
├── LICENSE.txt              # MIT-0 license
├── setup.sh                 # Installation script
├── nex-skillmon.py          # Main CLI
└── lib/
    ├── __init__.py
    ├── config.py            # Configuration
    ├── storage.py           # Database layer
    ├── cost_tracker.py      # Cost analytics
    └── scanner.py           # Skill discovery
```

### Testing

Manual testing steps:

```bash
# Setup
bash setup.sh

# Scan
python3 nex-skillmon.py scan

# List
python3 nex-skillmon.py list

# Health
python3 nex-skillmon.py health

# Cost
python3 nex-skillmon.py cost

# Stale
python3 nex-skillmon.py stale
```

## License

MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

See `LICENSE.txt` for details.

## Support

For issues, feature requests, or questions:

- Visit: https://nex-ai.be
- Author: Kevin Blancaflor (Nex AI)

---

**[Nex SkillMon by Nex AI | nex-ai.be]**
