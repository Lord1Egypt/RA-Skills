# PlaneFilter — OpenClaw Skill ✈️

> Flight aircraft type lookup with multi-source confidence scoring.

**Query any flight number** → get aircraft type, equipment changes, and confidence scoring from multiple aviation data sources — all within your OpenClaw agent.

## Install

### Option 1: ClawHub (recommended)

```bash
npx clawhub install planefilter
```

### Option 2: Git clone

```bash
git clone https://github.com/ImL1s/planefilter-openclaw-skill.git ~/.openclaw/workspace/skills/planefilter
```

### Option 3: Let the agent install it

Tell your OpenClaw agent:

> "Install the planefilter skill from https://github.com/ImL1s/planefilter-openclaw-skill"

The agent will clone and place it in the correct directory.

### After install

```bash
# Verify it loaded
openclaw skills list | grep planefilter

# Set up your API key
openclaw skills onboard
```

## Setup API Keys

| Key | Required | Free Tier | Get One |
|-----|----------|-----------|---------|
| `RAPIDAPI_KEY` | ✅ Yes | 150 req/month | [AeroDataBox on RapidAPI](https://rapidapi.com/aedbx-aedbx/api/aerodatabox) |
| `AIRLABS_KEY` | Optional | 150 req/month | [AirLabs](https://airlabs.co/signup) |

Set via `openclaw skills onboard` (auto-prompted) or manually in `~/.openclaw/openclaw.json`.

## Usage

Just ask your OpenClaw agent naturally:

- *"What aircraft is CI101 using today?"*
- *"查一下 BR108 的機型"*
- *"Check if EVA Air flight 12 has an equipment change"*

The agent will call `search_flight.js` and interpret the results.

## What It Does

1. **Parallel query** — OpenSky (free) + AeroDataBox + AirLabs
2. **Confidence scoring** — Weighted votes, agreement detection
3. **Equipment change** — Detects scheduled vs actual aircraft swap (upgrade/downgrade/lateral)
4. **ICAO normalization** — Converts model names (e.g. "Airbus A330-300") to ICAO codes ("A333")

## Example Output

```json
{
  "flightNumber": "CI101",
  "airline": "China Airlines",
  "origin": "NRT",
  "destination": "TPE",
  "aircraftType": "A333",
  "registration": "B-18311",
  "confidence": 0.6,
  "equipmentChange": null,
  "sources": ["aerodatabox"]
}
```

## License

MIT
