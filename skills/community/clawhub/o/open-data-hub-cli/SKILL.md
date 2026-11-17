---
name: open-data-hub-cli
description: Query Open Data Hub/NOI Techpark data through `odh`: Tourism, Mobility, traffic, A22, parking, EV charging, STA GTFS, and transit.
homepage: https://github.com/galjos/odh-cli
metadata:
  {
    "openclaw":
      {
        "os": ["darwin", "linux"],
        "requires": { "bins": ["odh"] },
        "install":
          [
            {
              "id": "go",
              "kind": "go",
              "module": "github.com/galjos/odh-cli/cmd/odh@v0.7.1",
              "bins": ["odh"],
              "label": "Install odh CLI (go)",
            },
          ],
      },
  }
---

# Open Data Hub CLI

Use `odh` instead of scraping Open Data Hub pages. Most practical data is South Tyrol / Autonomous Province of Bolzano; verify record-level location from coordinates, origin, or metadata.

## Setup

```bash
odh version
odh doctor --timeout 10s # local doctor flag, not the global --timeout
```

Need `odh v0.7.1` or newer for the current command contracts, dataset guidance, source/provenance fields, traffic helpers, GTFS/transit, filtered latest measurements, comma-safe `--param`, `transit journey --with-realtime`, and MCP server mode. Installs below pin v0.7.1.

Preferred manual install options:

```bash
go install github.com/galjos/odh-cli/cmd/odh@v0.7.1
brew install galjos/odh/odh
```

Agent hosts can also use the declared OpenClaw Go installer metadata in this skill. If running from the source repo, use `./odh`.

Agent hosts that prefer MCP over shell commands can run the same curated surface as Model Context Protocol tools with `odh mcp serve`; tools advertise read-only behavior and return structured JSON alongside text, with the same contracts and warnings as the CLI.

## Output Rules

- Curated commands may default to table. Add `--json` or `--format json` before parsing output.
- This applies especially to `traffic`, `a22 status`, `transit`, `tourism types`, `mobility types`, and `mobility datatypes`.
- Treat stderr as diagnostics, not data.
- Nonzero exit means failure. Exit `2` usually means bad invocation.
- For bounded agent loops, put the global timeout before the subcommand, for example `odh --timeout 20s traffic today --area bozen-unterland --json`. `odh doctor --timeout` is a separate local flag.
- When unsure about command shape, run `odh <command> --help`; current help includes task-focused examples.
- Prefer discovery commands before guessing provider names, data types, stop IDs, or zone IDs.
- Prefer returned `source`, `source_detail`, `endpoint`, `archive`, `realtime`, and `warnings` fields over inferred provenance.
- Stable curated JSON fields are documented in `docs/json-contracts.md` in the repo.
- Traffic and normalized `mobility latest` results include `coverage` with fetched, matched, and returned counts. Check `result_truncated` and `upstream_may_have_more` before claiming a complete list; matched counts cover only the fetched rows. Content traffic also reports `upstream_total` when supplied by the source.

## Discovery

```bash
odh apis
odh datasets guide "ev charging availability" --format json
odh datasets search parking
odh openapi mobility
odh openapi tourism
odh mobility types --kind station
odh mobility origins --station-type ParkingStation
odh mobility datatypes --station-type TrafficSensor --origin A22 --limit 1000 --json
```

For unfamiliar data questions, run `odh datasets guide <topic> --format json` first and follow its `discovery`, `verify`, and `caveats` fields before choosing lower-level commands.

Always run `odh mobility origins --station-type <type>` before filtering any query with `--origin`, even when the origin seems obvious (A22, ALPERIA, PROVINCE_BZ): origin names are upstream vocabulary, and a catalogued origin or datatype is not proof that open measurement rows exist.

`mobility origins`, `mobility stations`, `mobility datatypes`, and `mobility events` add a *truncation* entry to `warnings` whenever the result filled `--limit`, including the default limit; raise `--limit` until that truncation entry disappears before claiming a complete list. Other `warnings` entries are unrelated to `--limit` and do not go away — `mobility events` always carries the Timeseries feed caveat, so its `warnings` array is never empty.

Use `odh call <api> <path> --param key=value` for known endpoints. `--param` is repeatable and values may contain commas.

## Traffic

Roadworks, closures, and road events:

```bash
odh traffic zones --json
odh traffic categories --json
odh traffic today --area ueberetsch-unterland --type roadworks --json
odh traffic search badia --today --zone-id 6 --json
odh traffic today --near 46.42,11.25 --radius 15km --json
odh traffic today --source content --json
odh traffic today --source content --area pustertal --json
odh traffic search radroute --today --source content --json
```

