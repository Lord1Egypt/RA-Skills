# omie-energy

Skill package for Iberian (Portugal/Spain) OMIE day-ahead price automation.

It provides CLI commands to:
- Show upcoming hourly marginal prices for PT or ES
- Find the cheapest contiguous charging/runtime window
- Compare Portugal vs Spain prices hour by hour
- Trigger on/off commands from price thresholds

Built on the [`OMIEData`](https://pypi.org/project/OMIEData/) Python library — the same source used in the [grid-pulse](../grid-pulse) project.

## Requirements

- Python 3.9+
- `OMIEData` and `pandas` (see `requirements.txt`)
- No API credentials (public OMIE data)

## Quick Start

```bash
python3 -m pip install -r requirements.txt
bash run.sh prices --area PT --hours 24
```

Optional default area:

```bash
cp .env.example .env
# edit OMIE_AREA=PT or ES
bash run.sh prices --hours 24
```

## Common Commands

```bash
# Portugal upcoming prices
bash run.sh prices --area PT --hours 36

# Spain upcoming prices
bash run.sh prices --area ES --hours 36

# PT vs ES comparison
bash run.sh compare --hours 24

# Cheapest 2-hour window in Portugal
bash run.sh optimize --area PT --duration-hours 2

# Cheapest window for energy target (kWh / kW => duration)
bash run.sh optimize --area PT --kwh 28 --power-kw 11

# Dry-run control (thresholds in EUR/kWh)
bash run.sh control \
  --area PT \
  --price-below 0.10 \
  --on-command "echo on" \
  --off-command "echo off"
```

## Price Units

- OMIE publishes **EUR/MWh** (marginal day-ahead price).
- The CLI also shows **EUR/kWh** (`EUR/MWh ÷ 1000`).
- `optimize` and `control` thresholds use **EUR/kWh** for consistency with `ostrom-energy` and `tibber-energy`.

## Safety

- `.env` is local-only and ignored by git.
- Keep control in dry-run first; only add `--execute` after validating thresholds.
- `--on-command`/`--off-command` run shell commands, so only use trusted command strings.

## Files

- `SKILL.md`: skill metadata and usage instructions
- `run.sh`: launcher that loads local env and executes Python script
- `omie_energy.py`: OMIEData fetch + optimization/control logic
- `requirements.txt`: Python dependencies
- `.env.example`: optional default area
- `config.json.example`: optional persisted config
