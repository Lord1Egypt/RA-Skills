---
name: polymarket-geopolitics-sentiment-reversal-trader
description: Trades mean reversion on geopolitical markets pushed to probability extremes by breaking news. Markets at >92% or <8% with long time horizons systematically over-react and revert. Combines overreaction bias detection with staleness factor (days-to-resolution) for conviction sizing.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Geopolitics Sentiment Reversal Trader
  difficulty: advanced
---

# Geopolitics Sentiment Reversal Trader

> **This is a template.**
> The default signal is purely price-based with a staleness (days-to-resolution) multiplier -- no external API required. The skill discovers geopolitical markets at probability extremes, identifies likely overreactions using time-horizon analysis, and trades mean reversion.
> The skill handles all the plumbing (market discovery, geopolitics filtering, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Geopolitical prediction markets are uniquely susceptible to overreaction. When breaking news hits -- a military strike, a sanctions announcement, a ceasefire collapse -- retail traders rush to reprice markets. The result is a predictable pattern: markets overshoot to probability extremes (>92% or <8%) and then revert 30-50% of the move within 24-48 hours.

This skill systematically identifies and trades these overreactions by combining two signals:

1. **Probability extremes:** Markets pushed beyond the reversal zones (>92% or <8%) where overreaction is statistically most likely.
2. **Staleness factor:** Markets with long time horizons (30-180 days) at extreme prices are far more likely to be overreactions than markets with 2-3 days to resolution where the extreme price may reflect genuine resolution information.

## Edge Thesis: Behavioral Finance Overreaction Bias

The overreaction hypothesis (De Bondt & Thaler, 1985) documents that markets systematically overshoot in response to dramatic news and subsequently revert. In geopolitical prediction markets, this bias is amplified by three mechanisms:

**1. Availability heuristic under fear**
Breaking geopolitical news (airstrikes, troop movements) activates fear responses. Retail traders anchor to the most dramatic possible outcome and price accordingly. A single airstrike pushes "Will there be a full-scale invasion?" from 40% to 93% -- even though the base rate for escalation from single strikes to full invasion is historically low.

**2. Asymmetric attention**
The news that pushes a market to 95% gets wall-to-wall coverage. The slow de-escalation that brings it back to 70% happens quietly over days. Retail attention is front-loaded on the shock, creating a predictable overshoot-and-decay pattern.

**3. Time-horizon mispricing**
A market at 92% with 180 days to resolve embeds enormous uncertainty that retail ignores in the heat of the moment. The staleness factor captures this: longer horizons mean more room for reversion, more intervening events, and more time for the initial overreaction to wash out.

## Signal Logic

### Step 1 -- Market Discovery

Keyword sweep across geopolitical topics: war, ceasefire, military, strike, Iran, Israel, Gaza, Lebanon, sanctions, nuclear, troops, conflict, attack, bomb, invasion, Hezbollah, Hamas.

A regex filter then confirms the market question is genuinely geopolitical (avoids false positives from keywords appearing in non-geopolitical contexts).

### Step 2 -- Signal Gates

- Spread <= MAX_SPREAD (wide spreads eat the reversal edge)
- Days to resolution >= MIN_DAYS (standard minimum)
- Days to resolution >= MIN_DAYS_FOR_REVERSAL (need enough runway for reversion)

### Step 3 -- Signal Direction

| Condition | Trade | Rationale |
|---|---|---|
| p >= REVERSAL_ZONE_HIGH (92%) and p >= NO_THRESHOLD | Buy NO | Market is "too certain" -- expect reversion DOWN |
| p <= REVERSAL_ZONE_LOW (8%) and p <= YES_THRESHOLD | Buy YES | Market is "too pessimistic" -- expect reversion UP |
| Between zones | Skip | Not at an overreaction extreme |

### Step 4 -- Staleness Factor

The staleness factor is the key innovation. It scales from 0.0 to 1.0 based on days to resolution:

| Days to resolution | Staleness factor | Interpretation |
|---|---|---|
| 7 (minimum) | 0.0 | Near-term -- extreme price may be correct |
| 30 | 0.28 | Some room for reversion |
| 60 | 0.64 | Substantial overreaction likely |
| 90+ | 1.00 | Maximum -- extreme is almost certainly an overreaction |

Formula: `staleness = min(1.0, (days - MIN_DAYS_FOR_REVERSAL) / (90 - MIN_DAYS_FOR_REVERSAL))`

### Step 5 -- Conviction Sizing

For NO (high extreme reversion):
```
raw_conviction = (p - REVERSAL_ZONE_HIGH) / (1 - REVERSAL_ZONE_HIGH)
conviction = staleness * raw_conviction
size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
```

For YES (low extreme reversion):
```
raw_conviction = (REVERSAL_ZONE_LOW - p) / REVERSAL_ZONE_LOW
conviction = staleness * raw_conviction
size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
```

### How Sizing Works

With defaults (REVERSAL_ZONE_HIGH=92%, REVERSAL_ZONE_LOW=8%, MIN_TRADE=$5, MAX_POSITION=$40):

**High extreme reversion (buy NO):**

| Market price p | Days left | Staleness | Raw conviction | Final conviction | Size |
|---|---|---|---|---|---|
| 93% | 14d | 0.08 | 12.5% | 1.0% | $5 (floor) |
| 95% | 30d | 0.28 | 37.5% | 10.5% | $5 (floor) |
| 95% | 90d | 1.00 | 37.5% | 37.5% | $15 |
| 98% | 60d | 0.64 | 75.0% | 48.0% | $19 |
| 98% | 120d | 1.00 | 75.0% | 75.0% | $30 |

**Low extreme reversion (buy YES):**

| Market price p | Days left | Staleness | Raw conviction | Final conviction | Size |
|---|---|---|---|---|---|
| 7% | 14d | 0.08 | 12.5% | 1.0% | $5 (floor) |
| 5% | 30d | 0.28 | 37.5% | 10.5% | $5 (floor) |
| 3% | 90d | 1.00 | 62.5% | 62.5% | $25 |
| 1% | 120d | 1.00 | 87.5% | 87.5% | $35 |

### Remix Ideas

- **GDELT event velocity:** Wire in GDELT's real-time event stream to measure the *rate* of new events. A single spike followed by silence is the classic overreaction pattern. Sustained event velocity means the market move may be justified -- reduce conviction.
- **Twitter/X sentiment decay:** Track sentiment volume on geopolitical hashtags. If sentiment peaked 12-24h ago and is declining, the overreaction is already unwinding -- increase conviction for the reversal trade.
- **Historical reversion rate by event type:** Airstrikes revert faster than sanctions announcements. Build a lookup table of event-type-specific reversion rates to weight conviction.
- **Cross-market correlation:** If multiple geopolitical markets spike simultaneously on the same news event, the overreaction is likely correlated. Trade the most extreme one and skip the rest to avoid correlated risk.
- **Volatility regime detection:** During periods of sustained geopolitical escalation (war phases), extreme prices may be correct. Add a regime filter that reduces conviction when multiple markets have been at extremes for >7 days (sustained crisis vs. flash overreaction).

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
| `SIMMER_MIN_VOLUME` | `15000` | Min market volume filter |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread (8%) |
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution (standard gate) |
| `SIMMER_MAX_POSITIONS` | `6` | Max concurrent open positions |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_YES_THRESHOLD` | `0.38` | Standard YES gate -- only buy YES below this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Standard NO gate -- only buy NO above this |
| `SIMMER_REVERSAL_ZONE_HIGH` | `0.92` | Above this probability, market is in overreaction zone (high) |
| `SIMMER_REVERSAL_ZONE_LOW` | `0.08` | Below this probability, market is in overreaction zone (low) |
| `SIMMER_MIN_DAYS_REVERSAL` | `7` | Min days to resolution for reversal trades (need runway for reversion) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
