---
name: nft-floor-price-monitor
description: Monitor NFT collection floor prices and send alerts via Discord DM when floors hit target levels. Use when the user wants to (1) check the current floor price of an NFT collection (Blur, OpenSeafloor, NFTfi, etc.), (2) set floor price alerts, (3) compare multiple collections, (4) track floor price history, (5) DM alerts to Discord when floors cross thresholds. Triggers: "NFT floor", "floor price", "monitor NFT", "NFT alert", "collection floor", "Blur floor", "OpenSea floor", "NFT portfolio", "floor alert".
version: 1.0.0
author: 9527Craft
price: 49
category: nft
tags: [nft, floor-price, blur, opensea, web3, monitor, alerts, discord, trading]
license: MIT
---

# NFT Floor Price Monitor

Monitor NFT collection floor prices and receive Discord DM alerts when floors hit your targets.

## Quick Usage

```bash
uv run python scripts/floor_monitor.py --collection bored-ape --target 80 --discord
uv run python scripts/floor_monitor.py --collection bayc --target 100 --direction below
uv run python scripts/floor_monitor.py --collection doodles --target 10 --output json
uv run python scripts/floor_monitor.py --collection mutant-ape-punks --compare 3 --output json
```

## Core Features

1. **Live Floor Price** — Current floor from multiple sources (Blur, OpenSea)
2. **Price Alerts** — Get a Discord DM when floor crosses your target
3. **Multi-Collection Compare** — Compare up to 5 collections at once
4. **Direction Triggers** — Alert when floor goes above OR below target
5. **JSON Output** — For automation pipelines: `--output json`

## Scripts

- `scripts/floor_monitor.py` — Main script. Run standalone with `uv run python scripts/floor_monitor.py [args]`

### Arguments

| Arg | Description |
|-----|-------------|
| `--collection` | Collection slug (e.g. bored-ape, bayc, doodles) — **required** |
| `--target` | Target floor price in ETH for alert |
| `--direction` | `above` or `below` (default: below) |
| `--discord` | Send Discord DM alert when triggered |
| `--discord-webhook` | Discord webhook URL (or set env var `DISCORD_WEBHOOK_URL`) |
| `--compare` | Compare N collections at once |
| `--output` | `text` (default) or `json` |

## Collection Slugs

Common collection slugs (slug for URL: opensea.com/collection/{slug}):

| Collection | Slug |
|------------|------|
| Bored Ape Yacht Club | bored-ape-yacht-club |
| Mutant Ape Yacht Club | mutant-ape-yacht-club |
| Doodles | doodles |
| Azuki | azuki |
| Clone X | clonex |
| Others | Check OpenSea or Blur for the correct slug |

## Alert Logic

- `--direction below` (default): Alert when floor drops to or below target
- `--direction above`: Alert when floor rises to or above target
- Automatic alert on 24h change > 10%

## Discord DM Setup

1. Set `DISCORD_WEBHOOK_URL` env var, or pass `--discord-webhook https://...`
2. Use `--discord` flag to enable DM alerts
3. The webhook will post an embedded alert message

## Technical Notes

- Uses CoinGecko NFT price data and OpenSea/Blur APIs (no auth required)
- Rate limiting: respect API limits, add delays between requests
- Floor prices are in ETH by default
