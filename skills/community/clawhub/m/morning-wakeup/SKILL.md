---
name: morning-wakeup
description: Morning wake-up automation that fetches today's weather and matches a Sonos playback preset. Use when setting up daily morning routines, alarm-style wake-up flows, or weather-aware music automation. Triggers on phrases like "morning routine", "wake up automation", "morning alarm", "weather-based music".
---

# Morning Wake-up

Automate a daily morning wake-up: fetch weather → match preset → play on Sonos.

## Prerequisites

- Weather skill installed (Open-Meteo, no API key needed)
- Sonos CLI (`sonos`) installed and speakers on the local network
- At least one Sonos favorite configured per preset category

## Preset Mapping

The script maps WMO weather codes to Sonos favorite presets:

| Weather category | WMO codes | Default preset |
|---|---|---|
| Clear / Sunny | 0, 1 | `Morning Sunshine` |
| Cloudy | 2, 3, 45, 48 | `Cloudy Morning` |
| Rain / Drizzle | 51–57, 61–67, 80–82 | `Rainy Day` |
| Snow | 71–77, 85–86 | `Winter Morning` |
| Storm | 95–99 | `Stormy Ambient` |

Override presets by editing `scripts/presets.json` in the skill directory.

## Usage

### One-shot run

```bash
bun scripts/morning-wakeup.ts --location "Shanghai" --speaker "Bedroom"
```

### Scheduled (cron)

Set up a daily cron job, e.g. 7:00 AM:

```bash
# In OpenClaw cron
bun <skill-dir>/scripts/morning-wakeup.ts --location "Shanghai" --speaker "Bedroom"
```

Or use the OpenClaw cron tool:

```json
{
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "Asia/Shanghai" },
  "payload": { "kind": "agentTurn", "message": "Run the morning wake-up routine: fetch weather for Shanghai and play the matching Sonos preset on Bedroom speaker." }
}
```

## Script Parameters

| Param | Required | Default | Description |
|---|---|---|---|
| `--location` | Yes | — | City name or "lat,lon" |
| `--speaker` | Yes | — | Sonos speaker name |
| `--volume` | No | 15 | Start volume (0–100) |
| `--units` | No | celsius | celsius or fahrenheit |

## Flow

1. Fetch current weather via Open-Meteo
2. Map weather code → preset name
3. Set Sonos volume
4. Open the matching Sonos favorite
5. Output JSON result with weather summary and preset used