Prefer `traffic` over raw `mobility events --origin PROVINCE_BZ`. Surface stale/source warnings. Do not present stale open-ended rows as confirmed current closures. The default `--source odh` is a Mobility Timeseries event feed, not a live bulletin: an empty result is not evidence that roads are clear. Report the newest row date the command returns.

`--source content` runs the same commands against the Content API `/v1/Announcement` bulletin, which is where the province still publishes. It supports `--from`/`--to`/`--today`, `--near`/`--radius`, `--search`, `--type`, `--limit`, `--include-expired` and `--zone-id`/`--area`, and rejects `--road` and `--type bike` with exit code 2 rather than returning a partial list. Its results omit `zone_id`, `zone`, `zone_it`, `road`, `road_name`, `severity` and `series_id` because this source cannot populate them. An absent `end` means the announcement is still open; use `event.get("end")` to read it. Already-ended ones are hidden unless `--include-expired` is passed, and `stale` there only means "unchanged for 30 days", which is normal for long-running restrictions.

`--zone-id` and `--area` are geographic inference on this source, not a field read: the announcement's coordinates are matched against a committed table of ~1100 coordinates whose zone the Mobility feed recorded, matching when the nearest is within 2.0 km. Announcements beyond that, or without coordinates, are excluded as unassignable and counted in a warning. No inferred zone is written into the output. Surface that warning and phrase the answer as "in that area", not "filed under that zone". Municipality aliases such as `--area kaltern` narrow only to the zone here — the response warns — so use `--search` when the answer must be about the village.

A22:

```bash
odh a22 status --limit 10 --json
odh mobility events --origin A22 --latest --limit 20
```

`a22 status` inspects a Mobility Timeseries event feed alongside `TrafficForecast`; neither is a live bulletin. Do not infer live incidents from `TrafficForecast`. Report an empty or stale event feed as "this feed returned no current data", never as evidence that the motorway is clear, and get current notices from `odh call tourism /v1/Announcement --param source=a22 --param rawsort=-LastChange`. For past local A22 incidents, say these feeds may not retain history and use dated external sources if needed.

## Mobility Measurements

For current availability, discover origin/datatype first, then filter freshness:

```bash
odh diagnostics ev-charging --origin <ORIGIN> --fresh-within 24h   # <ORIGIN> from mobility origins
odh diagnostics parking-forecasts --origin "Municipality Merano" --fresh-within 2h --forecast-minutes 60
odh mobility latest --station-type ParkingStation --data-type free --origin "Municipality Merano" --active --fresh-within 2h --sort newest --request-limit 10000 --limit 10 --format table
```

`EChargingStation` carries rows from well outside South Tyrol, and most fresh rows are not local. Check `scoordinate` before turning a count into a local claim.

Raw latest rows can contain stale inactive stations. Surface `warnings`. If diagnostics says `current_only`, report current occupancy but not stale forecasts.

Tourism events:

```bash
odh diagnostics tourism-events --date 2026-05-18 --limit 20
odh tourism poi --limit 1 --seed 42 --fields Detail.en.Title,GpsInfo
```

Check `date_status`, `location_status`, and `GpsInfo` before making “near me today” claims.

## Transit

```bash
odh gtfs datasets
odh gtfs realtime --dataset sta-time-tables --feed trip-updates --limit 5
odh transit stops search merano --limit 10
odh transit departures --stop-id <stop_id> --date 2026-05-16 --around 13:00 --mode train --json
odh transit trip --from-stop-id <from_id> --to-stop-id <to_id> --date 2026-05-16 --time 13:00 --mode train --json
odh transit journey --from-stop-id <from_id> --to-stop-id <to_id> --date 2026-05-16 --time 13:00 --max-transfers 3 --with-realtime --json
odh transit delay-stats --from auer --to brenner --time 14:05 --weekday saturday --json
```

Use stop IDs when names are ambiguous. `journey --with-realtime` annotates static routes with current GTFS-RT; it does not live-reroute. Missing realtime entities do not prove on-time service. Historical delay probability is unsupported without archived GTFS-RT; use `delay-stats` and do not guess.

## Evals

```bash
scripts/run-agent-evals.sh
```

Use `evals/agent/tasks.json` for manual scoring and `evals/agent/recipes.json` as machine-readable command recipes. Use evals to decide if repeated failures need docs, skill guidance, agent reasoning, or a narrow CLI feature.

## References

- https://opendatahub.com/api/
- https://docs.opendatahub.com/en/latest/datasets.html
- https://docs.opendatahub.com/en/latest/howto/mobility/getstarted.html
