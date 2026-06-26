---
name: polymarket-divergence-trader
description: Trades a Simmer-indexed market when your estimated probability diverges from the live market price, with dry-run on sim by default, context checks, reasoning tags, and optional live execution on Polymarket through ClawHub.
metadata:
  author: "Saul Su"
  version: "1.0.0"
  displayName: "Polymarket Divergence Trader"
  difficulty: "intermediate"
---

# Polymarket Divergence Trader

This skill is a publishable Simmer trading template for ClawHub. It compares your probability estimate with the live market price, checks market context, and only places a trade when the edge clears a configurable threshold.

> **This is a template.** The default signal is probability divergence: if your model thinks the event is more likely than the market implies, the skill buys YES; if less likely, it buys NO. Remix the signal source with your own model, API, or research. The skill handles trade discipline, operator output, and Simmer trade tagging.

## When To Use

Use this skill when an agent already has a probability estimate for a specific Simmer-indexed market and needs a safe execution wrapper around that signal.

## Skill Folder

This skill ships with three files:

- SKILL.md
- clawhub.json
- divergence_trader.py

## Defaults

- Dry-run venue: sim
- Live venue: polymarket
- Trade size: 5.0
- Minimum edge: 0.05
- Execution mode: dry-run unless `--live` is passed
- Trade source: `sdk:polymarket-divergence-trader`
- Skill slug: `polymarket-divergence-trader`

## Required Inputs

The skill expects:

- `SIMMER_API_KEY`
- `MARKET_ID` for the target market
- `MY_PROBABILITY` as a decimal between `0` and `1`

Optional inputs:

- `TRADE_SIZE`
- `MIN_EDGE`
- `REASONING_PREFIX`
- `LIVE_VENUE` to override the live venue if you intentionally want something other than `polymarket`

## Safety Rules

1. Always fetch market context before deciding.
2. Always default to dry-run. Live trading requires explicit `--live`.
3. Always attach `source`, `skill_slug`, and human-readable `reasoning`.
4. Skip trading when context reports warnings, severe flip-flop risk, or excessive slippage.
5. Return `HOLD` when the edge is smaller than the configured threshold.
6. Pass the venue explicitly by choosing the correct client venue for dry-run versus live execution.

## Decision Logic

1. Read the live market probability from market context.
2. Compute `edge = my_probability - market_probability`.
3. If `edge >= min_edge`, buy YES.
4. If `edge <= -min_edge`, buy NO.
5. Otherwise hold.

## Example Commands

Dry-run:

```bash
python divergence_trader.py --market-id 12345 --my-probability 0.62
```

Live trade:

```bash
python divergence_trader.py --market-id 12345 --my-probability 0.62 --amount 5 --live
```

## Expected Operator Output

The script prints an operator-style summary:

```text
Skill: polymarket-divergence-trader
Venue: sim
Risk alerts:
- none

Decision:
- 12345: TRADE YES size=5.00 mode=dry-run edge=+7.0%
```

## Remix Ideas

- Replace `MY_PROBABILITY` with a forecast model output.
- Drive `MARKET_ID` from a market scanner.
- Add bankroll-aware sizing before the trade call.
- Extend the loop to poll on a cron schedule and auto-redeem winning positions.