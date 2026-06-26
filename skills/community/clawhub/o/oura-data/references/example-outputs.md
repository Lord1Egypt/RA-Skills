# Example Outputs

Real samples from `oura-cli` so the assistant (and ClawHub browsers) can see exactly what each subcommand returns and how to interpret it.

## `today`

```
$ uv run oura-data.py today

=== Sleep ===

📅 2026-05-13  Sleep Score: 82
  Total: 7h32m | Deep: 1h28m | REM: 2h05m | Light: 3h59m
  Efficiency: 91%
  Bedtime: 23:42 → 07:18
  Avg HR: 56 | Lowest: 49 | HRV: 64
  Contributors: deep_sleep: 88, efficiency: 95, latency: 82, rem_sleep: 90, restfulness: 71, timing: 85, total_sleep: 80

=== Activity ===

📅 2026-05-13  Activity Score: 88
  Steps: 12483 | Active Cal: 612 | Total Cal: 2741
  Walking Distance: 9.4 km

=== Readiness ===

📅 2026-05-13  Readiness Score: 79
  Temp Deviation: -0.1°C
  Contributors: activity_balance: 85, body_temperature: 100, hrv_balance: 72, previous_day_activity: 88, previous_night: 82, recovery_index: 76, resting_heart_rate: 95, sleep_balance: 70
```

**How to read this:** Sleep 82 = good. Readiness 79 = good, but HRV balance contributor at 72 suggests slightly elevated training load — fine to train, not a "max effort" day.

## `sleep`

Single date:

```
$ uv run oura-data.py sleep --date 2026-05-12

📅 2026-05-12  Sleep Score: 76
  Total: 6h54m | Deep: 1h12m | REM: 1h41m | Light: 4h01m
  Efficiency: 88%
  Bedtime: 00:18 → 07:24
  Avg HR: 58 | Lowest: 51 | HRV: 51
  Contributors: deep_sleep: 80, efficiency: 88, latency: 92, rem_sleep: 72, restfulness: 65, timing: 70, total_sleep: 72
```

Date range:

```
$ uv run oura-data.py sleep --start 2026-05-06 --end 2026-05-12

📅 2026-05-06  Sleep Score: 81
  Total: 7h21m | Deep: 1h33m | REM: 1h55m | Light: 3h53m
  ...

📅 2026-05-07  Sleep Score: 73
  Total: 6h12m | Deep: 0h58m | REM: 1h32m | Light: 3h42m
  ...

# ... (one block per night)
```

## `activity`

```
$ uv run oura-data.py activity --date 2026-05-12

📅 2026-05-12  Activity Score: 91
  Steps: 14802 | Active Cal: 743 | Total Cal: 2895
  Walking Distance: 11.2 km
```

## `readiness`

```
$ uv run oura-data.py readiness --start 2026-05-06 --end 2026-05-12

📅 2026-05-06  Readiness Score: 83
  Temp Deviation: -0.2°C
  Contributors: activity_balance: 88, body_temperature: 100, hrv_balance: 78, ...

📅 2026-05-07  Readiness Score: 71
  Temp Deviation: +0.4°C
  Contributors: activity_balance: 75, body_temperature: 60, hrv_balance: 62, ...
```

The temp_deviation spike on 2026-05-07 (+0.4°C) dragged the `body_temperature` contributor to 60 — a strong signal of illness, late-night alcohol, or warm sleeping environment.

## `heartrate`

```
$ uv run oura-data.py heartrate --date 2026-05-12

Heart Rate — Min: 49 | Max: 142 | Avg: 71 | Samples: 287
```

## `workout`

Returns raw JSON from the API:

```json
[
  {
    "id": "abc...",
    "activity": "running",
    "calories": 412,
    "day": "2026-05-12",
    "distance": 6420.5,
    "end_datetime": "2026-05-12T18:47:00+00:00",
    "intensity": "moderate",
    "label": null,
    "source": "autodetected",
    "start_datetime": "2026-05-12T18:12:00+00:00"
  }
]
```

## `spo2`

```json
[
  {
    "id": "...",
    "day": "2026-05-12",
    "spo2_percentage": {
      "average": 97.4
    }
  }
]
```

## `stress`

```json
[
  {
    "id": "...",
    "day": "2026-05-12",
    "stress_high": 1820,
    "recovery_high": 6300,
    "day_summary": "balanced"
  }
]
```

## `ring`

```json
{
  "id": "...",
  "color": "stealth",
  "design": "heritage",
  "firmware_version": "2.9.32",
  "hardware_type": "gen3",
  "size": 10,
  "set_up_at": "2024-08-14T19:22:00+00:00"
}
```

## `personal`

```json
{
  "id": "...",
  "age": 32,
  "weight": 72.4,
  "height": 1.78,
  "biological_sex": "male",
  "email": "user@example.com"
}
```

> ⚠️ Personal info contains email. Never echo this output in any context where the conversation may be logged or shared.
