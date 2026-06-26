# Use Case: Daily Recovery Score

Calculate a 0–100 recovery score each morning based on last night's HRV, resting heart
rate, and sleep data. Your agent will message you the score and a brief interpretation
before you start your day.

---

## How the Score Works

Recovery is computed from three signals measured **during or immediately after sleep**:

| Signal | Source field | Weight | Direction |
|--------|-------------|--------|-----------|
| HRV (SDNN) | `HeartRateVariabilitySDNN` during sleep window | 50% | Higher = better |
| Resting HR | `RestingHeartRate` (Apple's daily value) | 30% | Lower = better |
| Sleep duration | `SleepAnalysis` (asleep stages) | 20% | More = better |

> **Why these rules matter:**
> - Use **`RestingHeartRate`** only — Apple computes this once per day with a proprietary
>   algorithm. Do NOT average raw `HeartRate` readings; they run higher and produce
>   misleading results.
> - HRV must be filtered to the **sleep window only** (`SleepAnalysis` startDate →
>   endDate). Daytime HRV readings are 20–30 ms lower and will drag the score down
>   artificially.

### Scoring formula

Each signal is normalised against a rolling 30-day personal baseline, then blended:

```
hrv_score  = clamp((hrv_tonight / hrv_baseline) * 100, 0, 100)
rhr_score  = clamp((2 - rhr_tonight / rhr_baseline) * 100, 0, 100)
sleep_score = clamp((sleep_hours / 8) * 100, 0, 100)

recovery = round(hrv_score * 0.5 + rhr_score * 0.3 + sleep_score * 0.2)
```

### Interpretation

| Score | Label | Suggested action |
|-------|-------|-----------------|
| 80–100 | 🟢 Recovered | Ready for hard training or demanding work |
| 60–79  | 🟡 Moderate | Normal day; avoid maximal effort |
| 40–59  | 🟠 Fatigued | Light activity only; prioritise rest |
| 0–39   | 🔴 Low | Rest day; investigate sleep quality |

---

## Cron Job Setup

Ask your OpenClaw agent to create the cron job:

> "Add a cron job that runs every morning at 7 AM to calculate my recovery score from
> last night's health data and message me the result."

Or configure it manually:

### 1. Add the cron to `openclaw.json`

```json
{
  "cron": {
    "jobs": [
      {
        "id": "recovery-score",
        "schedule": "0 7 * * *",
        "task": "recovery-score-daily",
        "agentId": "main",
        "enabled": true
      }
    ]
  }
}
```

### 2. Add the task prompt

Create or update your agent's cron task definitions:

```json
{
  "tasks": {
    "recovery-score-daily": {
      "prompt": "Calculate my recovery score for today using the health data in health-data.jsonl. Steps:\n1. Find last night's sleep window from SleepAnalysis records (most recent InBed/Asleep session)\n2. Extract HeartRateVariabilitySDNN readings within that sleep window and compute the mean\n3. Get today's RestingHeartRate value\n4. Calculate total sleep duration from Asleep stage records\n5. Compute a 30-day rolling baseline for HRV and RHR\n6. Apply the formula: recovery = hrv_score*0.5 + rhr_score*0.3 + sleep_score*0.2\n7. Send me the score, the three component values, and a one-sentence interpretation via Discord"
    }
  }
}
```

### 3. Verify

```bash
# Check the cron is registered
openclaw cron list

# Trigger manually to test
openclaw cron run recovery-score
```

---

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `HEALTHCLAW_DATA_DIR` | platform default | Path to `health-data.jsonl` |
| `RECOVERY_BASELINE_DAYS` | `30` | Rolling window for personal baseline |
| `RECOVERY_SLEEP_TARGET_HRS` | `8` | Sleep target for 100% sleep score |
| `RECOVERY_NOTIFY_CHANNEL` | `discord` | Channel for morning message |

Set these as environment variables or agent config before the cron runs.

---

## Example Output

> 🟡 **Recovery: 68 / 100** — Moderate
>
> HRV: 42 ms (baseline 51 ms) · RHR: 52 bpm (baseline 50 bpm) · Sleep: 6.8 h
>
> You're a bit below baseline. Fine for a normal day — skip high-intensity training.
