---
name: llm-regression-monitor
description: Use this skill when the user wants to monitor LLM behavior over time and get alerted when outputs change unexpectedly. Triggers on requests like "set up LLM regression monitoring", "alert me when my prompts start behaving differently", "watch my LLM for regressions", "run behavioral tests on my AI outputs on a schedule", or "detect when my model starts drifting". Handles first-time setup, baseline capture, scheduled monitoring, and alert configuration via WhatsApp, Slack, Discord, or email.
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "optionalEnv":
          [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "OLLAMA_BASE_URL",
            "CUSTOM_LLM_BASE_URL",
            "CUSTOM_LLM_API_KEY",
            "ALERT_WHATSAPP_TO",
            "ALERT_SLACK_WEBHOOK",
            "ALERT_DISCORD_WEBHOOK",
            "ALERT_EMAIL_TO",
            "ALERT_EMAIL_FROM",
            "ALERT_EMAIL_PASSWORD",
            "ALERT_EMAIL_SMTP",
            "ALERT_EMAIL_PORT",
          ],
        "primaryEnv": "OPENAI_API_KEY",
      },
  }
---

# LLM Regression Monitor

## Overview

Automated behavioral regression monitoring for LLM apps. Captures baseline outputs, detects drift on a schedule, and fires WhatsApp or Slack alerts the moment something regresses.

---

## Workflow Decision Tree

```
User request
├── "set up monitoring" / first time    → Full Setup (steps 1–5)
├── "run the monitor now"               → Step 4 only
├── "I changed my prompt/model"         → Step 3b (update baseline)
└── "configure alerts"                  → Step 5
```

---

## Step 1 — Install

```bash
pip install llm-behave[semantic] pyyaml requests python-dotenv
```

---

## Step 2 — Create test_suite.yaml

Create in the project root. Minimal example:

```yaml
tests:
  - name: support_response
    prompt: "A customer says they never received their order. How do you respond?"
    provider: openai        # openai | anthropic | ollama | custom
    model: gpt-4o-mini
    assertions:
      - type: tone
        expected: "empathetic"
    drift:
      enabled: true
      threshold: 0.80
```

Set the API key for the chosen provider:
```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...   # if using anthropic
# ollama needs no key
```

Read `references/test-suite-format.md` for the full field spec.
Read `references/providers.md` for env vars and Ollama setup.

---

## Step 3 — Capture Baselines

```bash
python scripts/capture_baseline.py
```

Saves ground-truth outputs to `.llm_behave_baselines/`. Run once before monitoring begins.

For more reliable baselines on important tests, set `baseline_samples: 3` in `test_suite.yaml` — the script will call the LLM 3 times and save the most representative response, eliminating outliers.

To test real production behavior, add a `system_prompt` field to your test — it gets sent to the LLM exactly as in your app.

### 3b — Update after intentional prompt/model change

```bash
# Reset one test
python scripts/capture_baseline.py --update-baseline <test-name>

# Reset all
python scripts/capture_baseline.py --force
```

---

## Step 4 — Run the Monitor

```bash
python scripts/run_monitor.py
```

Writes `monitor_report.json`. Exits 0 on all-pass, 1 on any failure (CI-compatible).

---

## Step 4b — Track Trends (Predictive Alerts)

Run after each monitor run to log scores and detect gradual drift before it crosses the threshold:

```bash
python scripts/trend_tracker.py
```

Appends each run's scores to `monitor_trend.jsonl`. If a test's drift score has been declining for the last 5 runs and is within 0.10 of the threshold, it prints a warning. Exit code 2 = trend warning, 0 = all clear.

The daily schedule command (Step 6) already includes it:
```
python run_monitor.py; python trend_tracker.py; python send_alert.py
```

---

## Step 5 — Configure Alerts

Set whichever channels you want in `.env` — scripts load it automatically.

```bash
# WhatsApp (requires wacli installed and logged in)
ALERT_WHATSAPP_TO="+1234567890"

# Slack
ALERT_SLACK_WEBHOOK="https://hooks.slack.com/services/..."

# Discord
ALERT_DISCORD_WEBHOOK="https://discord.com/api/webhooks/..."

# Email (Gmail example — use an App Password, not your main password)
ALERT_EMAIL_TO="you@example.com"
ALERT_EMAIL_FROM="sender@gmail.com"
ALERT_EMAIL_PASSWORD="your-app-password"
# Optional — defaults to smtp.gmail.com:587
# ALERT_EMAIL_SMTP="smtp.gmail.com"
# ALERT_EMAIL_PORT="587"
```

You can set any combination — all configured channels fire on failure. Send via:
```bash
python scripts/send_alert.py
```

Silent on green runs. Logs every alert to `monitor_alerts.log` regardless.

---

## Step 6 — Schedule with OpenClaw Cron

Confirm the schedule with the user (default: 9am daily), then add:

- **Schedule:** `0 9 * * *`
- **Command:** `python run_monitor.py; python trend_tracker.py; python send_alert.py`
- **Directory:** project root (where `test_suite.yaml` lives)

All three scripts run every day regardless of pass/fail. `send_alert.py` reads both `monitor_report.json` (hard failures) and `trend_warnings.json` (predictive warnings from `trend_tracker.py`) — it fires alerts only when there is something to report, and stays silent on fully green runs.

---

## Common Errors

| Error | Fix |
|---|---|
| `llm-behave is not installed` | `pip install llm-behave[semantic]` |
| `OPENAI_API_KEY is not set` | Export key or add to `.env` |
| `No baseline found` | Run step 3 first |
| `test_suite.yaml not found` | Create it in project root |
| LLM call errors in report | API issue — not a regression |
