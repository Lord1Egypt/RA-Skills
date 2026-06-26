---
name: polymarket-ladder-f1-championship-trader
description: Trades distribution-sum violations in F1 championship winner markets on Polymarket. Driver winner probabilities form a distribution that must sum to ~100% — when the field is collectively overpriced or underpriced, individual driver markets are structurally mispriced.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Ladder F1 Championship Distribution Trader
  difficulty: advanced
---

# Ladder -- F1 Championship Distribution Trader

> **This is a template.**
> The default signal exploits distribution-sum violations in F1 championship winner markets. No external API required beyond simmer-sdk. The skill discovers F1 driver championship markets, groups them by championship, checks whether the implied probability distribution sums to ~100%, and trades the correction when it drifts.

## Strategy Overview

In a winner-takes-all market like "Who will be the 2026 F1 Drivers' Champion?", the individual driver probabilities **must** sum to approximately 100%. On Polymarket, each driver is listed as a separate binary market. Because each market has its own bid-ask spread, retail flow, and narrative momentum, the implied probabilities frequently drift apart:

- **Sum > 105%**: The field is collectively overpriced. Each driver's YES price is inflated relative to the fair share of 100%. We sell the most overpriced drivers (buy NO on the highest-probability ones).
- **Sum < 95%**: The field is collectively underpriced. Each driver's YES price is too low. We buy the most underpriced drivers (buy YES on the lowest-probability ones).

This is a **structural arbitrage on probability distributions**, not a directional bet on any single driver winning or losing.

## The Core Insight: Why Distribution Violations Exist

Three mechanisms create and sustain distribution-sum violations:

**1. Independent bid-ask spreads**
Each driver market has its own spread. When you sum 20 drivers' mid prices, the individual spreads compound. A 2-3 cent spread on each of 20 markets can push the total sum 10-15% above or below 100%.

**2. Narrative-driven retail flow**
When news breaks (e.g., Verstappen dominates a qualifying session), retail piles into that driver's YES market, pushing the entire field's sum above 100%. The other drivers' prices don't drop fast enough to compensate because there's no automated arbitrage mechanism across separate binary markets.

**3. Stale pricing on low-liquidity drivers**
The top 3-5 drivers have active order books. The remaining 15+ drivers may have stale prices that don't adjust when the favorites move, creating persistent sum violations.

## Signal Logic

### Step 1 -- Market Discovery

Keyword search across F1-specific terms plus a `get_markets(limit=200)` fallback. All candidates are filtered by a regex that matches F1/motorsport market questions.

### Step 2 -- Championship Grouping

Markets are parsed to extract `(championship_name, driver_name)` tuples using regex patterns that match:
- "Will Verstappen be the 2026 F1 Drivers' Champion?"
- "Will Gasly win the 2026 Formula 1 championship?"

Markets are grouped by championship name.

### Step 3 -- Distribution Sum Check

For each championship group, sum all driver probabilities. If `|sum - 1.0| < MIN_VIOLATION` (default 5%), the distribution is within tolerance and we skip the group.

### Step 4 -- Signal Direction

- **Overpriced field (sum > 105%)**: Sort drivers by probability descending. Buy NO on drivers above `NO_THRESHOLD` (most overpriced first).
- **Underpriced field (sum < 95%)**: Sort drivers by probability ascending. Buy YES on drivers below `YES_THRESHOLD` (most underpriced first).

### Step 5 -- Conviction-Based Sizing

For NO (overpriced field):
```
conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
violation_boost = min(1.5, 1.0 + violation_magnitude)
size = max(MIN_TRADE, conviction * violation_boost * MAX_POSITION)
```

For YES (underpriced field):
```
conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
violation_boost = min(1.5, 1.0 + violation_magnitude)
size = max(MIN_TRADE, conviction * violation_boost * MAX_POSITION)
```

The violation boost increases position size when the distribution-sum violation is larger (more edge).

### How Sizing Works

With defaults (YES_THRESHOLD=38%, NO_THRESHOLD=62%, MIN_TRADE=$5, MAX_POSITION=$40, violation=10%):

**Overpriced field (buy NO on high-p drivers):**

| Driver p | Conviction | Violation boost | Size |
|---|---|---|---|
| 62% (at threshold) | 0% | 1.10x | $5 (floor) |
| 70% | 21% | 1.10x | $9 |
| 80% | 47% | 1.10x | $21 |
| 90% | 74% | 1.10x | $33 |

**Underpriced field (buy YES on low-p drivers):**

| Driver p | Conviction | Violation boost | Size |
|---|---|---|---|
| 38% (at threshold) | 0% | 1.10x | $5 (floor) |
| 30% | 21% | 1.10x | $9 |
| 20% | 47% | 1.10x | $21 |
| 10% | 74% | 1.10x | $33 |

### Keywords Monitored

```
F1, Formula 1, champion, Drivers Champion, Grand Prix,
Verstappen, Hamilton, Norris, Leclerc, Piastri,
Russell, Gasly, Albon, Bottas
```

### Remix Signal Ideas

- **Cross-championship arbitrage**: Compare distribution-sum violations across multiple championships (F1, MotoGP, IndyCar) and prioritize the most violated distribution
- **Historical sum tracking**: Track the distribution sum over time and trade mean-reversion when the sum spikes or dips
- **News-driven violation detection**: Wire in an F1 news feed and trigger scans immediately after major race results or qualifying sessions, when retail flow is most likely to create violations
- **Team-pair arbitrage**: Within a team, the two drivers' probabilities should roughly reflect their relative performance -- trade when team-pair ratios diverge from season data
- **Volume-weighted conviction**: Weight conviction by each driver market's volume -- low-volume markets have staler prices and potentially more edge

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` -- nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter |
| `SIMMER_MAX_SPREAD` | `0.06` | Max bid-ask spread (6%) |
| `SIMMER_MIN_DAYS` | `7` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES when driver probability <= this in underpriced field |
| `SIMMER_NO_THRESHOLD` | `0.62` | Buy NO when driver probability >= this in overpriced field |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_MIN_VIOLATION` | `0.05` | Min distribution-sum violation to trigger trades (5%) |

## Edge Thesis

F1 driver championship winner probabilities on Polymarket systematically deviate from a 100% total because of three structural mechanisms:

1. **Retail trades drivers individually** -- users buy YES on their favorite driver without checking whether the field total already exceeds 100%. A wave of enthusiasm after a race result inflates the winner without deflating the rest.
2. **No cross-market consistency enforcement** -- unlike a traditional bookmaker who adjusts the entire field when one runner's odds move, Polymarket has no market maker enforcing that the sum of all driver probabilities stays at 100%. Each driver is a separate order book with independent liquidity.
3. **Driver entry and exit creates transient imbalances** -- when a new driver is added to the championship market (mid-season replacement, rookie promotion) or a driver is removed (retirement, disqualification), the existing prices do not instantly re-normalize. The sum drifts until enough traders notice and correct it.

These three forces guarantee recurring distribution-sum violations that revert as resolution approaches and the market must price a single winner at 100%.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
