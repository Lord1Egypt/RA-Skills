---
name: nzta-traffic
description: Query real-time NZ state highway traffic conditions from the Waka Kotahi NZTA Traffic and Travel API. Use when checking road events, incidents, closures, roadworks, traffic cameras, or travel conditions on New Zealand highways. Covers all 14 NZ regions (Northland to Southland). No API key required. Use for queries like "how's the traffic", "any road closures", "check SH1 conditions", or "traffic cameras near Wellington".
---

# NZTA Traffic

Query the Waka Kotahi Traffic and Travel REST API for real-time state highway conditions across New Zealand.

## Quick Start

Check road events for a region:

```bash
scripts/nzta-traffic.sh --region Wellington
```

Check a specific highway:

```bash
scripts/nzta-traffic.sh --journey 10
```

Check traffic cameras in a region:

```bash
scripts/nzta-traffic.sh --cameras --region Wellington
```

## Script Usage

```
scripts/nzta-traffic.sh [options]

Options:
  --region <name|id>    Region name or ID (e.g. "Wellington" or "9")
  --journey <id>        Journey/highway ID (e.g. 10 for SH1 Wellington)
  --bbox <minlon,minlat,maxlon,maxlat>  Bounding box query
  --cameras             List traffic cameras instead of events
  --list-regions        List all region names and IDs
  --list-journeys       List journeys for a region (requires --region)
  --json                Output raw JSON instead of formatted summary
  --zoom <level>        Geometry zoom level, -1 for no geometry (default: -1)
```

## Region and Journey Lookup

Run `--list-regions` to get region IDs, then `--list-journeys --region <name>` to find highway journey IDs for that region.

Common Wellington region journeys: SH1 (ID 10), SH2 (ID 9), SH58 (ID 12), SH59 (ID 341).

For full endpoint reference and response field descriptions, see [references/api-endpoints.md](references/api-endpoints.md).

## Event Impact Levels

- **Closed** — road is closed
- **Major delays** — significant delays expected
- **Minor delays** — some delays
- **Caution** — be aware, proceed carefully
- **Watch and observe** — informational

## Notes

- API base: `https://trafficnz.info/service/traffic/rest/4/`
- No authentication required
- Returns JSON with `Accept: application/json` header
- Empty response (`"response": ""`) means no active events — that's good news
