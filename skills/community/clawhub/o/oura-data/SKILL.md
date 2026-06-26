---
name: oura-data
description: |
  Fetch the user's personal Oura Ring health data via the official Oura API v2,
  using the zero-dependency `oura-cli` Python tool. Use this skill when the user
  asks about their sleep (score, total/deep/REM/light duration, efficiency,
  bedtime, HRV, resting heart rate), daily readiness, activity (steps, calories,
  walking distance), heart rate, workouts, blood oxygen (SpO2), stress levels,
  body temperature deviation, or any other biometric tracked by their Oura Ring.
  Also use when the user asks "how did I sleep", "am I recovered", "should I
  push hard today", "should I rest", or wants historical data for specific dates
  or date ranges. Assumes `oura-cli` is cloned locally and OAuth-authorized; if
  not, the skill provides setup instructions.
version: 1.0.0
metadata: {"clawdbot": {"emoji": "💍", "requires": {"bins": ["uv"]}, "category": "health"}}
---

# Oura Ring — Personal Health Data

Query your Oura Ring sleep, readiness, activity, HRV, and biometric data via the official Oura API v2. Wraps the zero-dependency [`oura-cli`](https://github.com/zqchris/oura-cli) Python tool — no Node, no Docker, no SaaS middleman, no telemetry. Your tokens stay on your machine.

- **Source**: https://github.com/zqchris/oura-cli
- **Oura API docs**: https://cloud.ouraring.com/v2/docs
- **License**: MIT-0

## What this skill unlocks

Once installed, your assistant can answer questions like:

- "How did I sleep last night?" → fetches sleep score, deep/REM/light breakdown, HRV, bedtime
- "Am I recovered enough for a hard workout today?" → fetches readiness, grounds the recommendation
- "What was my HRV trend last week?" → fetches a 7-day range
- "Did my deep sleep improve since I cut alcohol?" → compares date ranges
- "Why was my readiness low on March 12?" → fetches that day's contributors (temperature deviation, prior activity, recovery index, etc.)
- "Show me every workout this month" → fetches the workout endpoint

The skill does **not** invent numbers — every answer is grounded in a live API call.

## Prerequisites

This skill assumes [`oura-cli`](https://github.com/zqchris/oura-cli) is cloned and OAuth-authorized locally. If commands fail with `No tokens found` or `config.json not found`, **walk the user through setup** — do not attempt to resolve automatically:

```bash
# 1. Clone the repo (one-time)
git clone https://github.com/zqchris/oura-cli ~/oura-cli
cd ~/oura-cli

# 2. Register an Oura API app at:
#    https://cloud.ouraring.com  →  My Applications  →  New Application
#    - Redirect URI: http://localhost:8080/callback
#    - Scopes: enable all

# 3. Authorize (opens browser; one-time per machine)
uv run oauth-authorize.py --client-id <ID> --client-secret <SECRET>

# 4. Verify
uv run oura-data.py today
```

After first auth, tokens auto-refresh on HTTP 401. No manual renewal needed.

## Quick Reference

All commands run from inside the `oura-cli` directory:

```bash
uv run oura-data.py <subcommand> [--date YYYY-MM-DD | --start ... --end ...]
```

### Subcommands

| Subcommand | Returns |
|---|---|
| `today` / `daily` | Sleep + Activity + Readiness combined for today (or `--date`) |
| `sleep` | Score, total/deep/REM/light durations, efficiency, bedtime, avg/lowest HR, HRV |
| `activity` | Score, steps, active/total calories, walking distance |
| `readiness` | Score, temperature deviation, score contributors |
| `heartrate` | Min/max/avg BPM, sample count |
| `workout` | Auto-detected and manual workouts (raw JSON) |
| `spo2` | Blood oxygen during sleep (raw JSON) |
| `stress` | Stress levels (raw JSON) |
| `ring` | Ring configuration & battery level |
| `personal` | Age, weight, height, biological sex |

### Date arguments (all data commands except `ring` and `personal`)

```
--date YYYY-MM-DD                       # single day (default: today)
--start YYYY-MM-DD --end YYYY-MM-DD     # date range (any length)
```

## Common Patterns

```bash
# Today's full summary (sleep + activity + readiness)
uv run oura-data.py today

# Yesterday's sleep detail
uv run oura-data.py sleep --date $(date -v -1d +%Y-%m-%d)

# Last 7 days of readiness
uv run oura-data.py readiness \
  --start $(date -v -7d +%Y-%m-%d) \
  --end   $(date +%Y-%m-%d)

# Sleep on a specific date
uv run oura-data.py sleep --date 2026-03-15

# Activity for a full month
uv run oura-data.py activity --start 2026-04-01 --end 2026-04-30

# Workouts this week
uv run oura-data.py workout \
  --start $(date -v -7d +%Y-%m-%d) \
  --end   $(date +%Y-%m-%d)
```

For a Linux `date` equivalent, replace `-v -7d` with `-d "7 days ago"`.

## Interpreting Output

### Scores (0–100, Oura's proprietary scoring)

| Band | Meaning | Suggested response |
|---|---|---|
| 85+ | Optimal | Green light for hard training / demanding work |
| 70–84 | Good | Normal day; no special caveats |
| 60–69 | Fair | Suggest moderate intensity; recommend earlier bedtime |
| < 60 | Poor | **Actively suggest rest** if user asks "should I push?" |

### Temperature deviation (°C from user's 14-day baseline)

- **+0.3 °C or more**: possible illness, overtraining, alcohol the night before, or warm sleeping environment
- **Strongly negative**: can correlate with cycle phases for menstruating users
- **< ±0.2 °C**: noise; don't over-interpret

### HRV (RMSSD, milliseconds)

Higher = better autonomic recovery. **Always compare to the user's own trend**, never to absolute population numbers — individual baselines vary 20–200ms.

### Heart rate

- "Lowest HR" during sleep is the most reliable recovery marker
- Resting HR rising 5+ bpm over baseline often precedes illness 24–48h before symptoms

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `No tokens found` | OAuth not yet completed | Run `oauth-authorize.py` (see Prerequisites) |
| `config.json not found` | Refresh credentials missing | Re-run `oauth-authorize.py` |
| `API error 401` (after auto-refresh) | Refresh token revoked or expired | Re-run `oauth-authorize.py` |
| `API error 429` | Rate-limited (Oura cap: 5000/day) | Wait and retry |
| `API error 426` | Subscription required for this endpoint | Tell user the endpoint needs Oura membership |
| No data for a recent date | Ring hasn't synced yet | Ask user to open the Oura app on their phone |
| Empty `data` array | No measurement on that date | Likely ring wasn't worn |

## Critical Rules

1. **Never read, print, or echo `tokens.json` or `config.json`** — they contain OAuth secrets and client credentials.
2. **Always run from the `oura-cli` directory** — token files are resolved relative to the script.
3. **Don't fabricate numbers.** If the user asks about a date you haven't queried, run the command — don't infer from earlier context.
4. **For "should I push hard today" style questions**, always fetch `today` first and ground recommendations in the actual readiness score and HRV.
5. **Respect privacy.** This is the user's personal health data. Don't persist it to memory, send it to external systems, or include it in unrelated tool calls unless the user explicitly asks.
6. **Don't medicalize.** Report data and trends; do not diagnose. If the user asks medical questions, recommend they consult a clinician.

## Reference Files

- [`references/api-reference.md`](references/api-reference.md) — full Oura API v2 endpoint dictionary, scopes, rate limits
- [`references/example-outputs.md`](references/example-outputs.md) — real sample outputs for each subcommand
