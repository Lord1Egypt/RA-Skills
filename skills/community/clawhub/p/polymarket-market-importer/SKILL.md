---
name: polymarket-market-importer
displayName: "Polymarket Market Importer"
description: Auto-discover and import Polymarket markets matching your keywords, tags, and volume criteria. Runs on a schedule so you never miss a new market worth trading. Set your filters once — the skill handles the rest.
version: "1.0.3"
authors:
  - name: "DjDyll"
difficulty: "beginner"
---

# 🎯 Polymarket Market Importer

> **This is a template.** The keywords, categories, and volume filters are yours to set. The skill handles the hunting — searching Polymarket on a schedule, filtering by your criteria, skipping what you've already seen, and importing the rest into Simmer. You configure the net, it catches the fish.

## Setup

1. **Install the SDK:**
   ```bash
   pip install simmer-sdk
   ```

2. **Set your API key:**
   ```bash
   export SIMMER_API_KEY="sk_live_..."
   ```

3. **Set your filters:**
   ```bash
   python market_importer.py --set keywords=bitcoin,ethereum,solana
   python market_importer.py --set min_volume=25000
   ```

4. **Dry run to verify:**
   ```bash
   python market_importer.py
   ```

5. **Go live:**
   ```bash
   python market_importer.py --live
   ```

## Configuration

| Parameter | Env Var | Default | Description |
|-----------|---------|---------|-------------|
| `keywords` | `IMPORTER_KEYWORDS` | `bitcoin,ethereum` | Comma-separated search terms |
| `min_volume` | `IMPORTER_MIN_VOLUME` | `10000` | Minimum 24h volume — filters out thin markets |
| `max_per_run` | `IMPORTER_MAX_PER_RUN` | `5` | Cap on imports per execution |
| `categories` | `IMPORTER_CATEGORIES` | `crypto` | Comma-separated category filters (crypto, politics, sports, etc.) |

## Quick Commands

```bash
# Dry run — preview what would be imported
python market_importer.py

# Import for real
python market_importer.py --live

# Check what you've already imported
python market_importer.py --positions

# Show current config
python market_importer.py --config

# Update a setting
python market_importer.py --set keywords=bitcoin,ethereum,xrp

# Quiet mode — only output on imports or errors
python market_importer.py --live --quiet
```

## Example Output

```
🎯 Polymarket Market Importer
==================================================

  [LIVE MODE] Importing markets for real.

  Config: keywords=bitcoin,ethereum | min_volume=10000 | max_per_run=5 | categories=crypto

  Searching for: bitcoin
    Found 12 importable markets
    3 already imported, 9 new
    Category match: 7

  Searching for: ethereum
    Found 8 importable markets
    2 already imported, 6 new
    Category match: 5

  Importing: "Will BTC exceed $150k by July 2026?" (vol: $125,000)
    ✅ Imported successfully
  Importing: "Will ETH reach $5k by June 2026?" (vol: $89,000)
    ✅ Imported successfully

  Summary: 20 found | 5 already seen | 2 imported (max 5)
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "No importable markets found" | Broaden your keywords or lower `min_volume` |
| "Import failed" | Daily quota may be hit (10/day free, 50/day Pro). Try next run. |
| "SIMMER_API_KEY not set" | Get your key from simmer.markets/dashboard → SDK tab |
| Markets not matching categories | Category filter checks question text and tags. Try different terms. |

## Schedule

Runs every 6 hours via cron (`0 */6 * * *`). Adjust in `clawhub.json` if needed.
