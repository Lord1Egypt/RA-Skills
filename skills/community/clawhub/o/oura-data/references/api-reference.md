# Oura API v2 — Reference

Companion reference for the `oura` skill. Covers the full Oura API v2 surface so the LLM can answer questions beyond the common subcommand path.

Official docs: https://cloud.ouraring.com/v2/docs

## Endpoint map

`oura-cli` covers the most common endpoints. The Oura API exposes more — listed here for completeness so the assistant can suggest `curl` or extend the CLI when a question exceeds the built-in subcommands.

### Daily summary endpoints

| Endpoint | CLI subcommand | What it returns |
|---|---|---|
| `/v2/usercollection/daily_sleep` | `sleep` (daily score side) | Score 0–100, score contributors |
| `/v2/usercollection/sleep` | `sleep` (detail side) | Per-sleep-period: total/deep/REM/light, efficiency, bedtime, HR, HRV |
| `/v2/usercollection/daily_activity` | `activity` | Score, steps, calories, walking distance |
| `/v2/usercollection/daily_readiness` | `readiness` | Score, temp deviation, contributors |
| `/v2/usercollection/daily_spo2` | `spo2` | Average SpO2 during sleep |
| `/v2/usercollection/daily_stress` | `stress` | Stress and recovery time during day |
| `/v2/usercollection/daily_resilience` | _(not in CLI)_ | Long-term resilience score |
| `/v2/usercollection/daily_cardiovascular_age` | _(not in CLI)_ | Estimated cardiovascular age |
| `/v2/usercollection/vO2_max` | _(not in CLI)_ | VO2 max estimate |

### Time-series endpoints

| Endpoint | CLI subcommand | What it returns |
|---|---|---|
| `/v2/usercollection/heartrate` | `heartrate` | 5-min HR samples (no SpO2-style daily aggregate) |
| `/v2/usercollection/workout` | `workout` | Workouts (auto-detected + manual) |
| `/v2/usercollection/session` | _(not in CLI)_ | Meditation, breathwork, etc. |
| `/v2/usercollection/tag` | _(not in CLI)_ | Deprecated, see `enhanced_tag` |
| `/v2/usercollection/enhanced_tag` | _(not in CLI)_ | User-tagged events (illness, alcohol, etc.) |

### User info endpoints

| Endpoint | CLI subcommand |
|---|---|
| `/v2/usercollection/personal_info` | `personal` |
| `/v2/usercollection/ring_configuration` | `ring` |

## Score contributors

Both **sleep** and **readiness** scores expose `contributors` (0–100 each). These are the most useful subscore signals.

### Sleep contributors
- `deep_sleep` — minutes of deep sleep relative to user norm
- `efficiency` — sleep efficiency %
- `latency` — minutes to fall asleep (shorter is better, up to a point)
- `rem_sleep` — minutes of REM
- `restfulness` — wake-ups and movement
- `timing` — alignment with circadian midpoint
- `total_sleep` — total sleep duration

### Readiness contributors
- `activity_balance` — recent training load
- `body_temperature` — temp deviation flag
- `hrv_balance` — HRV vs baseline
- `previous_day_activity` — yesterday's load
- `previous_night` — last night's sleep quality
- `recovery_index` — overnight HR recovery
- `resting_heart_rate` — RHR vs baseline
- `sleep_balance` — running sleep debt

When the user asks "why was my readiness low?" — look at which contributor dropped most.

## OAuth scopes

The skill's `oauth-authorize.py` requests all scopes by default. Reference for completeness:

| Scope | Endpoints unlocked |
|---|---|
| `personal` | `personal_info` |
| `email` | email field in user info |
| `daily` | all daily summary endpoints |
| `heartrate` | `heartrate` |
| `workout` | `workout` |
| `tag` | `enhanced_tag` |
| `session` | `session` |
| `spo2` | `daily_spo2` |
| `ring_configuration` | `ring_configuration` |
| `stress` | `daily_stress` |
| `heart_health` | `daily_cardiovascular_age`, `vO2_max` |

## Rate limits

- **5000 requests / 24h** per access token (rolling window)
- **300 requests / 5 min** burst cap
- HTTP `429` on exceed; respect `Retry-After` header

The CLI does not currently cache responses — for heavy historical pulls, batch into one request via `--start`/`--end` rather than looping per-day.

## Date semantics

Oura's `day` field always refers to the **wake-up date** for sleep data.

- `daily_sleep` is filtered by `day` (wake-up) — straightforward
- `sleep` (detail) is filtered by `bedtime_start` — so to get sleep for `day=2026-03-15`, you need `start_date=2026-03-14` (the user went to bed on the 14th). The CLI's `sleep` subcommand handles this offset automatically.

## Error responses

| HTTP | Meaning |
|---|---|
| `400` | Bad request (usually malformed date) |
| `401` | Token expired/invalid → CLI auto-refreshes once |
| `403` | Scope not granted — re-authorize with the needed scope |
| `426` | Endpoint requires Oura subscription |
| `429` | Rate-limited |
| `5xx` | Oura backend issue — retry with backoff |

## Extending the CLI

The CLI is intentionally minimal. To add support for an uncovered endpoint:

1. Add the endpoint name to the `endpoint_map` dict in `oura-data.py`
2. Write a `format_*` function or use `format_generic` for raw JSON
3. Add the command name to `argparse`'s `choices` list

Pull requests welcome at https://github.com/zqchris/oura-cli.
