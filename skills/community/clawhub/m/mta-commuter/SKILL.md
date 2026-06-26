---
name: mta-commuter
description: >
  NYC commuter transit: LIRR, Metro-North, and Subway schedules, trip planning,
  and service alerts. Use when the user asks about train departures, arrivals,
  commute times, trip options, or service disruptions.
  Also for multi-leg trip planning between locations, finding nearby stations
  across all systems, alternatives to a specific train, or track alerts.
  Triggers on "LIRR", "Metro-North", "MNR", "subway", "train schedule",
  "train times", "train home", "get me to", "how do I get to", "trip from",
  "alternatives", "track alert", "nearby stations", "commute", "train options",
  "service alerts", "MTA".
version: 1.0.0
metadata:
  openclaw:
    emoji: "🚆"
    homepage: "https://github.com/ottomanelli/mta-commuter"
    requires:
      bins:
        - python3
    install:
      pip:
        - gtfs-realtime-bindings
---

## Instructions

Look up LIRR, Metro-North, and NYC Subway schedules with live delay data using `scripts/mta.py`. Uses MTA GTFS static feeds and GTFS-RT real-time APIs (no API key required). Requires the `gtfs-realtime-bindings` pip package (auto-installed via ClawHub; otherwise `pip install -r requirements.txt`).

Run from the skill directory (`skills/mta/`):

### Direct schedule lookup (LIRR or Metro-North)

```bash
python3 scripts/mta.py lirr "<origin>" "<destination>" --date YYYY-MM-DD --time HH:MM
python3 scripts/mta.py mnr "<origin>" "<destination>" --date YYYY-MM-DD --time HH:MM
```
- `--date` and `--time` default to now if omitted.
- Station names are fuzzy-matched. Common LIRR codes: NHP (New Hyde Park), NYK (Penn Station), JAM (Jamaica), ATL (Atlantic Terminal). Common MNR codes: GCT (Grand Central), WP (White Plains), HM (Harlem-125 St).
- Add `--json` for machine-readable output, `--count N` to change result count (default 5).
- Real-time delay data is automatically included for today's lookups. Use `--no-live` to show schedule only.

### Multi-leg trip planning

Plan trips across LIRR, Metro-North, and Subway connections. Uses `data/locations.json` for saved locations.

```bash
# Using saved locations
python3 scripts/mta.py trip --near-origin work --near-dest home --time 17:00

# Using coordinates
python3 scripts/mta.py trip --near-origin 40.75,-73.99 --near-dest 40.74,-73.68 --time 17:00

# Custom radius and count
python3 scripts/mta.py trip --near-origin work --near-dest home --time 17:00 --radius 2 --count 8
```

Trip planning finds commuter rail options from all systems and includes subway transfer legs where applicable (Penn Station, Grand Central, Atlantic Terminal, Jamaica, Woodside, Harlem-125 St).

### Find nearby stations (all systems)

```bash
python3 scripts/mta.py stations nearby --near home --radius 2
python3 scripts/mta.py stations nearby --lat 40.74 --lon -73.68
```

Returns LIRR, Metro-North, and Subway stations sorted by distance.

### Service alerts

```bash
python3 scripts/mta.py alerts                    # All systems
python3 scripts/mta.py alerts --system lirr       # LIRR only
python3 scripts/mta.py alerts --system mnr        # Metro-North only
python3 scripts/mta.py alerts --system subway     # Subway only
python3 scripts/mta.py alerts --json              # JSON output
```

### System-specific commands

```bash
python3 scripts/mta.py lirr --stations            # List all LIRR stations
python3 scripts/mta.py mnr --stations             # List all MNR stations
python3 scripts/mta.py lirr --routes              # List LIRR branches
python3 scripts/mta.py mnr --routes               # List MNR lines
python3 scripts/mta.py lirr --find-station "hyde"  # Search for a station
python3 scripts/mta.py lirr --alerts              # System-specific alerts
```

### Location management

Locations are stored in `data/locations.json`. Manage them conversationally:
- To add: geocode the user's address (via web search), then write to the JSON file directly
- To list: read and display the JSON file
- To update: modify the entry and rewrite the file

Format:
```json
{
  "home": {
    "address": "123 Main St, Anytown, NY 11000",
    "lat": 40.7432,
    "lon": -73.6812,
    "label": "Home"
  }
}
```

### Setup flow (first use)

When this skill is first activated and `data/locations.json` doesn't exist, ask the user:
1. "Where's home?" -- geocode the address via web search, save to locations.json
2. "Where's work?" -- same
3. "Any other places you travel to regularly?" -- save additional locations

After setup, when the user mentions a saved location, consider whether they might be asking about transit -- even without explicitly saying "train." For example, "how do I get home from the city" is a transit request if home is a saved location.

### Presenting trip results
- Highlight the best option (earliest arrival closest to target)
- Mention 2-3 alternatives with station distances
- For multi-leg trips, clearly show each leg (commuter rail + subway transfer)
- Note which branches/lines serve each option
- If there are relevant service alerts, check alerts and mention disruptions

### Track alerts

Watch for track announcements on LIRR or Metro-North trains using `scripts/check_track.py` via `openclaw cron`.

```bash
# LIRR track watch
openclaw cron add --every 20s \
  --command "cd skills/mta && python3 scripts/check_track.py --train 1582 --station NYK" \
  --channel telegram --delete-after-run \
  --name "Track watch: 5:22 PM to Huntington"

# Metro-North track watch
openclaw cron add --every 20s \
  --command "cd skills/mta && python3 scripts/check_track.py --system mnr --train 873 --station GCT" \
  --channel telegram --delete-after-run \
  --name "Track watch: 5:43 PM to White Plains"
```

**Note:** `check_track.py` queries undocumented endpoints used by the mylirr.org and mymnr.org web apps (`backend-unified.mylirr.org` / `backend-unified.mymnr.org`). These are not official public APIs and may change or become unavailable without notice. The rest of the skill uses the official MTA GTFS feeds and is not affected.

#### Workflow for "remind me about train X"

1. Look up the train to confirm it exists and get the departure time
2. Set up a cron job with `openclaw cron add` using the train number and `--system` flag
3. The cron job auto-deletes after the first notification (`--delete-after-run`)
4. Confirm the watch was added

### Limitations
1. **No subway real-time arrivals** -- subway frequency is estimated from schedule headways ("every ~8 min"), not live countdown data.
2. **No fares** -- cannot look up ticket prices.
3. **No bus** -- NJ Transit, MTA bus, and PATH are not included.

