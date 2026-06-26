# Use Case: Health Anomaly Alerts

Proactively detect unusual patterns in your health data and get notified before small
issues become bigger ones. Your agent checks key metrics a few times a day and messages
you if something looks off.

---

## What Gets Monitored

| Alert | Trigger condition | Suggested action |
|-------|------------------|-----------------|
| 🔴 **Elevated resting HR** | Today's `RestingHeartRate` ≥ 1.15× 30-day baseline | Rest, check hydration, rule out illness |
| 💛 **Low HRV** | Last night's sleep-window HRV ≤ 0.75× 30-day baseline | Reduce training load, prioritise sleep |
| 😴 **Short sleep** | Total asleep duration < 5.5 h | Adjust schedule; flag if it repeats 3 nights in a row |
| 🚶 **Very low steps** | Daily `StepCount` < 1000 by 8 PM | Check if you are unwell or unusually sedentary |
| 💓 **High active HR** | `HeartRate` > 180 bpm with no recent workout context | Could indicate arrhythmia — flag for follow-up |

Thresholds are intentionally conservative to avoid alert fatigue. Tune them to your own
normal ranges once you have a few weeks of baseline data.

---

## Cron Job Setup

Ask your OpenClaw agent to create the cron job:

> "Set up a health anomaly check that runs three times a day and alerts me on Discord
> if any of my key health metrics look unusual."

Or configure it manually:

### 1. Add the cron to `openclaw.json`

```json
{
  "cron": {
    "jobs": [
      {
        "id": "health-alerts-morning",
        "schedule": "0 8 * * *",
        "task": "health-anomaly-check",
        "agentId": "main",
        "enabled": true
      },
      {
        "id": "health-alerts-afternoon",
        "schedule": "0 14 * * *",
        "task": "health-anomaly-check",
        "agentId": "main",
        "enabled": true
      },
      {
        "id": "health-alerts-evening",
        "schedule": "0 20 * * *",
        "task": "health-anomaly-check",
        "agentId": "main",
        "enabled": true
      }
    ]
  }
}
```

### 2. Add the task prompt

```json
{
  "tasks": {
    "health-anomaly-check": {
      "prompt": "Run a health anomaly check using health-data.jsonl. For each check below, compare today's value against the 30-day rolling baseline. Only alert if a threshold is exceeded — stay silent otherwise (do not send 'all clear' messages).\n\nChecks:\n1. RestingHeartRate: alert if today's value >= 1.15x baseline\n2. HRV (sleep window only): alert if last night's mean SDNN <= 0.75x baseline\n3. Sleep duration: alert if last night's total asleep time < 5.5 hours\n4. StepCount: alert if it's after 20:00 and today's total < 1000 steps\n5. HeartRate spikes: alert if any reading > 180 bpm without a workout record nearby (±30 min)\n\nFor each triggered alert, send a short message on Discord with: the metric, the actual value, the baseline, and a one-line suggested action. Group multiple alerts into a single message."
    }
  }
}
```

> **Important:** The prompt tells the agent to stay silent when everything is normal.
> This prevents noisy "all clear" messages cluttering your chat three times a day.

### 3. Verify

```bash
# List registered crons
openclaw cron list

# Trigger manually to test (will alert only if thresholds are breached)
openclaw cron run health-alerts-morning
```

---

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `HEALTHCLAW_DATA_DIR` | platform default | Path to `health-data.jsonl` |
| `ALERT_BASELINE_DAYS` | `30` | Rolling window for personal baseline |
| `ALERT_RHR_MULTIPLIER` | `1.15` | RHR alert threshold (× baseline) |
| `ALERT_HRV_MULTIPLIER` | `0.75` | HRV alert threshold (× baseline) |
| `ALERT_SLEEP_MIN_HOURS` | `5.5` | Minimum sleep before alert |
| `ALERT_STEPS_MIN` | `1000` | Step count floor (checked after 8 PM) |
| `ALERT_NOTIFY_CHANNEL` | `discord` | Notification channel |

---

## Example Alert

> ⚠️ **Health check — 2 anomalies detected**
>
> 🔴 **Resting HR**: 62 bpm (baseline 52 bpm, +19%) — May indicate early illness or
> under-recovery. Consider a rest day.
>
> 💛 **HRV**: 28 ms last night (baseline 44 ms, −36%) — Significant drop. Avoid
> intense training; prioritise sleep tonight.

---

## Tips

- **Wait for baseline.** Alerts are only meaningful after ~2 weeks of data. Before
  that, the rolling average is too short and may produce false positives.
- **Tune thresholds gradually.** Start with the defaults; tighten them once you know
  your normal ranges.
- **Combine with recovery score.** A low recovery score + an active alert is a strong
  signal — take it seriously.
