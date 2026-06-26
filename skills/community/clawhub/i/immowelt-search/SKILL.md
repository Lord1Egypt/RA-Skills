---
name: immowelt-search
description: Search immowelt.at and immowelt.de real estate listings (apartments, houses) via HTML parsing. No browser needed. Search any Austrian or German location with price/room filters. Get full expose details including heating type, energy source, building condition, year built, energy class (HWB/fGEE), parking, and features. Use for Austrian or German property searches, immowelt queries, or building property reports. Triggers on "immowelt", "Austrian real estate", "German real estate", "Wohnung kaufen", "Haus kaufen", property search Austria Germany.
metadata: {"openclaw":{"emoji":"🏘️","requires":{"bins":["python3"]}}}
---

# Immowelt Real Estate Search

Search and retrieve property listings from immowelt.at (Austria) and immowelt.de (Germany) via HTML parsing. No browser automation needed.

## Prerequisites

Requires `python3` with the `requests` library (pre-installed in most environments).

## Quick Start

### Search listings

```bash
# Apartments for sale in Vienna, max €300k
python3 scripts/immowelt-search.py --location wien --type apartment --max-price 300000

# Houses in Wien, max €350k
python3 scripts/immowelt-search.py --location wien --type house --max-price 350000

# With room filter
python3 scripts/immowelt-search.py --location wien --type apartment --max-price 300000 --min-rooms 2

# German location
python3 scripts/immowelt-search.py --country de --location muenchen --type apartment --max-price 400000

# JSON output
python3 scripts/immowelt-search.py --location wien --type apartment --format json

# With full expose details (heating, energy, condition) — slower
python3 scripts/immowelt-search.py --location wien --type apartment --max-price 300000 --with-details
```

### Get expose details for a specific listing

```bash
python3 scripts/immowelt-search.py --expose 0a848843-86ba-4093-bd93-166258e909f7
python3 scripts/immowelt-search.py --expose 0a848843-86ba-4093-bd93-166258e909f7 --format json
```

Expose detail fields include:
- **heating**: Zentralheizung, Fußbodenheizung, Etagenheizung, etc.
- **energy_source**: Gas, Fernwärme, Wärmepumpe, Öl, Pellets, Strom, etc.
- **condition**: Erstbezug, Altbau, Gepflegt, Renovierungsbedürftig, etc.
- **year**: Construction year
- **hwb** + **hwb_class**: Heizwärmebedarf (kWh/m²·a) + class (A++ to G)
- **fgee** + **fgee_class**: Gesamtenergieeffizienz factor + class
- **price_note**: Additional price info (Stellplatz, etc.)
- **features**: Listed features
- **created** / **updated**: Listing dates

## Property Types

| CLI Type | Immowelt Category |
|----------|------------------|
| `apartment` | Wohnungen kaufen |
| `house` | Häuser kaufen |
| `apartment-rent` | Wohnungen mieten |
| `house-rent` | Häuser mieten |

## Location Slugs

Locations use the immowelt URL slug — taken directly from the URL path at immowelt.at or immowelt.de.

### Austria (--country at)

| Location | Slug |
|----------|------|
| Wien | `wien` |
| Niederösterreich | `niederoesterreich` |
| Oberösterreich | `oberoesterreich` |
| Salzburg | `salzburg` |
| Steiermark | `steiermark` |
| Kärnten | `kaernten` |
| Tirol | `tirol` |
| Vorarlberg | `vorarlberg` |
| Burgenland | `burgenland` |
| Mödling (NÖ) | `bezirk-moedling` |
| Baden (NÖ) | `bezirk-baden` |
| Korneuburg (NÖ) | `bezirk-korneuburg` |

### Germany (--country de)

| Location | Slug |
|----------|------|
| Bayern | `bayern` |
| Berlin | `berlin` |
| Hamburg | `hamburg` |
| München | `muenchen` |
| Passau | `passau` |

Any valid immowelt location slug works — these are just examples.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--country` | `at` (Austria, default) or `de` (Germany) |
| `--location` | Location slug (required for search) |
| `--type` | Property type: `apartment`, `house`, `apartment-rent`, `house-rent` |
| `--max-price` | Maximum price in EUR |
| `--min-rooms` | Minimum rooms |
| `--max-pages` | Max result pages (default: 5, ~32 items/page) |
| `--with-details` | Fetch expose for each listing (slower, includes heating/energy) |
| `--expose` | Get details for a specific expose UUID |
| `--format` | `text` or `json` |

## URL Filter Parameters

Immowelt uses URL query parameters for filtering:
- `pma` — Max price
- `rmi` — Min rooms
- `cp` — Page number

## Notes

- Search returns ~32 listings per page
- Expose UUIDs look like: `0a848843-86ba-4093-bd93-166258e909f7`
- Be respectful with request rates — add delays (~300ms) between detail requests
- The `--min-rooms` filter is applied server-side but may not always be exact
