---
name: hk-weather-info
description: "Hong Kong weather information — current conditions, forecasts from HKO (Hong Kong Observatory). Use when user asks about HK weather, temperature, rainfall, or weather forecast."
version: 1.1.0
author: Steven Ho
license: MIT
github: https://github.com/StevenHo1394/openclaw/tree/main/skills/hk-weather-info
metadata:
  hermes:
    tags: [weather, hong-kong, hko, forecast, temperature, rainfall]
    related_skills: []
  openclaw:
    providers: [hko]
---

# HK Weather Info

## Overview

Hong Kong weather skill using HKO (Hong Kong Observatory) OpenData API. Provides current weather reports and local weather forecasts. Supports regional filtering and multilingual output (English, Traditional Chinese, Simplified Chinese).

## Data Source

HKO OpenData API — free, no API key required.
- Current weather: `https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=<lang>`
- Forecast: `https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=<lang>`

## Variables

| Variable | Description | Values |
|---|---|---|
| `HK_WEATHER_INFO_REGION` | Target region/district. If None, returns general HK weather. | e.g. `"Tsuen Wan"`, `"Central"`, `None` |
| `HK_WEATHER_INFO_LANG` | Language preference | `tc` (Traditional Chinese, default), `en` (English), `sc` (Simplified Chinese) |

## Step 1: Get User Input

### (a) Target region
Ask user for target region/district. If user refuses or says "general/whole HK", set `HK_WEATHER_INFO_REGION = None`.

### (b) Language preference
Default to `tc` (Traditional Chinese) unless user specifies otherwise. Supported:
- `tc` — Traditional Chinese (繁體中文) — **default**
- `en` — English
- `sc` — Simplified Chinese (简体中文)

Store as `HK_WEATHER_INFO_LANG`. Default is `tc` if not set.

## Step 2: Workflow

### (a) Current weather report

Call:
```
GET https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=<HK_WEATHER_INFO_LANG>
```

The API returns JSON with:
- `temperature` — array of `{place, value, unit}`
- `humidity` — `{value, unit}`
- `rainfall` — array of `{place, value, unit}`
- `icon` — weather icon code
- `uvindex` — UV index (if available)
- `updateTime` — timestamp
- `warningMessage` — active warnings (string)
- `rainstormReminder` — rainstorm reminder (string)

**Regional filtering:** If `HK_WEATHER_INFO_REGION` is set (not None):
1. Search `temperature` array for entry where `place` matches the region (case-insensitive partial match)
2. Search `rainfall` array for entry where `place` matches the region
3. Display matched regional data

If no match found or `HK_WEATHER_INFO_REGION` is `None`:
- Display general HK weather (all temperature stations, all rainfall stations)

### (b) Local weather forecast

Call:
```
GET https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=<HK_WEATHER_INFO_LANG>
```

The API returns JSON with:
- `generalSituation` — general weather situation
- `forecastDesc` — forecast description
- `outlook` — outlook
- `forecastPeriod` — string (wind direction letters, NOT an array). Use `forecastDesc` for the human-readable forecast text.
- `updateTime` — timestamp

**Regional filtering:** If `HK_WEATHER_INFO_REGION` is set:
- The forecast is territory-wide. Note the regional context when presenting.

Display today's and tomorrow's forecast by default.

## Step 3: 1-Minute Average Temperature (CSV)

After completing Steps 1 and 2, fetch the latest 1-minute average temperature from HKO CSV.

> **Reference:** `references/1min-temp-csv.md` — actual column names, alias mapping, gotchas.

### (a) Determine CSV URL

Based on `HK_WEATHER_INFO_LANG`:

| Language | CSV URL |
|---|---|
| `en` | `https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_1min_temperature.csv` |
| `tc` | `https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_1min_temperature_uc.csv` |
| `sc` | `https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_1min_temperature_sc.csv` |
| any other value | Do not fetch CSV |

### (b) Download with retry

- Attempt to download the CSV via `curl` (or `urllib`).
- Retry at most **2 times** if download fails (network error, timeout, empty response).
- If all retries fail, skip the 1-minute temperature — do not block the rest of the weather output.

### (c) Extract temperature

The CSV column names vary by language. Actual column names observed:

| Language | Place column | Temperature column |
|---|---|---|
| `tc` | `自動氣象站` | `氣溫（攝氏）` |
| `en` | `Automatic Weather Station` | `Air Temperature(degree Celsius)` |
| `sc` | (similar Chinese names) | (similar Chinese names) |

The CSV starts with a **UTF-8 BOM** (`\ufeff`) — strip it before parsing or the first column key will be malformed.

The CSV contains ~39 automatic weather stations with specific station names (e.g. `荃灣可觀`, `赤鱲角`, `京士柏`), not district names. When matching regions:
- **If `HK_WEATHER_INFO_REGION` is set**: try direct partial match first, then try English-to-Chinese alias mapping (e.g. "Tsuen Wan" → `荃灣`, "Central" → `中環`). Use the first matched station's temperature.
- **If `HK_WEATHER_INFO_REGION` is not set or no match found**: compute the **average** of all stations' temperature values and present it as the 1-minute average temperature of Hong Kong overall.

### (d) Append to output

