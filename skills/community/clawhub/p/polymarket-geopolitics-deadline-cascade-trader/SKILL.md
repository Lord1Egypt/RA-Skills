---
name: polymarket-geopolitics-deadline-cascade-trader
description: Trades temporal inconsistencies across geopolitical markets with different deadlines. When P(event by later date) < P(event by earlier date), the later-deadline market is underpriced — a mathematical tautology violation. Also detects diplomacy-vs-escalation inversions within the same conflict.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Geopolitics Deadline Cascade Trader
  difficulty: advanced
---

# Geopolitics Deadline Cascade Trader

> **This is a template.**
> The default signal detects temporal monotonicity violations and diplomacy-escalation inversions across geopolitical deadline markets — remix it with richer conflict ontologies, news feeds, or satellite-derived intelligence.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Geopolitical prediction markets frequently list the same conflict event across multiple deadlines: "Will Iran be struck by March 31?", "Will Iran be struck by December 31, 2026?", etc. By the laws of probability, the later-deadline market must always be at least as likely as the earlier one. When this relationship breaks, it is not a matter of opinion — the market is mathematically inconsistent.

This skill scans Polymarket for geopolitical markets, groups them by conflict theme and deadline, and identifies two classes of mispricing:

1. **Temporal monotonicity violations** — P(event by later date) < P(event by earlier date)
2. **Diplomacy-escalation inversions** — within the same conflict, both diplomatic and escalation events priced above 50%, which is logically strained

## Edge Thesis

Individual geopolitical markets are priced by participants reacting to headlines. Few traders systematically compare related markets across deadlines. This creates pockets where the probability surface is not monotone — where buying the later deadline or selling the earlier one is structurally justified regardless of one's view on the conflict itself.

The edge is not in predicting wars. The edge is in enforcing calendar math.

## Signal Logic

### 1. Temporal Monotonicity Check

1. Discover geopolitical markets using conflict-related keywords (Iran, Israel, Gaza, Lebanon, nuclear, sanctions, tariff, ceasefire, war, troops, etc.)
2. Parse each question to extract `(conflict_theme, deadline_date, event_type)`
3. Group by `conflict_theme`
4. Within each group, sort by deadline and check that probabilities are non-decreasing
5. When a violation exceeds `MIN_VIOLATION`, generate:
   - **YES** on the underpriced later-deadline market
   - **NO** on the overpriced earlier-deadline market

### 2. Diplomacy-Escalation Inversion Check

Within the same conflict theme, if both an escalation event (war, strike, attack) and a diplomatic event (meeting, deal, sanctions) are priced above 50%, one should constrain the other. The skill flags both as overpriced and generates **NO** signals.

### 3. Conviction-Based Sizing

All trades use the conviction formula from the standard framework:

- **YES**: `conviction = (YES_THRESHOLD - p) / YES_THRESHOLD`, boosted by violation magnitude
- **NO**: `conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)`, boosted by violation magnitude
- **Size**: `max(MIN_TRADE, conviction * MAX_POSITION)`

Trades are only placed when both the inconsistency exists AND the single-market threshold is satisfied.

## Remix Ideas

- Add news sentiment scoring to weight violations that align with recent headlines
- Incorporate satellite imagery APIs for troop movement confirmation
- Extend conflict themes with country-pair graphs (e.g., US-China, Russia-Ukraine)
- Add cross-venue arbitrage against Kalshi or Metaculus geopolitical questions
- Weight violations by market liquidity depth, not just volume

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
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade at full conviction |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade |
| `SIMMER_MIN_VOLUME` | `10000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.07` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `6` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this value |
| `SIMMER_MIN_VIOLATION` | `0.04` | Min probability violation to trigger a signal |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
