---
name: pollen-forecast
description: Fetch pollen forecasts for Swedish locations from Pollenrapporten (Swedish Museum of Natural History). Use when Boss asks about pollen levels, pollen forecast, or allergy conditions in Sweden. Covers alder, hazel, birch, grass, and other pollen types with severity levels.
---

# Pollen Forecast (Sweden)

Fetch current pollen forecasts from the Swedish Pollen Report (Pollenrapporten) API.

## Quick Start

```bash
# Basic forecast
python3 $OPENCLAW_HOME/workspace/skills/pollen-forecast/scripts/get_forecast.py <city-name>

# With grass pollen alerts (for allergy sufferers)
python3 $OPENCLAW_HOME/workspace/skills/pollen-forecast/scripts/get_forecast.py <city-name> --alert
```

Example cities: Göteborg, Stockholm, Malmö, Jönköping, Uppsala

## How It Works

1. **Location mapping**: The script matches your city to the nearest region ID from the Swedish Pollen Report network
2. **Fetches forecast**: Current pollen levels and text summary from `api.pollenrapporten.se`
3. **Fetches pollen types**: Maps pollen IDs to human-readable names with threshold values
4. **Fetches level definitions**: Swedish names for severity levels from API
5. **Returns formatted output**: Severity levels + text forecast + grass pollen alerts (if `--alert` flag used)

## Severity Levels

- **0**: None (Inga halter)
- **1**: Low (Låga halter)
- **2**: Moderate (Måttliga halter)
- **3**: High (Höga halter)
- **4**: Very High (Mycket höga halter)

## Grass Pollen Alerts

Use the `--alert` flag for enhanced warnings about grass pollen (Gräs), which is the most common trigger for severe allergies.

**Alert triggers:**

| Level | Alert | Recommendations |
|-------|-------|-----------------|
| **2 - Moderate** | 💊 Start allergy medication | Consider mask for extended outdoor time |
| **3 - High** | 😷 Mask + 👓 glasses required | Keep windows closed, use air purifier |
| **4 - Very High** | 🚨 CRITICAL | Minimize outdoor exposure, shower after being outside |

**Usage for allergy sufferers:**
```bash
python3 $OPENCLAW_HOME/workspace/skills/pollen-forecast/scripts/get_forecast.py Göteborg --alert
```

## Usage

### Command Line

```bash
# Get forecast for Gothenburg
python3 $OPENCLAW_HOME/workspace/skills/pollen-forecast/scripts/get_forecast.py Göteborg

# Get forecast for Stockholm with grass pollen alerts
python3 $OPENCLAW_HOME/workspace/skills/pollen-forecast/scripts/get_forecast.py Stockholm --alert

# List available cities
python3 $OPENCLAW_HOME/workspace/skills/pollen-forecast/scripts/get_forecast.py --help
```

### From SKILL.md

The skill automatically:
1. Reads the region mappings from `references/regions.json`
2. Finds the closest matching region for the requested city
3. Calls the Pollenrapporten API
4. Formats the response with pollen types and severity levels

## Data Sources

- **API**: https://api.pollenrapporten.se/v1/
- **Source**: Swedish Museum of Natural History (Naturhistoriska riksmuseet)
- **Coverage**: 24 regions across Sweden
- **Update frequency**: Daily during pollen season

## Output Format

**Standard output:**
```
🌿 Pollen Forecast for Göteborg
📅 2026-03-10 to 2026-03-11

📝 Summary:
Under tisdagen och onsdagen väntas måttliga till höga halter av alpollen...

📊 Current Levels:
• Hassel: Low / Låga
• Al: Very High / Måttliga till höga
• Sälg och viden: None / Inga halter
• Gräs: None / Inga halter
```

**With `--alert` flag (grass pollen warning mode):**
```
🌿 Pollen Forecast for Göteborg
📅 2026-03-10 to 2026-03-11

📝 Summary:
...

📊 Current Levels:
• Gräs: High / Höga halter
...

⚠️ GRASS POLLEN ALERT ⚠️
🌾 Gräs is at HIGH levels.
💊 Take allergy medication now.
😷 Wear mask + 👓 glasses when outside.
🚪 Keep windows closed. Use air purifier if available.
```

## Region Coverage

See `references/regions.json` for the complete list of 24 monitored regions including:
- Göteborg (Gothenburg)
- Stockholm
- Malmö
- Jönköping
- Uppsala (nearest: Stockholm)
- Linköping (nearest: Norrköping)
- Lund (nearest: Malmö)

## Notes

- Forecasts are in Swedish; the API returns Swedish text summaries. You must send in Swedish, and also in English.
- Pollen season typically runs February–September
- Some smaller towns map to the nearest major monitoring station
