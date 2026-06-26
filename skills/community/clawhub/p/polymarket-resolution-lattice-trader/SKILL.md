---
name: polymarket-resolution-lattice-trader
description: Trades Polymarket markets by detecting logical inconsistencies between related contracts such as earlier-vs-later deadlines and prerequisite-vs-downstream event chains. Use when you want a non-template strategy driven by cross-market probability structure rather than single-market narrative.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Resolution Lattice Trader
  difficulty: advanced
---

# Resolution Lattice Trader

> **This is a template.**
> The default signal is cross-market inconsistency detection across deadline lattices and prerequisite chains — remix it with better parsers, richer rule extraction, or external event ontologies.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Most prediction bots make one-market judgments: find a market, estimate whether YES is too cheap or too expensive, then size the trade.

This skill does something else. It builds a small logical graph across related Polymarket markets and looks for violations.

Examples:

- **Temporal monotonicity**: "Will X happen before June?" cannot be more likely than "Will X happen before December?"
- **Prerequisite chains**: "Will candidate X become president?" should not exceed "Will candidate X win the nomination?" when nomination is a necessary step.

When those relationships break, the market is not just wrong in an opinionated sense — it is internally inconsistent.

## Signal Logic

### Default Signal: Resolution-Lattice Inconsistency

1. Discover markets with structurally linked wording such as `before`, `by`, `nominee`, `president`, `approval`, and similar milestone language
2. Parse each market question into a coarse subject plus a relation type
3. Group related markets into a local graph
4. Score violations of:
   - earlier deadline <= later deadline
   - prerequisite event >= downstream event
5. Trade only the leg with both:
   - a real graph inconsistency
   - threshold confirmation from `YES_THRESHOLD` / `NO_THRESHOLD`

This means the strategy is not trying to be smarter than the news. It is trying to be stricter than the market.

## What Makes It Different

- It is **cross-market**, not single-market
- It uses **logical constraints**, not only keywords or narrative bias
- It sizes conviction from **inconsistency magnitude**, not from raw extremeness alone

## Current Constraint Families

### 1. Temporal Lattice

If two markets refer to the same event with different deadlines, the earlier deadline must be less likely than or equal to the later one.

If the market prices:

- `Will X happen before June 2026?` = 44%
- `Will X happen before December 2026?` = 37%

then the graph is broken. The strategy prefers:

- `NO` on the earlier contract if it is already expensive enough
- `YES` on the later contract if it is already cheap enough

### 2. Prerequisite Chain

If a downstream event requires an upstream event, the downstream contract should not be more likely.

Example:

- `Will Candidate X win the nomination?` = 41%
- `Will Candidate X become president?` = 53%

The graph implies:

- nomination should not be lower than presidency
- therefore the strategy looks for `YES nomination` and/or `NO presidency`

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` mean nothing runs automatically until configured in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as a high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `35` | Max USDC per trade at full conviction |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade |
| `SIMMER_MIN_VOLUME` | `10000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.07` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `6` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this value |

## Edge Thesis

Prediction markets are often analyzed as if each contract stands alone. In practice, users trade them as separate stories, while many of them are mathematically or procedurally linked. That leaves pockets where the book is not coherent.

This skill treats the market set as a probability lattice and trades the repair of that lattice.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
