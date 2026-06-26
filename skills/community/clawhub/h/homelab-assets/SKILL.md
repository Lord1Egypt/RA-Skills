---
name: homelab-assets
description: Track and manage homelab hardware inventory — servers, switches, UPS units, drives, cables, and accessories. Records purchase dates, prices, warranty expiration, power draw, and physical location. Answers questions like "What's my total homelab spend?", "What warranties expire this year?", "What's my estimated monthly power cost?", and generates insurance-ready asset reports. Triggers on: homelab inventory, hardware assets, what hardware do I have, warranty check, homelab spend, asset tracker, insurance report, homelab hardware, track hardware.
---

# Homelab Assets Skill

Manages a local JSON inventory of homelab hardware. All data lives at `~/.openclaw/workspace/homelab-assets/inventory.json`.

## Scripts

All scripts live in `scripts/`. Run with `python3 scripts/<script>.py [args]`. Use `--help` on any script for full usage.

### add_asset.py — Add a hardware asset

```
python3 scripts/add_asset.py \
  --name "Raspberry Pi 4" \
  --type server \
  --brand Raspberry Pi Foundation \
  --model "Pi 4 Model B 8GB" \
  --purchase-date 2023-06-15 \
  --purchase-price 85.00 \
  --warranty-months 12 \
  --power-watts 8 \
  --location "Rack Shelf 2" \
  --serial ABC123 \
  --notes "Runs Home Assistant"
```

Required: `--name`, `--type`. All others optional. UUID auto-generated.
Types: `server`, `switch`, `router`, `ups`, `drive`, `cable`, `accessory`, `other`

### update_asset.py — Update an existing asset

```
python3 scripts/update_asset.py --id <uuid> --status retired --location "Storage Box A"
python3 scripts/update_asset.py --search "Pi 4" --notes "Repurposed as DNS server" --power-watts 6
```

Target by `--id` (exact UUID) or `--search` (fuzzy name match). Updatable fields: `--status`, `--location`, `--notes`, `--power-watts`.
Statuses: `active`, `retired`, `sold`, `rma`

### inventory.py — List assets

```
python3 scripts/inventory.py
python3 scripts/inventory.py --type server --status active
python3 scripts/inventory.py --location "Rack" --warranty-expiring 90
python3 scripts/inventory.py --output json
```

Filters: `--type`, `--status`, `--location` (substring), `--warranty-expiring <days>`. Output: table (default) or `--output json`.

### report.py — Generate full asset report

```
python3 scripts/report.py
python3 scripts/report.py --kwh-rate 0.14 --output report.md
```

Produces Markdown with: total assets, total investment, estimated current value (straight-line depreciation over 5 years), total power draw, monthly power cost estimate, warranty alerts (expiring within 90 days), assets by type, assets by location. Configurable `--kwh-rate` (default: 0.12).

### search.py — Fuzzy search across all fields

```
python3 scripts/search.py "raspberry"
python3 scripts/search.py "rack shelf" --output json
```

Searches name, brand, model, location, notes, serial, type. Case-insensitive substring match across all text fields.

## Data Location

Default: `~/.openclaw/workspace/homelab-assets/inventory.json`
Override with env var: `HOMELAB_ASSETS_PATH=/path/to/inventory.json`

## References

See `references/power-estimates.md` for common homelab device power draw estimates.
See `assets/inventory.example.json` for example asset structure.
