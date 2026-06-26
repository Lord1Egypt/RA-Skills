---
name: nightscout-local
description: Read glucose data from a Nightscout site. Use when the user asks for the current CGM reading, trend, recent readings, or Nightscout status. This skill is read-only and should not be used for portal login automation or write actions.
---

# Nightscout Local

Use this skill for **read-only Nightscout data access**.

Set the Nightscout base URL with either:
- environment variable: `NIGHTSCOUT_BASE_URL`
- command flag: `--url https://your-site.example/`

Supported tasks:
- get current glucose from Nightscout
- get recent readings
- check basic Nightscout site status/config

## Commands

Current reading:

```bash
NIGHTSCOUT_BASE_URL="https://your-site.example/" \
python3 /Users/serveradmin/.openclaw/workspace/skills/nightscout-local/scripts/nightscout_read.py current
```

Simple command path for later automation/use:

```bash
python3 /Users/serveradmin/.openclaw/workspace/scripts/current_bg.py
```

Recent readings:

```bash
NIGHTSCOUT_BASE_URL="https://your-site.example/" \
python3 /Users/serveradmin/.openclaw/workspace/skills/nightscout-local/scripts/nightscout_read.py recent 6
```

Site status:

```bash
NIGHTSCOUT_BASE_URL="https://your-site.example/" \
python3 /Users/serveradmin/.openclaw/workspace/skills/nightscout-local/scripts/nightscout_read.py status
```

## Output guidance

- Report glucose in **mg/dL**.
- Include trend/direction when available.
- Include the reading timestamp in America/Los_Angeles.
- Keep medical wording careful: report readings clearly, but do not claim to provide medical advice.

## Guardrails

- Read-only only.
- Do not modify Nightscout settings.
- Do not infer treatment recommendations unless Martin explicitly asks for interpretation.
- If the endpoint is unavailable, report that plainly.
