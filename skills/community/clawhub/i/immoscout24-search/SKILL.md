---
name: immoscout24-search
description: Search ImmoScout24 (Germany) real estate listings using their mobile API. Bypasses anti-bot/DataDome protection. Search apartments, houses for buy/rent with filters. Get full expose details including heating, energy, parking, condition. Use when searching German property listings, checking ImmoScout24 exposes, or building property reports. Triggers on "immoscout", "immobilienscout24", "IS24", "Wohnung kaufen Deutschland", "Haus kaufen Bayern", or any German real estate search.
---

# ImmoScout24 Search

Search and retrieve property listings from ImmoScout24.de using their mobile API. No browser needed — bypasses DataDome anti-bot completely.

## Prerequisites

Requires `immoscout` Python package:
```bash
pip3 install --break-system-packages immoscout
```

## Quick Start

### Search listings

```bash
# Apartments for sale in Passau area, max €300k, 2+ rooms
python3 scripts/immoscout24-search.py --region /de/bayern/passau-kreis --type apartmentbuy --max-price 300000 --min-rooms 2

# Houses for sale in Passau area, max €350k
python3 scripts/immoscout24-search.py --region /de/bayern/passau-kreis --type housebuy --max-price 350000

# JSON output for machine processing
python3 scripts/immoscout24-search.py --region /de/bayern/passau-kreis --type apartmentbuy --max-price 300000 --format json
```

### Get expose details (heating, energy, parking)

```bash
python3 scripts/immoscout24-search.py --expose 166875438
python3 scripts/immoscout24-search.py --expose 166875438 --format json
```

Expose details include:
- **Heizungsart** (heating type): Zentralheizung, Fußbodenheizung, Etagenheizung, etc.
- **Energieträger** (energy source): Erdgas, Fernwärme, Wärmepumpe, Öl, Pellets, etc.
- **Garage/Stellplatz** (parking): Tiefgarage, Carport, Stellplatz, etc.
- **Baujahr** (year built), **Objektzustand** (condition)
- **Energieverbrauchskennwert** (energy rating)
- Internal fields: `obj_heatingType`, `obj_parkingSpace`, `obj_condition`, `obj_purchasePrice`

## Real Estate Types

| Type | Description |
|------|-------------|
| `apartmentbuy` | Apartments for sale (Eigentumswohnung) |
| `housebuy` | Houses for sale (Haus kaufen) |
| `apartmentrent` | Apartments for rent (Mietwohnung) |
| `houserent` | Houses for rent (Haus mieten) |

## Region Format

Regions use the path format: `/de/{bundesland}/{kreis-oder-stadt}`

Common regions:
| Region | Path |
|--------|------|
| Passau (Kreis) | `/de/bayern/passau-kreis` |
| Passau (Stadt) | `/de/bayern/passau` |
| München | `/de/bayern/muenchen` |
| Berlin | `/de/berlin/berlin` |
| Hamburg | `/de/hamburg/hamburg` |
| Köln | `/de/nordrhein-westfalen/koeln` |
| Frankfurt | `/de/hessen/frankfurt-am-main` |

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--region` | Region geocode (required for search) |
| `--type` | Real estate type (default: apartmentbuy) |
| `--max-price` | Maximum price in EUR |
| `--min-rooms` | Minimum number of rooms |
| `--max-pages` | Max result pages to fetch (default: 5, 20 items/page) |
| `--expose` | Get details for a specific expose ID |
| `--format` | Output format: `text` or `json` |

## Typical Workflow for Property Reports

1. **Search** multiple regions and types:
```bash
python3 scripts/immoscout24-search.py --region /de/bayern/passau-kreis --type apartmentbuy --max-price 300000 --min-rooms 2 --format json > /tmp/is24-apt.json
python3 scripts/immoscout24-search.py --region /de/bayern/passau-kreis --type housebuy --max-price 350000 --format json > /tmp/is24-house.json
```

2. **Get expose details** for interesting listings to check heating type:
```bash
python3 scripts/immoscout24-search.py --expose 166875438 --format json
```

3. **Filter** based on heating, condition, energy rating, parking.

4. **Compile report** with URLs, prices, heating info, and location details.

## Notes

- Uses IS24 mobile API (`api.mobile.immobilienscout24.de`) — no browser or authentication needed
- Rate limiting is lenient but don't hammer it — add small delays between expose lookups
- Listing URLs follow pattern: `https://www.immobilienscout24.de/expose/{id}`
- Search returns: id, title, price, area, rooms, address, postcode, published date
- Expose returns: full details including heating, energy, parking, condition, year built
