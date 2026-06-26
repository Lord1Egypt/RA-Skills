---
name: kalshi-politics-random-buyer
description: Dry-run Kalshi skill that finds politics-related markets, picks a valid candidate at random, runs Simmer context checks, and proposes a trade plan without placing a real order.
metadata:
  author: "GitHub Copilot"
  version: "1.0.0"
  displayName: "Kalshi Politics Random Buyer"
  difficulty: "intermediate"
---

# Kalshi Politics Random Buyer

This skill scans Kalshi for politics-related markets, randomizes the candidate pool, checks Simmer context safeguards, and prints a manual-confirmation trade plan for one valid candidate.

> **This is a template.** The default signal is intentionally simple: find a politics market at random, then only keep it if context and edge checks still pass. Remix the query set, side logic, price filters, and sizing model with your own thesis.

## What It Does

On each run, the skill:

1. Searches Kalshi importable markets using politics-related queries.
2. Falls back to a global Kalshi scan when keyword searches return nothing.
3. Filters for politics candidates with usable tickers and URLs.
4. Ignores markets outside a configurable price band.
5. Randomizes the candidate list.
6. Ensures each candidate is indexed in Simmer using check-then-import.
7. Fetches Kalshi market context and skips risky candidates.
8. Picks YES or NO using a simple fair-probability edge rule.
9. Sizes the hypothetical trade with `simmer_sdk.sizing.size_position()`.
10. Prints a structured execution plan and reasoning for human review.

## Important Limitation

This template is intentionally non-executing.

- Passing `--live` is rejected.
- No real order is sent.
- No wallet private key is needed for the default workflow.
- The output is a manual-review execution plan, not an order.

## Required Files

- `SKILL.md`
- `clawhub.json`
- `trade_skill.py`

## Environment Variables

### Credentials

- `SIMMER_API_KEY` (required): Your Simmer API key.

### Strategy Config

- `SEARCH_QUERIES`: Comma-separated politics search terms. Default: `election,president,presidency,senate,house,governor,politics,campaign,ballot,nominee,party`
- `MAX_MARKETS_PER_QUERY`: Maximum Kalshi results to inspect per query. Default: `50`
- `MIN_PRICE`: Minimum YES price allowed. Default: `0.02`
- `MAX_PRICE`: Maximum YES price allowed. Default: `0.98`
- `FAIR_PROBABILITY`: Fair YES probability for edge checks. Default: `0.55`
- `MIN_EDGE`: Minimum edge required to produce a plan. Default: `0.02`
- `MAX_SLIPPAGE_PCT`: Skip candidates with excessive slippage. Default: `0.15`
- `RANDOM_SEED`: Optional integer seed for reproducible selection.

## Safety Model

- Manual-confirmation only.
- Uses Simmer context before proposing a trade.
- Skips severe flip-flop, HOLD/SKIP recommendations, resolved markets, and excessive slippage.
- Uses bankroll-aware sizing instead of a hard-coded stake.
- Avoids publishing wallet identifiers in reasoning.

## Local Usage

Default planning run:

```bash
export SIMMER_API_KEY="sk_live_..."
python trade_skill.py
```

Deterministic planning run:

```bash
export RANDOM_SEED="7"
python trade_skill.py
```

Custom politics search:

```bash
export SEARCH_QUERIES="president,election,governor"
export FAIR_PROBABILITY="0.60"
python trade_skill.py
```

## Remix Ideas

- Replace random candidate selection with volume or liquidity ranking.
- Add event-level filters for US elections only.
- Add position-awareness to avoid repeat exposure.
- Convert the dry-run plan into a proposal file instead of stdout.
