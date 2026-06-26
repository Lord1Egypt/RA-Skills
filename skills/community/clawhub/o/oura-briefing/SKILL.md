---
name: oura-briefing
description: Fetch and summarize Oura Ring v2 sleep, readiness, and activity data. Use when the user asks about their sleep score, HRV, readiness, recovery, or Oura metrics. Delivers a concise daily health briefing. Requires OURA_API_TOKEN set in the environment or passed via --token.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl", "jq"] },
      },
  }
---

# Oura Briefing

Fetch and summarize daily health metrics from the Oura Ring API (v2).

## Setup

Set your Oura Personal Access Token:

```bash
export OURA_API_TOKEN="your_token_here"
```

Get a token at: https://cloud.ouraring.com/personal-access-tokens

## Usage

```bash
# Today's briefing
bash scripts/oura-briefing.sh

# Specific date
bash scripts/oura-briefing.sh --date 2024-01-15

# JSON output
bash scripts/oura-briefing.sh --json

# Use a token directly
bash scripts/oura-briefing.sh --token YOUR_TOKEN
```

## What it returns

- **Sleep:** total sleep, efficiency, deep/REM/light breakdown, latency, wake time, score
- **Readiness:** readiness score, HRV balance, body temperature deviation, recovery index
- **Activity:** activity score, steps, active calories, equivalent walking distance

## Agent guidance

When a user asks about sleep, readiness, HRV, or recovery:
1. Run `bash scripts/oura-briefing.sh` (requires OURA_API_TOKEN in environment)
2. Parse the output and present a plain-language summary
3. Flag anything below their normal range (sleep < 70, readiness < 70, HRV drop > 15%)
4. Suggest actionable adjustments if scores are low (bedtime, wind-down, recovery day)

## Wake detection

The script exits 0 with a `wake_confirmed` field when the user has woken up today (bedtime_end present in latest long_sleep session). Use this as a gate before sending morning reports.

```bash
bash scripts/oura-briefing.sh --wake-check
# exit 0 = awake, exit 1 = not yet
```
