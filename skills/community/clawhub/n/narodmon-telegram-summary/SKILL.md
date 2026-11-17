---
name: narodmon-telegram-summary
description: "Use when setting up daily sensor summary reports from narodmon.ru to Telegram. Covers REST API authentication, sensorsHistory/sensorsValues calls, matplotlib chart generation with min/max annotations, Telegram Bot API photo delivery, and Hermes cron job setup."
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [narodmon, telegram, iot, sensors, charts, cron, monitoring]
    related_skills: []
---

# Narodmon Daily Summary → Telegram

## Overview

Sends a daily chart of narodmon.ru sensor readings (last 24h) to a Telegram chat via Bot API. Runs as a Hermes `no_agent` cron job — pure Python script, no LLM tokens spent per run.

Configuration is stored in a JSON file (see `templates/narodmon_config.json`) — no credentials hardcoded in the script.

## When to Use

- User has sensors on narodmon.ru and wants daily summaries in Telegram
- User asks to "set up narodmon reporting" or "send sensor graphs to Telegram"
- User wants to monitor IoT sensors (temperature, pressure, humidity) on a schedule

**Don't use for:** one-time sensor queries (just use curl), or non-narodmon IoT platforms.

## Prerequisites

1. **narodmon.ru account** with registered sensors (public or private)
2. **API key** — from Профиль → Мои приложения
3. **Telegram bot** — bot token (from @BotFather) and chat ID
4. **matplotlib** installed in the Python environment used for cron scripts

## Narodmon REST API Reference

### Endpoint
- `POST http://api.narodmon.ru` (JSON body, UTF-8)
- HTTPS may be unreachable from some VPS IPs — HTTP works fine for public sensors

### Required HTTP Headers (every request)
```
User-Agent: MyAppName          # latin letters, mandatory
Narodmon-Api-Key: ***          # from Профиль → Мои приложения
Content-Type: application/json  # for POST
```

### Required JSON Fields (every request)
- `cmd` — API method name
- `uuid` — MD5 hash (lowercase), generated once, identifies the app installation
- `lang` — `"ru"`, `"en"`, or `"uk"`

### Key Methods

| Method | Purpose |
|--------|---------|
| `appInit` | Init, sensor type reference, favorites. Requires `version` field. |
| `userLogon` | Auth: `hash = MD5(uuid + MD5(password))`. Returns `uid`, `tz`, `login`, `vip`. Call once per 24h max. |
| `sensorsNearby` | Find sensors by coordinates. `my=1` for own sensors (requires auth). |
| `sensorsValues` | Current readings by sensor ID array (≤30, limited by PubsLimit). |
| `sensorsHistory` | History by period. Accepts `id` (single) or `sensors` (array). Periods: `hour`, `day`, `week`, `month`, `year`. `offset` shifts back. |

### Rate Limit
- **1 request per minute** per client/IP — exceeding returns HTTP 429, prolonged abuse blocks API key.
- `userLogon` — max once per 24h.

### Finding Sensor IDs

**Option A — via API (automatic):**
1. `userLogon` with login + hash to bind uuid to account
2. `sensorsNearby` with `my=1` returns only your devices+sensors

**Option B — manual:**
- Open narodmon.ru, find your sensors on the map
- URL format: `narodmon.ru/SXXXXX` where XXXXX is the sensor ID

## Implementation Steps

### Step 1: Generate UUID
```bash
python3 -c "import hashlib; print(hashlib.md5('MyAppUniqueName'.encode()).hexdigest())"
```
Save this UUID — it's permanent for this app installation.

### Step 2: Create Config File

Copy `templates/narodmon_config.json` and fill in your credentials:

```json
{
  "api_url": "http://api.narodmon.ru",
  "api_key": "your_api_key",
  "uuid": "your_md5_uuid",
  "login": "your_login",
  "password": "your_password",
  "lang": "ru",
  "utc_offset": 3,
  "output_path": "/tmp/narodmon_daily.png",
  "telegram": {
    "token": "your_bot_token",
    "chat_id": "your_chat_id"
  },
  "sensors": [
    {"id": 12345, "label": "Улица", "color": "#2196F3"},
    {"id": 12346, "label": "Дом", "color": "#FF5722"},
    {"id": 12347, "label": "Баня", "color": "#4CAF50"},
    {"id": 12348, "label": "Давление", "color": "#9C27B0", "secondary": true}
  ]
}
```

