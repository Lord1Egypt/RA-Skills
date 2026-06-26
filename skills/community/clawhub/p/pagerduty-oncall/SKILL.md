---
name: pagerduty-oncall
description: "Manage PagerDuty incidents, on-call schedules, escalation policies, and services via the PagerDuty REST API. Use when you need to: (1) List or acknowledge active incidents, (2) Trigger or resolve incidents, (3) Check who is on-call right now, (4) View escalation policies, (5) Manage PagerDuty services, (6) Get incident timelines or notes, (7) Snooze or reassign incidents, (8) Run PagerDuty operations from the agent. Requires PAGERDUTY_API_KEY env var."
---

# PagerDuty On-Call Skill

Manage incidents and on-call operations via the PagerDuty REST API (v2).

## Setup

```bash
export PAGERDUTY_API_KEY="your-api-key-here"
# Optional: set default email for actions that require it
export PAGERDUTY_FROM_EMAIL="oncall@yourcompany.com"
```

Get your API key: PagerDuty → User Icon → My Profile → User Settings → API Access Keys → Create New API Key

## Core Workflows

### List Active Incidents

```bash
python3 ~/.openclaw/workspace/skills/pagerduty-oncall/scripts/pd.py incidents --status triggered,acknowledged
```

### Acknowledge an Incident

```bash
python3 ~/.openclaw/workspace/skills/pagerduty-oncall/scripts/pd.py acknowledge --id P1234AB
```

### Resolve an Incident

```bash
python3 ~/.openclaw/workspace/skills/pagerduty-oncall/scripts/pd.py resolve --id P1234AB
```

### Trigger a New Incident

```bash
python3 ~/.openclaw/workspace/skills/pagerduty-oncall/scripts/pd.py trigger \
  --service-key "your-service-integration-key" \
  --description "Database is down" \
  --severity critical
```

### Who is On-Call Right Now?

```bash
python3 ~/.openclaw/workspace/skills/pagerduty-oncall/scripts/pd.py oncall
# With schedule filter:
python3 ~/.openclaw/workspace/skills/pagerduty-oncall/scripts/pd.py oncall --schedule-id PABC123
```

### Get Incident Details

```bash
python3 ~/.openclaw/workspace/skills/pagerduty-oncall/scripts/pd.py get --id P1234AB
```

### List Services

```bash
python3 ~/.openclaw/workspace/skills/pagerduty-oncall/scripts/pd.py services
```

### List Escalation Policies

```bash
python3 ~/.openclaw/workspace/skills/pagerduty-oncall/scripts/pd.py escalations
```

### Add Note to Incident

```bash
python3 ~/.openclaw/workspace/skills/pagerduty-oncall/scripts/pd.py note --id P1234AB --message "Investigating DB failover"
```

### Snooze Incident

```bash
python3 ~/.openclaw/workspace/skills/pagerduty-oncall/scripts/pd.py snooze --id P1234AB --duration 3600
```

### Reassign Incident

```bash
python3 ~/.openclaw/workspace/skills/pagerduty-oncall/scripts/pd.py reassign --id P1234AB --user-id PU12345
```

## Direct API Calls (Advanced)

For operations not covered by the script, use curl directly:

```bash
curl -s -H "Authorization: Token token=$PAGERDUTY_API_KEY" \
  -H "Accept: application/vnd.pagerduty+json;version=2" \
  "https://api.pagerduty.com/incidents?statuses[]=triggered&limit=25"
```

## Key Concepts

- **Incidents**: The core alert object. States: `triggered` → `acknowledged` → `resolved`
- **Services**: Represent monitored systems/applications
- **Escalation Policies**: Define who gets paged and when
- **Schedules**: Define on-call rotation rotations
- **Integration Keys**: Service-specific keys for triggering incidents

## Common Tasks for Agents

- Morning standup briefing: run `incidents` to check overnight alerts
- On-call handoff: `oncall` + `incidents` for current state
- Post-incident: `get` for timeline, then `note` to document RCA
- Auto-acknowledge low-severity pages: `incidents` filtered by urgency, then `acknowledge`

## API Rate Limits

- 900 requests/minute for REST API
- Events API (triggering): 120 events/minute per service
- Use `--limit` flag to control result set size
