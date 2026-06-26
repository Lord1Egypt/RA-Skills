---
name: oura-ring
description: |
  What: Query Oura Ring health data — sleep, readiness, activity, heart rate, and trends via the Oura API v2.
  When: User asks about their sleep, readiness, activity, heart rate, health trends, or wants a daily health briefing.
  Triggers: oura, sleep score, readiness, activity score, heart rate, HRV, health briefing, ring data
version: 1.0.0
license: MIT
---

# Oura Ring Skill

Query Oura Ring health data via the Oura API v2. Requires a personal access token at `~/.config/oura/credentials.json`.

## Setup

```json
// ~/.config/oura/credentials.json
{"personal_access_token": "YOUR_TOKEN", "base_url": "https://api.ouraring.com/v2"}
```

Get your token at https://cloud.ouraring.com/personal-access-tokens

## Commands

All commands use: `/opt/homebrew/bin/python3.11 <skill_dir>/scripts/oura_api.py <command> [args]`

### `status`
Connection test + personal info (age, email, biological sex).

### `briefing`
Today's combined readiness + sleep + activity summary. Best for morning check-ins.

### `sleep [YYYY-MM-DD]`
Detailed sleep data: duration, stages, efficiency, HRV, temperature. Defaults to last night.

### `readiness [YYYY-MM-DD]`
Readiness score with all contributors (HRV balance, body temp, recovery, sleep, activity). Defaults to today.

### `activity [YYYY-MM-DD]`
Activity details: steps, calories, active time, movement breakdown. Defaults to today.

### `heartrate [hours]`
Recent heart rate statistics (min, max, avg, latest). Default: last 4 hours.

### `trends [days]`
Multi-day trend view of readiness, sleep, and activity scores. Default: 7 days.

## Health Alerts

Standalone alert checker for heartbeats/crons:

```
/opt/homebrew/bin/python3.11 <skill_dir>/scripts/health_alerts.py
```

Outputs one line per alert. Empty output = nothing notable. Exit code 0 always.

Checks:
- Readiness < 70
- Sleep < 6 hours
- HRV trending down 3+ days
- Resting HR spike > 5bpm above 7-day average
- Body temperature deviation > 0.5°C
- Recovery index < 30

## Output Format

All output is human-readable text with emoji indicators:
- 🟢 Good (score ≥ 85)
- 🟡 Fair (score 70–84)
- 🔴 Needs attention (score < 70)

## Error Handling

- Exit code 0: success
- Exit code 1: error (message on stderr)
- Common errors: missing credentials file, invalid token, no data for date
