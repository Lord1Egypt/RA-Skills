---
name: polymarket-clob-microstructure
description: >
  Analyzes Polymarket CLOB order book microstructure to find structural inefficiencies.
  Scores markets 0-100 on liquidity gaps, order book imbalance, whale activity, and
  fake breakout detection. Generates actionable signals (ENTRY_OK, REDUCE_SIZE, SKIP,
  MEAN_REVERT) and trades the fade on fake breakouts for structural alpha.
metadata:
  author: "Mibayy"
version: "2.0.4"
  displayName: "CLOB Microstructure Scanner"
  difficulty: "advanced"
  type: "automaton"
---

# CLOB Microstructure Scanner

Structural alpha from Polymarket order book analysis. Nobody else on Simmer does this.

## What It Does

Pulls raw order book data from Polymarket's CLOB API and scores each market on four
microstructure dimensions:

| Dimension | What It Measures |
|-----------|-----------------|
| **Liquidity Gaps** | Thin zones in the book where price can jump |
| **Order Book Imbalance** | Bid vs ask weight asymmetry |
| **Whale Activity** | Large single orders relative to book depth |
| **Fake Breakout Detection** | Sudden moves on thin volume that revert |

Each dimension scores 0-25, combined into a 0-100 inefficiency score.

## Signals

- **ENTRY_OK** — Normal conditions, standard sizing
- **REDUCE_SIZE** — Elevated microstructure risk, cut position size
- **SKIP** — Too dangerous, stay out
- **MEAN_REVERT** — Fake breakout detected, fade the move

The bot only trades on MEAN_REVERT signals, fading fake breakouts via SimmerClient.

## Configuration

- Runs every 5 minutes via cron
- Defaults to dry-run; pass `--live` for real execution
- Requires `SIMMER_API_KEY` environment variable

## Usage

```bash
# Dry run (default)
python clob_microstructure.py

# Live trading
python clob_microstructure.py --live

# Quiet mode for cron
python clob_microstructure.py --live --quiet
```

> 🧪 **Remixable Template** — Fork this skill and tweak the scoring weights,
> signal thresholds, or add your own microstructure indicators. The modular
> scoring system makes it easy to extend.