If a 1-minute average temperature was successfully obtained, append it to the reply:

**TC output:**
```
🕒 1分鐘平均氣溫：XX°C（[地區名稱 / 全港平均]）
```

**EN output:**
```
🕒 1-Min Avg Temp: XX°C ([Region Name / HK Average])
```

**SC output:**
```
🕒 1分钟平均气温：XX°C（[地区名称 / 全港平均]）
```

## Output Format

**When `lang=tc` (default)**, the HKO API returns all text fields in Traditional Chinese. Use Chinese labels for consistency:

### Current Weather (TC)
```
🇭🇰 香港天氣 [地區]

🌡️ 氣溫：XX°C（測站名稱）
💧 濕度：XX%
🌧️ 雨量：XXmm（測站名稱）
☀️ 紫外線指數：XX（如有）

⚠️ 生效警告：[警告內容 / 無]
🕐 更新時間：<updateTime>
```

### Forecast (TC)
```
📅 天氣預測

📋 概況：<generalSituation>

📅 今日：<forecast> | 溫度：<tempRange>°C | 濕度：<rhRange>%
📅 明日：<forecast> | 溫度：<tempRange>°C | 濕度：<rhRange>%

🔮 展望：<outlook>

🕐 更新時間：<updateTime>
```

**When `lang=en`**, use English labels:
```
🌤️ Hong Kong Weather [Region if set]
Temperature: XX°C (Station Name)
Humidity: XX%
...
Forecast: <forecastDesc>
```

## Timezone & Date Handling

**Always check system time first.** Run `date '+%Y-%m-%d %H:%M:%S %Z'` and convert to HKT (UTC+8) before responding. Never assume the date from conversation context or system prompt timestamps. The conversation may span multiple days.

No API key required. HKO OpenData is free and open.

### Dependencies
- Python 3.10+ stdlib only (urllib, json, datetime)

### Script
`scripts/hk_weather.py` — CLI client with 10-min file cache. **Default language is `tc` (Traditional Chinese).**

```bash
python3 scripts/hk_weather.py                          # General HK, Traditional Chinese (default)
python3 scripts/hk_weather.py --region "Tsuen Wan"     # Regional, TC
python3 scripts/hk_weather.py --lang en                 # English output
python3 scripts/hk_weather.py --action current          # Current only
python3 scripts/hk_weather.py --action forecast         # Forecast only
```

## Common Pitfalls

0. **Default language is TC** — The script defaults to `--lang tc`. All output (including labels) should be in Traditional Chinese unless user specifies `--lang en` or `--lang sc`. The HKO API returns Chinese text fields when `lang=tc`, so output labels must also be in Chinese for consistency.
1. **No API key needed** — HKO OpenData is free and open
2. **Rate limiting** — respectful polling, cache results for 10-15 minutes
3. **Regional name matching** — use partial case-insensitive match. Some station names differ from district names
4. **UV index** — may be null at night or on cloudy days
5. **Warning message** — may be empty string if no warnings active
6. **Forecast language** — the `lang` parameter affects all text fields
7. **Rainfall entries may lack `value` key** — always check `"value" in matched` before accessing. Some stations report empty/missing rainfall data differently.
8. **`forecastPeriod` is a string, not an array** — the `flw` API returns `forecastPeriod` as a string (wind direction letters), NOT an array of forecast period objects. Use `forecastDesc` for the human-readable forecast text.
9. **1-min CSV has UTF-8 BOM** — the HKO CSV files start with `\ufeff`. Strip before parsing or the first column key will be corrupted. The CSV also uses language-specific Chinese column names (e.g. `自動氣象站`, `氣溫（攝氏）`), not the generic `地區`/`溫度` names.
10. **CSV regional matching requires alias mapping** — station names in the CSV are specific automatic weather station names (e.g. `荃灣可觀`, `赤鱲角`), not district names. English region names like "Tsuen Wan" won't directly match Chinese station names — use alias mapping (e.g. "Tsuen Wan" → `荃灣`).

## Verification Checklist

- [x] HKO OpenData API used (no API key)
- [x] Regional filtering implemented
- [x] Language preference supported (en/tc/sc)
- [x] Current weather and forecast both fetched
- [x] Output format defined
- [x] No external dependencies (Python stdlib only)

## Changelog

### v1.1.0 — Bug fixes and 1-minute average temperature CSV
- Fixed `warningMessage` formatting: HKO API can return a list of warning strings, not just a single string. Now iterates and prints each warning on its own line.
- Fixed `forecastPeriod` description in SKILL.md: it's a string (wind direction), not an array. Removed contradictory description.
- Added Step 3: fetch latest 1-minute average temperature from HKO regional-weather CSV.
- Supports all 3 languages (en/tc/sc) with separate CSV URLs per language.
- Retry up to 2 times on download failure.
- Regional match: extracts temperature for the requested region; otherwise computes HK-wide average.
- Appended to the end of the weather reply.
- Fixed `match_region` to support English→Chinese alias mapping for current weather regional filtering.
- Fixed humidity unit display: HKO API returns `"percent"` instead of `"%".

### v1.0.0 — Initial release
- HKO OpenData API (rhrread + flw), regional filtering, multilingual (en/tc/sc), Traditional Chinese default.
