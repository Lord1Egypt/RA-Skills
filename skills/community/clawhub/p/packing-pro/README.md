# Packing Pro

An agent skill that generates smart, categorized packing lists based on destination weather, trip duration, activities, and transport type.

## Features

- 🌦️ **Weather-adaptive** — cold→thermals, beach→sunscreen, monsoon→rain gear
- 📅 **Duration-aware** — scales quantities to trip length with laundry buffer
- 🎯 **Activity-driven** — specialized gear for hiking, swimming, business, skiing, etc.
- ✈️ **Transport-aware** — flight liquid limits, car accessories, train essentials
- ⚖️ **Weighted** — per-item weight estimates for baggage management
- 🔴 **Critical items** — highlights must-not-forget essentials

## Installation

```bash
cp -r packing-pro /path/to/skills/
```

## Usage

```bash
# Full specification
python3 scripts/packing_pro.py \
  --destination "Tokyo, Japan" \
  --duration 7 \
  --season winter \
  --activities hiking photography \
  --transport flight

# With temperature override
python3 scripts/packing_pro.py \
  --destination "Reykjavik, Iceland" \
  --duration 5 \
  --season winter \
  --temp-c -5 \
  --activities hiking \
  --transport flight \
  --output my_trip.json
```

### Parameters

| Parameter | Required | Description |
|---|---|---|
| `--destination` | Yes | Trip destination |
| `--duration` | Yes | Number of days (integer) |
| `--season` | Yes | `summer`, `winter`, `spring`, `autumn` |
| `--temp-c` | No | Override average temperature (°C) |
| `--activities` | No | Space-separated: `hiking`, `swimming`, `business`, `skiing`, `photography`, `formal` |
| `--transport` | No | `flight`, `train`, `car`, `bus` (default: `flight`) |
| `--output` | No | Output file path (default: stdout) |

## Output Format

JSON with:
- `critical_items` — must-not-forget essentials
- `categories` — clothing, toiletries, electronics, activity_gear, misc
- Each item has: `item`, `quantity`, `weight_g`, and optional `note`
- `estimated_total_weight_g` — total estimated weight

## Reference Documentation

- [Item Database](references/item-database.md) — full catalog of items with weights
- [Weather & Activity Logic](references/weather-logic.md) — selection rules explained

## License

MIT © Denis Voronin
