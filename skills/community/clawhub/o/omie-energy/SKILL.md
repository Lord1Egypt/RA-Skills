---
name: omie-energy
description: "Fetch Iberian day-ahead electricity prices for Portugal and Spain from OMIE via the OMIEData library, plan cheapest appliance or EV charging windows, compare PT vs ES prices, and trigger smart-home actions from price thresholds."
homepage: https://www.omie.es
metadata:
  openclaw:
    emoji: "⚡"
    primaryEnv: OMIE_AREA
    requires:
      bins:
        - python3
---

# OMIE Energy (Portugal / Spain)

## When to use

Use when the user asks about:
- Current or upcoming electricity spot prices in Portugal or Spain
- Iberian OMIE day-ahead marginal prices
- Cheapest time to run a load (dishwasher, laundry, EV charging)
- Portugal vs Spain price comparison
- Device actions based on price thresholds

## Setup

Install Python dependencies once:

```bash
python3 -m pip install -r requirements.txt
```

No API credentials are required — OMIE publishes day-ahead marginal prices publicly.

Optional default area (`PT` or `ES`):

```bash
export OMIE_AREA="PT"
```

You can also copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Alternatively, for shareable/persistent configuration, create:
`~/.config/omie-energy/config.json`

```bash
cp config.json.example ~/.config/omie-energy/config.json
```

Configuration precedence:
1) environment variables (`OMIE_*`)
2) `~/.config/omie-energy/config.json`
3) default area `PT`

## Run

Use the wrapper from the skill directory:

```bash
bash run.sh prices
```

## Commands

### 1) Fetch current and upcoming hourly day-ahead prices

Portugal (default):

```bash
bash run.sh prices --hours 36
```

Spain:

```bash
bash run.sh prices --area ES --hours 36
```

Custom date window:

```bash
bash run.sh prices --area PT --start 2026-06-01 --end 2026-06-07 --hours 48
```

### 2) Find optimal time for appliance or EV charging

Estimate hours from `kwh / power-kw`, then find cheapest contiguous block:

```bash
bash run.sh optimize \
  --area PT \
  --kwh 28 \
  --power-kw 11 \
  --window-start "2026-06-20T18:00:00+01:00" \
  --window-end "2026-06-21T08:00:00+01:00"
```

For fixed duration instead of kWh:

```bash
bash run.sh optimize --area PT --duration-hours 2
```

### 3) Compare Portugal vs Spain prices

```bash
bash run.sh compare --hours 24
```

### 4) Control smart-home devices by price threshold

Thresholds use **EUR/kWh** (divide OMIE EUR/MWh by 1000).

Dry-run:

```bash
bash run.sh control \
  --area PT \
  --price-below 0.10 \
  --on-command "ha service call switch.turn_on --entity_id switch.ev_charger" \
  --off-command "ha service call switch.turn_off --entity_id switch.ev_charger"
```

Execute commands:

```bash
bash run.sh control \
  --area PT \
  --price-above 0.20 \
  --on-command "ha service call switch.turn_on --entity_id switch.boiler" \
  --off-command "ha service call switch.turn_off --entity_id switch.boiler" \
  --execute
```

## Notes

- Data source: OMIE (Iberian electricity market operator) via the `OMIEData` Python package.
- Concepts: `PRICE_PT` (Portugal), `PRICE_SP` (Spain).
- Prices are day-ahead **marginal** market prices in **EUR/MWh**; the CLI also shows **EUR/kWh**.
- Timestamps use Iberian local time (`Europe/Lisbon`).
- OMIE can expose `H25` on daylight-saving transition days.
- Tomorrow's prices are typically published in the afternoon; if upcoming hours look short, widen `--start`/`--end`.
- `optimize` and `control` use EUR/kWh internally for threshold compatibility with other energy skills.
- Start with dry-run control mode and verify commands before `--execute`.

## Safety

- No secrets required, but keep `.env` local if you use it for preferences.
- Keep `--execute` off until threshold logic is verified in dry-run.
- Treat `--on-command` and `--off-command` as trusted input only (they run as shell commands).

## Publisher Checklist (ClawHub)

- Include: `SKILL.md`, `run.sh`, `omie_energy.py`, `requirements.txt`, `.env.example`, `config.json.example`, `.gitignore`
- Exclude: `.env`, `__pycache__/`, local logs, temporary files
- Validate from a clean shell:
  - `python3 -m pip install -r requirements.txt`
  - `bash run.sh prices --area PT --hours 6`
  - `bash run.sh prices --area ES --hours 6`
  - `bash run.sh compare --hours 6`
  - `bash run.sh optimize --area PT --duration-hours 2`
  - `bash run.sh control --area PT --price-below 0.10 --on-command "echo on" --off-command "echo off"`
