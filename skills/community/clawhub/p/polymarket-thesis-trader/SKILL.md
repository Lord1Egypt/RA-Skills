---
name: polymarket-thesis-trader
description: Scan Polymarket markets for a configurable thesis, compare your probability to the market price, and trade only when the edge clears a safety threshold.
tags:
  - aion-sdk
  - aion
  - aionmarket
metadata:
  author: "GitHub Copilot"
  version: "1.0.0"
  displayName: "Polymarket Thesis Trader"
  difficulty: "intermediate"
---

# Polymarket Thesis Trader

> **This is a template.** The default signal is a user-supplied thesis probability
> for markets matching a query string. Remix it with your own model, news feed,
> research pipeline, or alternative market-selection logic. The skill handles market
> discovery, context checks, execution tags, dry-run safety, and operator summaries.

## What It Does

This skill searches Polymarket for markets matching a thesis query such as `bitcoin`,
`fed`, or `election`, then compares your fair probability to the current market price.
If the gap exceeds the configured minimum edge, it proposes or executes a trade.

Default behavior:

- Read candidate markets from AION market discovery.
- Compute edge as `fair_value - yes_price` for YES trades or `(1 - fair_value) - no_price` for NO trades.
- Check market context before acting.
- Skip trades when warnings or flip-flop risk are present.
- Default to dry-run unless `--live` is passed.
- Tag every trade with `source` and `skill_slug`.

## Strategy Inputs

The entrypoint accepts CLI flags or environment variables:

- `--query` or `MARKET_QUERY`: Search term for market discovery.
- `--thesis-probability` or `THESIS_PROBABILITY`: Your fair probability from `0` to `1`.
- `--min-edge` or `MIN_EDGE`: Minimum required edge before trading.
- `--trade-amount` or `TRADE_AMOUNT_USD`: Position size per trade.
- `--limit` or `MARKET_LIMIT`: Max markets to scan.
- `--live` or `RUN_LIVE=true`: Enable real trading.

## Example Usage

Dry-run:

```bash
python trade_thesis.py --query bitcoin --thesis-probability 0.62
```

Live trading:

```bash
python trade_thesis.py --query bitcoin --thesis-probability 0.62 --min-edge 0.08 --trade-amount 5 --live
```

Environment-driven run:

```bash
export AION_API_KEY=your_api_key
export MARKET_QUERY=bitcoin
export THESIS_PROBABILITY=0.62
python trade_thesis.py
```

## Required Credentials

- `AION_API_KEY`: Required for market reads and trade execution.

## Remix Ideas

- Replace the thesis probability input with a custom forecast model.
- Use `get_briefing()` opportunity markets instead of query search.
- Add venue-specific sizing rules.
- Add position caps, PnL-aware de-risking, or stale-order cancellation.
- Schedule multiple automaton runs for different themes.

## Publishing

From inside this skill folder:

```bash
npx clawhub@latest publish . --slug polymarket-thesis-trader --version 1.0.0
```

Then verify installation:

```bash
npx clawhub@latest install polymarket-thesis-trader
```
