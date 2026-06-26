---
name: polymarket-btc-weekend-volatility-trader
description: Trades BTC weekend price threshold markets on Polymarket by exploiting the systematic gap between first-passage probability ("will BTC touch 150k at ANY POINT this weekend?") and terminal probability ("will BTC close above 150k?") — a structural mispricing that replenishes every weekend. Conviction scaled by entry timing window and BTC halving cycle volatility regime.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: BTC Weekend Volatility Trader
  difficulty: advanced
---

# BTC Weekend Volatility Trader

> **This is a template.**
> The default signal is keyword-based BTC threshold market discovery combined with conviction-based sizing and `btc_weekend_bias()` — three structural edges, no external API required.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Every weekend, Polymarket lists markets asking: *"Will Bitcoin trade above 150,000 USDT at any time between Saturday 00:00 UTC and Sunday 23:59 UTC?"*

Retail prices this as a terminal probability question — *will BTC be above 150k at market close?* The question is asking for something fundamentally different: a **first-passage probability** — *will BTC touch 150k at any single moment across a full 48-hour window?*

For a threshold level close to the current price, the first-passage probability is approximately **twice** the terminal probability. For far-OTM levels, the gap narrows but remains positive. Retail has no idea this distinction exists. The mispricing replenishes every single weekend.

Three structural edges compound without any API:

1. **First-passage vs terminal probability correction** — "Any time above X" is not "close above X." Given BTC's 70%+ annualized vol and fat-tail distribution (kurtosis ≈ 5–8 vs Gaussian 3), touch probability is systematically higher than what Polymarket prices.

2. **Entry timing window** — The edge is sharpest on Thursday–Friday morning when vol model estimates are freshest and weekend positional flows haven't yet crowded the market. By Sunday, the path is largely revealed and risk premium dominates.

3. **BTC halving cycle** — Weekend gap volatility is highest in the bull expansion phase (days 181–540 post-halving) when realized vol runs 70–90% annualized. Bear phase vol compression (30–45%) makes far-threshold markets chronically overpriced.

## The Core Insight: First-Passage ≠ Terminal Probability

This is the sharpest single edge in the entire skill. Here is the math:

For a random walk with annualized volatility σ over a time window T (in years):

```
σ_window = σ × √T

For BTC (σ ≈ 70%) over a 48-hour weekend window:
  T = 2/365 ≈ 0.00548 years
  σ_weekend ≈ 70% × √0.00548 ≈ 4.1%

A threshold 8% above current price:
  d = 8% / 4.1% ≈ 1.95 standard deviations

  Terminal P(BTC > threshold at end) ≈ Φ(-1.95) ≈ 2.6%
  Touch P  (BTC touches at any time) ≈ 2 × Φ(-1.95) ≈ 5.2%
```

The market prices **2.6%**. The correct answer is **5.2%**. Retail consistently prices the terminal probability when the question resolves on the touch.

Add BTC's empirical fat tails (extreme moves happen 3–5× more often than a Gaussian model predicts) and the true touch probability is even higher — potentially 7–10% for this level.

The edge is largest for levels 5–15% above current price — close enough to be reachable but far enough that retail dismisses them. Deep OTM levels (>20% away) narrow the gap; levels already nearly breached have the least edge as the path becomes predictable.

## Signal Logic

### Default Signal: Conviction-Based Sizing with BTC Weekend Bias

1. Discover active BTC price threshold markets across all levels (100k–200k+)
2. Gate: must be a genuine BTC price threshold market with a weekend/time window
3. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
4. Apply `btc_weekend_bias()` — semantic correction × entry timing × halving cycle
5. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION

### BTC Weekend Bias (built-in, no API required)

**Factor 1 — Semantic Resolution Type (first-passage correction)**

| Question semantics | Multiplier | What's actually being priced |
|---|---|---|
| "any time", "at any point", "at least once" | **1.25x** | First-passage: ≈2× terminal P; retail prices as terminal |
| "strictly above", "above", "trade above" | **1.20x** | Likely first-passage; BTC fat tails on top |
| Binance BTCUSDT named as primary source | **+0.05x** | Single clean feed reduces oracle risk; less interpretation uncertainty |
| "close above", "closing price", "at close" | **1.00x** | Terminal probability; standard pricing; less structural edge |

**Factor 2 — Entry Timing Window**

| Day / time (UTC) | Multiplier | Why |
|---|---|---|
| Thursday (any time) | **1.20x** | Optimal: 2–3 days to weekend, vol fresh, no positional crowding |
| Friday before 16:00 UTC | **1.15x** | Good: pre-market, US equity session active |
| Friday after 16:00 UTC | **1.10x** | Crypto weekend has opened; Asian session beginning |
| Saturday before noon UTC | **0.95x** | Path partially revealed; some touch edge remains |
| Saturday after noon UTC | **0.85x** | Well into window; realized price action dominates |
| Sunday | **0.75x** | Near resolution; risk premium dominates over structural edge |
| Monday–Wednesday | **1.00x** | Next weekend too far; vol estimate imprecise |

