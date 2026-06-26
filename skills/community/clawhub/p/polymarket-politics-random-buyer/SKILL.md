---
name: polymarket-politics-random-buyer
description: Randomly finds a live Polymarket politics market, checks trading context, and buys 1 USDC by default with explicit dry-run and live modes for AION Market.
metadata:
  author: "GitHub Copilot"
  version: "1.0.0"
  displayName: "Polymarket Politics Random Buyer"
  difficulty: "intermediate"
---

# Polymarket Politics Random Buyer

This skill is a publishable AION trading template that scans Polymarket politics markets, randomly picks one valid candidate, checks market context, and buys 1 USDC by default.

> **This is a template.** The default signal is intentionally simple: pick a random live politics market that passes context checks, then buy 1 USDC on the chosen side. Remix the selection logic, side logic, sizing, and filters with your own research or model. The skill handles market discovery, guardrails, and AION trade tagging.

## When To Use

Use this skill when you want a minimal AION-compatible Polymarket trading skill that can discover politics markets automatically instead of taking a fixed market id.

## Skill Folder

This skill ships with three files:

- SKILL.md
- clawhub.json
- politics_random_buyer.py

## Defaults

- Venue: polymarket
- Search scope: politics and election-related Polymarket markets
- Trade side: YES
- Trade size: 1.0 USDC
- Execution mode: dry-run unless `--live` is passed
- Trade source: `sdk:polymarket-politics-random-buyer`
- Skill slug: `polymarket-politics-random-buyer`

## Required Inputs

The skill expects the user to provide:

- `AION_API_KEY` or `AIONMARKET_API_KEY`
- `WALLET_PRIVATE_KEY`

Optional inputs:

- `SEARCH_QUERIES` as a comma-separated override for the politics search terms
- `TRADE_SIZE` to override the 1 USDC default
- `TRADE_SIDE` to choose `yes` or `no`
- `MAX_MARKETS` to control how many market search results to inspect
- `RANDOM_SEED` to make the random pick reproducible
- `REASONING_PREFIX` to customize the public reasoning string

## Safety Rules

1. Always fetch market context before trading.
2. Always default to dry-run. Live trading requires explicit `--live`.
3. Always require the user's API key and wallet private key from env.
4. Always attach `source`, `skill_slug`, and human-readable `reasoning`.
5. Skip candidates when market context returns warnings or flip-flop risk.
6. Return a clear HOLD result when no valid politics market passes the checks.

## Decision Logic

1. Search Polymarket using politics-related keywords.
2. Flatten nested event -> market results into tradeable sub-markets.
3. Filter to live politics candidates with usable identifiers.
4. Randomize the candidate list.
5. Check market context candidate by candidate until one passes safeguards.
6. Buy the configured side for the configured amount.

## Example Commands

Dry-run:

```bash
python politics_random_buyer.py
```

Live trade with the default 1 USDC size:

```bash
python politics_random_buyer.py --live
```

Deterministic pick for testing:

```bash
python politics_random_buyer.py --seed 7 --max-markets 30
```

## Expected Operator Output

The script prints an operator summary like:

```text
Skill: polymarket-politics-random-buyer
Venue: polymarket
Wallet: 0x1234...abcd
Scanned markets: 42

Decision:
- TRADE YES size=1.00 market=US election market here mode=dry-run

Risk alerts:
- none
```

## Remix Ideas

- Change the politics filters to target only US election markets.
- Replace random selection with volume, liquidity, or edge ranking.
- Add position checks before entering another politics trade.
- Flip the side dynamically based on your own forecast signal.