Add `"secondary": true` for non-temperature sensors (pressure, humidity) to plot them on a secondary Y-axis.

### Step 3: Create Bash Wrapper

The script accepts `--config` argument pointing to the JSON config. Create a `.sh` wrapper:

```bash
#!/bin/bash
exec /path/to/venv/python /path/to/scripts/narodmon_daily.py --config /path/to/narodmon_config.json
```

Make executable. Use the Python interpreter that has matplotlib installed.

### Step 4: Create Cron Job

```
cronjob(action='create', schedule='0 9 * * *', no_agent=True, script='narodmon_daily.sh', name='narodmon-daily-summary')
```

- `no_agent=True` — script runs directly, stdout delivered verbatim, no LLM tokens
- Empty stdout = silent (nothing sent to user)
- Non-zero exit = error alert sent to user

### Step 5: Verify

Run the script manually and check:
- stderr shows `Authorized: uid=XXXX`
- stderr shows `Chart saved: /tmp/narodmon_daily.png`
- stderr shows `Telegram: photo sent (message_id=NN)`
- Photo arrives in Telegram

## Chart Features

The script generates a dual-axis matplotlib chart:
- **Left Y-axis:** temperature sensors (°C) with colored lines
- **Right Y-axis:** pressure/humidity (secondary sensors) with purple axis
- **Min/max annotations:** ▲▼ markers + text labels on each temperature line
- **Collision avoidance:** max-labels auto-shifted horizontally when sensors peak at similar times
- **Bottom summary:** current value + trend arrow (↑↓→) + min/max range per sensor
- **Extended Y-limits:** ±2.5°C padding so annotations aren't clipped
- **Time axis:** local timezone, 2-hour intervals

## Common Pitfalls

1. **HTTPS unreachable from VPS.** `https://narodmon.ru` may timeout (geo-block or IP filter). Use `http://api.narodmon.ru` — works for public sensors. For private sensors, HTTP still works but password hash travels unencrypted. Acceptable for most home setups.

2. **Missing required headers.** `User-Agent` and `Narodmon-Api-Key` are both mandatory. Without `User-Agent`, server returns `{"error":"NO_VERSION_INFO","errno":400}` or rejects silently.

3. **`appInit` requires `version`.** If you call `appInit` without `version` field, you get `NO_VERSION_INFO` error. Always pass `"version":"1.0"` at minimum.

4. **`sensorsValues` limited to 30 sensors** (or fewer, per your PubsLimit). Check Профиль → Мои приложения → PubsLimit.

5. **`userLogon` rate limit.** Call auth at most once per 24h. The script calls it once per run (daily), which is safe. If you increase cron frequency, cache the auth state.

6. **matplotlib not in system Python.** Install it in the Python environment that the cron script uses. Verify with `python -c "import matplotlib"`.

7. **Cron script path.** Hermes `no_agent` cron scripts must be relative filenames in the Hermes scripts directory — not absolute paths. Use a `.sh` wrapper that calls the Python script with full paths.

8. **Config file permissions.** The JSON config contains credentials in plaintext. Restrict file permissions (`chmod 600 narodmon_config.json`). Do not commit to version control.

9. **`sensorsHistory` accepts both `id` and `sensors`.** Use `sensors` array for multiple sensors in one request. Response has `sensors[]` (metadata) and `data[]` (time-value pairs with sensor `id` field for matching).

10. **Timezone.** API returns UnixTime (UTC+0). Convert to local with `datetime.fromtimestamp(t, tz=timezone(timedelta(hours=utc_offset)))`. The server timezone is Europe/Moscow — don't pass local time as-is to API.

## Verification Checklist

- [ ] matplotlib installed in the Python environment used by the cron script
- [ ] JSON config file created with all credentials filled in
- [ ] Config file permissions restricted (chmod 600)
- [ ] Bash wrapper executable, calls correct Python interpreter with `--config` path
- [ ] Manual run produces a chart and sends photo to Telegram
- [ ] Cron job created with `no_agent=True`, `script='narodmon_daily.sh'`
- [ ] Cron schedule set to desired time (e.g., `0 9 * * *` for 09:00 daily)
