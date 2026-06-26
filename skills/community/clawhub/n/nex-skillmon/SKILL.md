---
name: nex-skillmon
description: Health monitoring and cost optimization tool for OpenClaw skill ecosystems and power users managing multiple skills. Track all installed skills with real-time health scoring, detect stale skills (unused for 30+ days), identify skills with security flags or vulnerabilities, and monitor for available updates. View comprehensive cost dashboards showing API usage, estimated monthly costs, and spending per skill to identify expensive skills and optimize budget allocation. Set monthly cost budgets and receive alerts when approaching limits. Scan skill installation directories to discover all active skills and build baseline health metrics. Perform security checks for file integrity, vulnerability detection, and suspicious patterns. View usage statistics including trigger counts, execution duration, success rates, and trends over time. Generate detailed reports in markdown or JSON format for stakeholder communication and compliance documentation. Perfect for power users, development teams, and organizations managing complex skill infrastructures who need visibility into skill health, costs, and security posture.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "\U0001F50D"
    requires:
      bins:
        - python3
      env:
        - CLAWHUB_API_URL
        - SKILLS_BASE_DIR
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-skillmon.py"
      - "lib/*"
      - "setup.sh"
---

# Nex SkillMon

Skill Health & Cost Monitor - meta-tool for OpenClaw power users. Monitor installed skills, track API costs, detect stale skills, check security flags, and manage your skill ecosystem.

## When to Use

Use this skill when the user asks about:

- Which skills they have installed and their health status
- Cost tracking and which skills are most expensive
- API costs and token usage per skill
- Skills that haven't been used recently (stale skills)
- Security flags, vulnerabilities, or integrity issues with skills
- Available updates for installed skills
- Overall skill ecosystem health and usage patterns
- Deprecated or removed skills
- Skill performance metrics and trends
- Monthly budget tracking and spending
- Skill usage statistics over time
- Exporting skill reports and analytics

Trigger phrases: "skill monitor", "which skills", "skill costs", "expensive skills", "stale skills", "security flags", "skill updates", "skill health", "API costs", "token usage", "skill report", "skill ecosystem", "monitor my skills", "what skills am I using"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory, initializes the database, and sets up the monitoring environment.

## Available Commands

### Basic Information

- **scan** - Discover and scan all installed skills
  ```bash
  nex-skillmon scan
  ```

- **list** - List skills with filters
  ```bash
  nex-skillmon list                    # All skills
  nex-skillmon list --status active    # Active only
  nex-skillmon list --stale            # Stale skills (unused 30+ days)
  nex-skillmon list --flagged          # Flagged/security issues
  ```

- **show** - Show detailed skill information
  ```bash
  nex-skillmon show "skill-name"
  ```

### Monitoring & Health

- **health** - Health dashboard with scores
  ```bash
  nex-skillmon health
  ```

- **check** - Run comprehensive health checks
  ```bash
  nex-skillmon check                        # All skills
  nex-skillmon check --skill "skill-name"   # Specific skill
  ```

- **security** - Security scan
  ```bash
  nex-skillmon security
  ```

- **stale** - Show unused/stale skills
  ```bash
  nex-skillmon stale
  ```

- **updates** - Check for available updates
  ```bash
  nex-skillmon updates
  ```

### Cost & Usage

- **cost** - Cost overview
  ```bash
  nex-skillmon cost                        # This month
  nex-skillmon cost --period weekly --last 4   # Last 4 weeks
  nex-skillmon cost --skill "skill-name"  # Specific skill
  ```

- **usage** - Usage statistics
  ```bash
  nex-skillmon usage
  nex-skillmon usage --skill "skill-name"
  ```

- **budget** - Budget management
  ```bash
  nex-skillmon budget                # Check current budget
  nex-skillmon budget --set 50       # Set monthly budget (€)
  nex-skillmon budget --currency usd # Set currency
  ```

### Alerts & Configuration

- **alerts** - Show security/cost alerts
  ```bash
  nex-skillmon alerts
  nex-skillmon alerts --unacknowledged
  ```

- **acknowledge** - Acknowledge an alert
  ```bash
  nex-skillmon acknowledge 42
  ```

- **export** - Export report as markdown or JSON
  ```bash
  nex-skillmon export --format json --period monthly
  nex-skillmon export --format markdown
  ```

- **config** - Configuration management
  ```bash
  nex-skillmon config                    # Show config
  nex-skillmon config --set SKILLS_BASE_DIR /path/to/skills
  ```

## Dashboard Output Example

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

## Features

- **Real-time Monitoring**: Scan installed skills and track their status
- **Cost Tracking**: Monitor API usage and estimated costs per skill
- **Security Checks**: Detect flagged skills, file integrity changes, and vulnerabilities
- **Health Scoring**: Comprehensive skill health metric (0-100) based on usage, errors, and staleness
- **Update Detection**: Check for available updates on ClawHub
- **Stale Detection**: Identify skills not used in N days
- **Usage Analytics**: Track triggers, duration, success rate per skill
- **Budget Alerts**: Set monthly budgets and get cost alerts
- **Report Export**: Export detailed reports in markdown or JSON format

## Data Storage

All data is stored locally in `~/.nex-skillmon/`:

- **skillmon.db** - SQLite database with skills, usage logs, and security checks
- **logs/** - Application logs
- **.env** - Configuration (SKILLS_BASE_DIR, API credentials, etc.)

## Configuration

Key environment variables can be set in `~/.nex-skillmon/.env`:

```
SKILLS_BASE_DIR=/path/to/skills
CLAWHUB_API_URL=https://api.clawhub.dev
LOG_LEVEL=INFO
CURRENCY=EUR
```

## Security & Privacy

- All skill data is stored locally on your machine
- Security checks query ClawHub API for known vulnerabilities (can be disabled)
- File integrity verification uses local hashing
- No personal data is sent to external services without your configuration

## Requirements

- Python 3.9+
- Standard library only (urllib, sqlite3, etc.)

## License

MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
