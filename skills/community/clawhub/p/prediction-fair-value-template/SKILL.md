---
name: prediction-fair-value-template
description: Scan Simmer markets for a configurable fair-value edge and buy YES or NO when the market price diverges enough from your thesis.
metadata:
  author: "GitHub Copilot"
  version: "1.0.0"
  displayName: "Prediction Fair Value Template"
  difficulty: "intermediate"
---

# Prediction Fair Value Template

This skill scans active Simmer-indexed markets matching a search query, compares the current market price to your fair probability, and places a trade only when the gap is large enough to justify action.

> **This is a template.** The default signal is a user-supplied fair probability plus a keyword market search.
> Remix it with your own model outputs, news signals, research pipeline, or external data.
> The skill handles discovery, sizing, context checks, redemption, and trade execution plumbing.

## What It Does

On each run, the skill:

1. Calls Simmer briefing and auto-redeem.
2. Searches active markets using `MARKET_QUERY`.
3. Compares each market's current YES price to `FAIR_PROBABILITY`.
4. Buys YES when the market is under your fair value by at least `MIN_EDGE`.
5. Buys NO when the market is over your fair value by at least `MIN_EDGE`.
6. Sizes the position with `simmer_sdk.sizing.size_position()`.
7. Checks market context before trading to avoid severe flip-flops, weak edge, or excessive slippage.
8. Defaults to dry-run unless you explicitly enable live trading.

## Required Files

This skill follows Simmer's manual build pattern for ClawHub:

- `SKILL.md`
- `clawhub.json`
- `trade_skill.py`

## Environment Variables

### Credentials

- `SIMMER_API_KEY` (required): Simmer API key from your dashboard.
- `WALLET_PRIVATE_KEY` (optional): Only needed for external-wallet self-custody mode on supported venues.

### Strategy Config

- `MARKET_QUERY`: Search term used to discover markets. Default: `bitcoin`
- `FAIR_PROBABILITY`: Your estimated YES probability from `0` to `1`. Default: `0.60`
- `MIN_EDGE`: Minimum pricing gap required to act. Default: `0.05`
- `MAX_MARKETS`: Maximum number of markets to inspect per run. Default: `5`
- `MAX_SLIPPAGE_PCT`: Skip trades if estimated slippage exceeds this threshold. Default: `0.15`
- `TRADING_VENUE`: `sim` or `polymarket`. Default: `sim`
- `SIMMER_ENABLE_LIVE`: Set to `true` to allow live order placement in automations. Default: `false`

## Safety Model

- Dry-run is the default.
- Every trade is tagged with `source` and `skill_slug`.
- Every trade includes public `reasoning`.
- Market context is checked before order placement.
- Sizing is based on bankroll and edge, not a hard-coded fixed stake.

## Local Usage

Dry-run:

```bash
export SIMMER_API_KEY="sk_live_..."
python trade_skill.py
```

Live mode:

```bash
export SIMMER_API_KEY="sk_live_..."
python trade_skill.py --live
```

Custom thesis:

```bash
export MARKET_QUERY="fed rates"
export FAIR_PROBABILITY="0.72"
export MIN_EDGE="0.06"
export TRADING_VENUE="sim"
python trade_skill.py
```

## Remix Ideas

- Replace `FAIR_PROBABILITY` with a model output.
- Use different fair probabilities by market category.
- Add external signals from a news API, a research pipeline, or your own classifier.
- Add stricter filters for time to resolution or liquidity.
- Change sizing thresholds to fit your risk tolerance.

## Publishing

From inside this skill folder:

```bash
npx clawhub@latest publish . --slug prediction-fair-value-template --version 1.0.0
```

Always publish with an explicit `--slug`.
