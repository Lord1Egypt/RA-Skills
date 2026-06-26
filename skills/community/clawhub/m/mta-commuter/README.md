# mta-commuter — NYC Commuter Transit Skill

LIRR, Metro-North, and NYC Subway in one skill — with multi-leg trip planning across commuter rail and subway, live delays, and track-assignment watches.

Schedule lookup, multi-leg trip planning, and service alerts for the Long Island Rail Road (LIRR), Metro-North (MNR), and NYC Subway. Uses the MTA's public GTFS static feeds and GTFS-realtime APIs — no API key required.

## What it does

- **Schedule lookup** — LIRR and Metro-North trains between any two stations, with live delays
- **Multi-leg trip planning** — combines commuter rail with subway connections through major terminals (Penn, Grand Central, Atlantic Terminal, Jamaica, Woodside, Harlem-125 St)
- **Nearby stations** — finds the closest commuter rail and subway stations to a point
- **Service alerts** — current disruptions across all three systems
- **Track watch** — notifies you when a track is assigned to a specific train (via cron)

## Quickstart

```bash
# LIRR lookup
python3 scripts/mta.py lirr "Penn Station" "New Hyde Park" --time 17:00

# Metro-North lookup
python3 scripts/mta.py mnr "Grand Central" "White Plains" --time 17:00

# Multi-leg trip (saved locations in data/locations.json)
python3 scripts/mta.py trip --near-origin work --near-dest home --time 17:00

# Alerts
python3 scripts/mta.py alerts
```

See `SKILL.md` for the full command reference and agent-facing instructions.

## What you can ask your agent

Because the skill is triggered by natural-language intent (not just literal commands), you can talk to it the way you'd talk to a commuter friend who has the schedule memorized:

### Getting home / to work

> "When's the next train from Penn to Huntington?"
> "How do I get home from the office around 6?"
> "What time should I leave work to make the 5:22 out of Penn?"
> "Train options from Grand Central to White Plains tonight after 9."

### Multi-leg trips

> "Get me from home to the WTC by 9 AM."
> "What's the fastest way from Flatbush to Westchester?"
> "Plan a trip from my place to 34th and 8th — I can walk or take the train."

The planner combines LIRR or Metro-North with a subway transfer at the right terminal (Penn, Grand Central, Atlantic Terminal, Jamaica, Woodside, or Harlem-125 St) and picks the connection with the shortest total time.

### Finding alternatives

> "The 1582 got canceled — what are my options?"
> "Any other trains around 5:30 that can get me near Mineola?"
> "Give me alternatives that avoid the Port Jefferson branch."

### Nearby stations

> "What stations are near 40.74, -73.68?"
> "Closest subway to my hotel."
> "Are there any MNR stations within 2 miles of home?"

### Service alerts

> "Any LIRR alerts today?"
> "Is the 6 train running normal?"
> "What's broken on the MTA right now?"

### Track watch (set-and-forget notifications)

> "Ping me when track is posted for the 5:22 PM Huntington train."
> "Watch for the track on MNR 873 out of Grand Central."

The agent sets up an `openclaw cron` job that polls the track API every 20 seconds and auto-deletes itself after it fires once.

### First-time setup

On first use the agent can save your common locations so you don't have to repeat addresses:

> "Save home as 123 Main St, Queens NY."
> "My office is at 250 Broadway."

After that: "train home," "leaving work at 5," "how do I get from home to Dev's apartment" all resolve automatically.

## Install

```bash
pip install -r requirements.txt
```

Installing via ClawHub handles this automatically. The only runtime dependency is `gtfs-realtime-bindings`, used to decode the MTA's GTFS-realtime protobuf feeds for live delays and service alerts.

**First run:** the subway headway cache takes ~20-30 seconds to build the first time (it's processing ~2M stop_times rows). Subsequent invocations read from the cache and are instant. The cache invalidates automatically when the GTFS feed is refreshed (every 24h).

## Example output

**Schedule lookup:**

```
$ python3 scripts/mta.py lirr "Penn Station" "New Hyde Park" --time 17:00
LIRR trains from Penn Station to New Hyde Park
Monday 2026-04-13, at/after 5:00 PM
(with real-time data)

Depart     Arrive     Duration   Branch                    To
---------------------------------------------------------------------------
5:10 PM    5:42 PM    32min      Port Washington Branch    Port Washington
5:22 PM    5:53 PM    31min      Port Jefferson Branch     Huntington
5:37 PM    6:05 PM    28min      Ronkonkoma Branch         Ronkonkoma
```

**Multi-leg trip:**

```
$ python3 scripts/mta.py trip --near-origin home --near-dest wtc --time 08:00
Transit options from Home to World Trade Center
Departing after 8:00 AM

Option 1 (~52 min total):
  8:05 AM  LIRR New Hyde Park -> Penn Station (35min, Port Jefferson Branch)
  Walk to E train (4 min)
  E train to World Trade Center (~12min, ~every 5 min)
  Walk to destination (1 min)

Option 2 (~58 min total):
  8:17 AM  LIRR New Hyde Park -> Atlantic Terminal (41min, Hempstead Branch)
  Walk to 2/3/4/5 train (3 min)
  2 train to Chambers St (~10min, ~every 4 min)
  Walk to destination (4 min)
```

**JSON output** (for agents and pipelines):

```
$ python3 scripts/mta.py lirr NYK NHP --time 17:00 --json --count 1
[
  {
    "trip_id": "PJ-17-1582",
    "system": "lirr",
    "route": "Port Jefferson Branch",
    "headsign": "Huntington",
    "depart": 1042,
    "depart_str": "5:22 PM",
    "arrive": 1073,
    "arrive_str": "5:53 PM",
    "duration": 31,
    "origin": "Penn Station",
    "destination": "New Hyde Park",
    "status": "On time",
    "delay_min": 0
  }
]
```

## Layout

```
skills/mta/
├── SKILL.md              # Agent-facing instructions
├── README.md             # This file
├── scripts/
│   ├── mta.py            # Unified CLI entry point
│   ├── gtfs.py           # Generic GTFS loader with caching
│   ├── subway.py         # Subway station/line/headway layer
│   ├── trip.py           # Multi-leg trip planner
│   ├── geo.py            # Haversine + nearby-station search
│   ├── locations.py      # Saved locations loader
│   ├── check_track.py    # Track watch (mylirr/mymnr APIs)
│   ├── feeds.json        # GTFS feed URLs per system
│   └── transfers.json    # Terminal-to-subway transfer map
├── tests/                # pytest test suite
└── data/                 # GTFS cache + locations.json (gitignored)
```

## Tests

```bash
cd skills/mta
python3 -m pytest tests/ -v
```

## Data sources

- [MTA Developer Resources](https://new.mta.info/developers) — GTFS static and GTFS-realtime feeds
- Track watch uses the unofficial `backend-unified.mylirr.org` and `backend-unified.mymnr.org` endpoints that power the mylirr.org / mymnr.org web apps. These are not official public APIs and may change without notice.

## License

MIT-0 (MIT No Attribution). See `LICENSE`.

## Limitations

- No subway real-time arrivals (frequency is estimated from schedule headways)
- No fare information
- No bus, NJ Transit, or PATH coverage
