---
name: hk-weather
description: "Hong Kong weather information from the Hong Kong Observatory (HKO) official open data API. Use when: user asks about Hong Kong weather, temperature, rainfall, UV index, weather warnings (typhoon, rainstorm, thunderstorm), or 9-day forecast. NOT for: global weather, historical climate data, or non-HK locations. Supports Traditional Chinese and English output. No API key needed."
metadata:
  {"openclaw":
      {"emoji": "🌤️",
        "requires": {"bins": ["python3"]},
        "keywords": ["hong kong weather", "hk weather", "香港天氣", "天文台", "hko", "typhoon", "rainstorm", "暴雨警告", "颱風", "紫外線", "uv index", "temperature", "降雨量", "forecast", "預報"],
        "locale": ["zh-HK", "en"],
        "category": "weather",
        "quality": {"latency": "2-5s", "fallback": true},
        "securityNotes":
          {"purpose": "Read-only weather query from HKO official open data",
            "allowedDomains": ["data.weather.gov.hk"],
            "writeScope": ["scripts/__pycache__/"],
            "noSecrets": true}}}
---

# Hong Kong Weather (v1.0.0)

Get real-time weather, warnings, and forecasts from the Hong Kong Observatory (HKO) official open data API. Zero dependencies, zero API keys.

## Output Policy (Safe & ClawHub-friendly)
- Prefer script output as reply basis.
- Allow minimal formatting cleanup for readability.
- Never fabricate weather data. If API fails, show exact error.
- Keep output concise. No lengthy explanations.

## Safety & Scope (for Security Scan)
- **Allowed commands only**:
  - `python3 scripts/hk_weather.py current [tc|en]`
  - `python3 scripts/hk_weather.py warning [tc|en]`
  - `python3 scripts/hk_weather.py forecast [tc|en]`
  - `python3 scripts/hk_weather.py all [tc|en]`
- **Network scope (allowlist)**:
  - `https://data.weather.gov.hk/*`
- **Write scope (skill-local only)**:
  - `scripts/__pycache__/`
- No secrets. No credentials. No config files.

## Language Handling
- **Chinese query → `tc`**: When user asks in Chinese/Cantonese, use `python3 scripts/hk_weather.py current tc`
- **English/non-Chinese query → `en`**: When user asks in English, use `python3 scripts/hk_weather.py current en`
- **Default to `tc`** if language is unclear (Hong Kong primary language)

## Usage

### Current Weather
Real-time temperature, humidity, rainfall, UV index, and conditions.

```bash
# Chinese output (default for HK)
python3 scripts/hk_weather.py current tc

# English output
python3 scripts/hk_weather.py current en
```

### Weather Warnings
Check active warnings (typhoon, rainstorm, thunderstorm, etc.).

```bash
python3 scripts/hk_weather.py warning tc
python3 scripts/hk_weather.py warning en
```

### 9-Day Forecast
Extended forecast with temperature range, humidity, and rain probability.

```bash
python3 scripts/hk_weather.py forecast tc
python3 scripts/hk_weather.py forecast en
```

### All-in-One
Combined current + warnings + forecast (first 3 days).

```bash
python3 scripts/hk_weather.py all tc
python3 scripts/hk_weather.py all en
```

## Examples

**"今天香港天氣點？"**
```bash
python3 scripts/hk_weather.py current tc
```

**"What's the weather in Hong Kong?"**
```bash
python3 scripts/hk_weather.py current en
```

**"有冇暴雨警告？"**
```bash
python3 scripts/hk_weather.py warning tc
```

**"Forecast for the week"**
```bash
python3 scripts/hk_weather.py forecast en
```

**"香港天氣點？有冇警告？未來幾日預報？"**
```bash
python3 scripts/hk_weather.py all tc
```

## Notes
- Data source: Hong Kong Observatory Open Data API (data.weather.gov.hk)
- No API key required
- Response time: typically 2-5 seconds
- When no warnings are active, the warning command returns "No active weather warnings" / "現時無生效天氣警告"
