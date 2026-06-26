---
name: polymarket-24h-geopolitics-cluster-trader
description: Trades logical inconsistencies in geopolitical event clusters on Polymarket. Geopolitical markets form clusters where probabilities must satisfy constraints — strike-count markets are cumulative (P(7) <= P(6)), daily military action across regions should correlate, and prerequisite events constrain downstream markets. When these constraints are violated, the mispriced market reverts. This skill detects violations and trades the correction, sizing by conviction.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: 24h Geopolitics Cluster Trader
  difficulty: advanced
---

# 24h Geopolitics Cluster Trader

> **This is a template.**
> The default signal is geopolitical cluster consistency checking — remix it with additional constraint types, news sentiment, or satellite data feeds.
> The skill handles all the plumbing (market discovery, cluster grouping, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists many geopolitical markets that form logical clusters:

- **Strike-count markets**: "Will Israel strike 5 countries?", "...6 countries?", "...7 countries?"
- **Daily military action**: "Will Israel take military action in Gaza on March 21?", "...in Lebanon on March 20?"
- **Bilateral escalation**: "Will Iran conduct military action against Israel?"
- **Ceasefire markets**: "Will there be a ceasefire in Gaza?"

These markets are logically constrained. Striking 7 countries requires striking 6 first, so P(7) <= P(6) always. Escalation in one region affects others. When retail trades these markets in isolation, the constraints break — and that is the edge.

## The Edge: Logical Consistency Arbitrage

### Three Violation Types

1. **Monotonicity violations** (strike-count markets):
   - P(strike 7) must be <= P(strike 6) <= P(strike 5)
   - If P(strike 7) = 8% but P(strike 6) = 5%, the 7-market is overpriced or the 6-market is underpriced

2. **Correlation violations** (daily military action):
   - If Israel has 100% probability of action in Gaza on a given date, correlated regions (Lebanon, Syria) should reflect heightened risk
   - A very low probability in a correlated region on the same date may be underpriced

3. **Prerequisite chain violations**:
   - If P(Iran military action against Israel) = 8%, then P(Israel strikes 6+ countries) — which likely requires Iranian theater escalation — should not be much higher
   - The downstream event cannot greatly exceed its prerequisite

### Example

| Market | Probability |
|--------|-------------|
| Israel strike 5 countries | 20% |
| Israel strike 6 countries | 15.9% |
| Israel strike 7 countries | 18% |

Violation: P(strike 7) = 18% > P(strike 6) = 15.9%. The 7-market is overpriced. Trade: sell NO on the 7-market (or buy YES on the 6-market).

## Why This Works

1. **Retail trades in silos** — users view each market independently without cross-referencing logically related markets
2. **Logical constraints are structural** — cumulative events, prerequisite chains, and correlation are mathematical facts, not opinions
3. **Resolution forces convergence** — as resolution approaches, the market must price consistently or create guaranteed arbitrage
4. **Low-liquidity geopolitical markets** — these niche markets have less market-maker coverage, so mispricings persist longer

## Signal Logic

1. Discover geopolitical markets via keyword search (Israel, military, strike, Iran, Gaza, Lebanon, war, ceasefire)
2. Parse each question: extract event type, region, actor, threshold, date
3. Group into clusters (strike-count, daily-action, bilateral, ceasefire)
4. Check consistency constraints:
   - Strike counts: monotonically decreasing probabilities
   - Daily action: cross-region correlation on same date
   - Prerequisites: downstream events bounded by upstream probability
5. Rank violations by magnitude
6. Trade only opportunities that pass threshold gates (`YES_THRESHOLD` / `NO_THRESHOLD`)
7. Size by conviction (violation magnitude + threshold distance), not flat amount

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
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-day) |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_MIN_VIOLATION` | `0.04` | Min cluster consistency violation to trigger a trade |

## Edge Thesis

Geopolitical events are not independent coin flips. They form causal chains: escalation in one theater raises risk in adjacent theaters; striking N countries is a prerequisite for striking N+1. Prediction markets price each event individually, but the joint probability distribution must be internally consistent.

When it is not, the inconsistency is a free edge. This skill systematically detects and trades these logical violations, acting as an automated consistency enforcer for geopolitical prediction markets.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