**Factor 3 — BTC Halving Cycle (volatility regime)**

| Phase | Days since halving | Multiplier | Typical realized vol |
|---|---|---|---|
| Bull expansion | 181–540 | **1.15x** | 70–90% annualized — weekend moves most dramatic |
| Post-halving momentum | 0–180 | **1.10x** | Vol picking up through the cycle |
| Distribution / topping | 541–900 | **1.00x** | Vol declining from peak |
| Bear / accumulation | 901+ | **0.85x** | 30–45% annualized — far-threshold markets overpriced |

### Combined Examples

Today (March 18, 2026): **Thursday** + **bull-expansion (day 333 since halving)**

| Market | Semantic | Timing | Cycle | Final bias |
|---|---|---|---|---|
| "BTC above 150k at any point this weekend?" — Thursday, Binance source | 1.25+0.05 = 1.30x | 1.20x | 1.15x | **1.40x cap** |
| "Will BTCUSDT trade above 140k this weekend?" — Thursday | 1.20x | 1.20x | 1.15x | **1.40x cap** |
| "Will BTC close above 160k by Sunday?" — Thursday | 1.00x | 1.20x | 1.15x | **1.38x** |
| Same market entered Saturday afternoon | 1.20x | 0.85x | 1.15x | **1.17x** |
| Same market entered Sunday | 1.20x | 0.75x | 1.15x | **1.03x** |
| Bear market (day 950) + Sunday + "close above" | 1.00x | 0.75x | 0.85x | **0.64x → MIN_TRADE** |

### How Sizing Works at Different Probability Levels

With defaults (YES_THRESHOLD=0.40, MIN_TRADE=$5, MAX_POSITION=$25, bull Thursday bias ≈1.40x):

| Market price p | Conviction | Biased conviction | Size |
|---|---|---|---|
| 40% (at threshold) | 0% | 0% | $5 (floor) |
| 30% | 25% | 35% | $9 |
| 20% | 50% | 70% | $18 |
| 10% | 75% | 100% capped | $25 |
| 5% | 87.5% | 100% capped | $25 |

Deep-OTM threshold markets (5–10% probability) get maximum size on Thursday — this is where the first-passage correction is most exploitable and where retail is most wrong.

### Keywords Monitored

```
bitcoin weekend, BTC weekend, BTCUSDT weekend, bitcoin this weekend,
BTC this weekend, bitcoin above, btc above, BTCUSDT above,
bitcoin reach, btc reach, bitcoin hit, btc hit, trade above,
at any point, any time this weekend, strictly above,
bitcoin 100k, bitcoin 110k, bitcoin 120k, bitcoin 130k,
bitcoin 140k, bitcoin 150k, bitcoin 160k, bitcoin 170k,
bitcoin 180k, bitcoin 200k, btc 100k, btc 150k, btc 200k,
100000 usdt, 110000 usdt, 120000 usdt, 130000 usdt, 140000 usdt,
150000 usdt, 160000 usdt, 170000 usdt, 200000 usdt,
Binance BTCUSDT, btcusdt above, last traded price
```

### Remix Signal Ideas

- **Binance real-time BTCUSDT price**: Wire the current spot price into `compute_signal` — compute distance-to-threshold in % and apply the barrier option first-passage formula directly; gives exact touch probability vs Polymarket's naive p; the precision arbitrage is cleanest when you have both numbers
- **Realized volatility from Binance OHLC**: Pull 30-day weekend-specific realized vol (Sat/Sun candles only) — weekend vol is often lower than weekday vol but with more extreme tail events; calibrate the σ_weekend to weekend-only data for a more precise touch probability model
- **Funding rate & perpetual basis**: Positive funding means longs are paying shorts — crowded long positioning around a threshold level dampens the surprise upside; negative funding means aggressive shorting, which can fuel squeeze moves upward through resistance levels
- **Multi-threshold internal consistency**: If markets for 130k, 140k, 150k, and 160k all resolve over the same weekend, their probabilities must be monotonically decreasing. When P(touch 150k) > P(touch 140k) in Polymarket, one of them is wrong — buy the underpriced one, sell the overpriced one

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` — nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `25` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread (8%) |
| `SIMMER_MIN_DAYS` | `1` | Min days until resolution — weekend markets are short-horizon by design |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions — can hold multiple threshold levels simultaneously |
| `SIMMER_YES_THRESHOLD` | `0.40` | Buy YES if market price ≤ this value — wider than default to capture OTM thresholds |
| `SIMMER_NO_THRESHOLD` | `0.65` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
