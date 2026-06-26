# 🟣 Oura Ring Skill for OpenClaw

Query your Oura Ring health data directly from your AI agent. Sleep, readiness, activity, heart rate, trends, and health alerts — all via the Oura API v2.

## Setup

### 1. Get a Personal Access Token

1. Go to [cloud.ouraring.com](https://cloud.ouraring.com/personal-access-tokens)
2. Sign in with your Oura account
3. Click **Create New Personal Access Token**
4. Copy the token

### 2. Save Credentials

```bash
mkdir -p ~/.config/oura
cat > ~/.config/oura/credentials.json << 'EOF'
{
  "personal_access_token": "YOUR_TOKEN_HERE",
  "base_url": "https://api.ouraring.com/v2"
}
EOF
chmod 600 ~/.config/oura/credentials.json
```

### 3. Verify

Ask your agent: *"Check my Oura status"*

Or run directly:
```bash
/opt/homebrew/bin/python3.11 scripts/oura_api.py status
```

## Commands

| Command | Description |
|---------|-------------|
| `oura status` | Connection test + personal info |
| `oura briefing` | Today's readiness + sleep + activity summary |
| `oura sleep [date]` | Detailed sleep data (stages, HRV, efficiency) |
| `oura readiness [date]` | Readiness score + all contributors |
| `oura activity [date]` | Steps, calories, movement breakdown |
| `oura heartrate [hours]` | Recent HR stats (default: 4 hours) |
| `oura trends [days]` | Multi-day score trends (default: 7 days) |

Dates use `YYYY-MM-DD` format. All default to today/last night.

## Health Alerts

The alert checker runs standalone and outputs warnings for:

- 🔴 Readiness score < 70
- 🔴 Sleep under 6 hours
- 🔴 HRV declining 3+ consecutive days
- 🔴 Resting HR spike > 5bpm above 7-day average
- 🔴 Body temperature deviation > 0.5°C
- 🔴 Recovery index < 30

```bash
/opt/homebrew/bin/python3.11 scripts/health_alerts.py
```

No output = nothing notable. Designed for heartbeats and cron jobs.

## Data Accessed

This skill reads (never writes) the following from your Oura account:

- **Personal Info** — age, sex, email, weight, height
- **Daily Readiness** — readiness score, HRV balance, recovery, temperature
- **Daily Sleep** — sleep score, duration, efficiency, stages
- **Daily Activity** — steps, calories, active time, movement
- **Heart Rate** — continuous HR readings
- **Sleep Sessions** — detailed per-session data (HRV, stages, timing)

## Requirements

- Python 3.11+ (uses only stdlib — no pip install needed)
- Oura Ring with active cloud sync
- Personal access token from cloud.ouraring.com

## Privacy

🔒 **Your data stays local.** This skill communicates only with the official Oura API (`api.ouraring.com`). No data is sent to third parties, cached, or stored anywhere other than Oura's own servers. Your access token never leaves your machine.

## License

MIT
