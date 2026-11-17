[![ClawHub](https://img.shields.io/badge/ClawHub-maps-cli-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: maps-cli
version: 2.0.0
description: Advanced OpenStreetMap CLI: geocode, reverse geocode, route, POI search, timezone, CSV export
tags: ["maps", "osm", "geocode", "routing", "poi", "cli", "location", "python", "open-source", "agent", "automation", "MIT"]
---

# Maps CLI (OpenStreetMap)

**Geocode, reverse-geocode, route, POI search, and timezone lookup — all via OpenStreetMap, with CSV export.**

> *Keywords: maps, osm, geocode, routing, poi, cli, location, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Maps need an API key and a SaaS for even basic geocoding/routing. Maps CLI (OpenStreetMap) solves this: Geocode, reverse-geocode, route, POI search, and timezone lookup — all via OpenStreetMap, with CSV export.

**Best for:** Developers, field/ops apps, and agents needing location data.

## Features

- **Geocode an address**
- **Reverse-geocode coordinates**
- **Route between two points**
- **Search POIs by category/radius**
- **CSV export + timezone**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/maps-cli/main/maps_cli.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python maps_cli.py self-test     # prove it works end-to-end
python maps_cli.py geocode --help   # geocode subcommand
python maps_cli.py reverse --help   # reverse subcommand
python maps_cli.py route --help   # route subcommand
python maps_cli.py poi --help   # poi subcommand
python maps_cli.py timezone --help   # timezone subcommand
python maps_cli.py export --help   # export subcommand
```

## Use cases

1. Geocode an address
1. Reverse-geocode coordinates
1. Route between two points
1. Search POIs by category/radius
1. CSV export + timezone

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Google Maps API | No key, OSM-backed, free tier friendly. |
| Manual geocoding | One CLI for geocode/reverse/route/POI. |
| Spreadsheet maps | CSV export drops into BI. |

## FAQ (SEO / AEO)

**Q: Provider?**  
A: OpenStreetMap (Nominatim/OSRM) — no key for basic use.

**Q: Routing?**  
A: Yes — route between lat/lon.

**Q: POI?**  
A: Search by category within a radius.

**Q: Offline?**  
A: No — queries OSM live.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test maps-cli
        run: python maps_cli.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/maps-cli)
