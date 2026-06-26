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
              "module": "github.com/galjos/odh-cli/cmd/odh@v0.3.0",
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
odh doctor --timeout 10s
```

Need `odh v0.3.0+` for the current command contracts, source/provenance fields, traffic helpers, GTFS/transit, filtered latest measurements, comma-safe `--param`, `transit journey --with-realtime`, and MCP server mode.

```bash
curl -fsSL https://raw.githubusercontent.com/galjos/odh-cli/main/scripts/install.sh | sh -s -- --version v0.3.0 --dir "$HOME/bin"
```

If running from the source repo, use `./odh`.

Agent hosts that prefer MCP over shell commands can run the same curated surface as Model Context Protocol tools with `odh mcp serve`; tool outputs follow the same JSON contracts and warnings as the CLI.

## Output Rules

- Curated commands may default to table. Add `--json` or `--format json` before parsing output.
- This applies especially to `traffic`, `a22 status`, `transit`, `tourism types`, `mobility types`, and `mobility datatypes`.
- Treat stderr as diagnostics, not data.
- Nonzero exit means failure. Exit `2` usually means bad invocation.
- For bounded agent loops, put the global timeout before the subcommand, for example `odh --timeout 20s traffic today --area bozen-unterland --json`.
- When unsure about command shape, run `odh <command> --help`; current help includes task-focused examples.
- Prefer discovery commands before guessing provider names, data types, stop IDs, or zone IDs.
- Prefer returned `source`, `source_detail`, `endpoint`, `archive`, `realtime`, and `warnings` fields over inferred provenance.
- Stable curated JSON fields are documented in `docs/json-contracts.md` in the repo.

## Discovery

```bash
odh apis
odh datasets search parking
odh openapi mobility
odh openapi tourism
odh mobility types --kind station
odh mobility origins --station-type ParkingStation
odh mobility datatypes --station-type TrafficSensor --origin A22 --limit 1000 --json
```

Always run `odh mobility origins --station-type <type>` before filtering any query with `--origin`, even when the origin seems obvious (A22, ALPERIA, PROVINCE_BZ): origin names are upstream vocabulary, and a catalogued origin or datatype is not proof that open measurement rows exist.

Use `odh call <api> <path> --param key=value` for known endpoints. `--param` is repeatable and values may contain commas.

## Traffic

Roadworks, closures, and road events:

```bash
odh traffic zones --json
odh traffic categories --json
odh traffic today --area ueberetsch-unterland --type roadworks --json
odh traffic search badia --today --zone-id 6 --json
odh traffic today --near 46.42,11.25 --radius 15km --json
```

Prefer `traffic` over raw `mobility events --origin PROVINCE_BZ`. Surface stale/source warnings. Do not present stale open-ended rows as confirmed current closures.

A22:

```bash
odh a22 status --limit 10 --json
odh mobility events --origin A22 --latest --limit 20
```

`a22 status` is current/live-oriented. Do not infer live incidents from `TrafficForecast`. For past local A22 incidents, say ODH/A22 live feeds may not retain history and use dated external sources if needed.

## Mobility Measurements

For current availability, discover origin/datatype first, then filter freshness:

```bash
odh diagnostics ev-charging --origin ALPERIA --fresh-within 24h
odh diagnostics parking-forecasts --origin "Municipality Merano" --fresh-within 2h --forecast-minutes 60
odh mobility latest --station-type ParkingStation --data-type free --origin "Municipality Merano" --active --fresh-within 2h --sort newest --request-limit 10000 --limit 10 --format table
```

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
