---
name: llm-regression-monitor
description: Use this skill when the user wants to monitor LLM behavior over time and get alerted when outputs change unexpectedly. Triggers on requests like "set up LLM regression monitoring", "alert me when my prompts start behaving differently", "watch my LLM for regressions", "run behavioral tests on my AI outputs on a schedule", or "detect when my model starts drifting". Handles first-time setup, baseline capture, scheduled monitoring, and alert configuration.
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
pip install llm-behave[semantic] pyyaml requests
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

## Step 5 — Configure Alerts

```bash
# WhatsApp (requires wacli installed and logged in)
export ALERT_WHATSAPP_TO="+1234567890"

# Slack
export ALERT_SLACK_WEBHOOK="https://hooks.slack.com/services/..."
```

Add to `.env` in project root — scripts load it automatically. Send via:
```bash
python scripts/send_alert.py
```

Silent on green runs. Logs every alert to `monitor_alerts.log` regardless.

---

## Step 6 — Schedule with OpenClaw Cron

Confirm the schedule with the user (default: 9am daily), then add:

- **Schedule:** `0 9 * * *`
- **Command:** `python run_monitor.py && true || python send_alert.py`
- **Directory:** project root (where `test_suite.yaml` lives)

The `|| send_alert.py` fires only when `run_monitor.py` exits 1 (failures found).

---

## Common Errors

| Error | Fix |
|---|---|
| `llm-behave is not installed` | `pip install llm-behave[semantic]` |
| `OPENAI_API_KEY is not set` | Export key or add to `.env` |
| `No baseline found` | Run step 3 first |
| `test_suite.yaml not found` | Create it in project root |
| LLM call errors in report | API issue — not a regression |
