---
name: polymarket-longshot-bias-trader
description: Exploits longshot bias — the most robust anomaly in betting and prediction market research. Systematically fades overpriced low-probability outcomes (buy NO when p ≤ 10%) and backs underpriced near-certainties (buy YES when p ≥ 88%). Domain-agnostic: the bias exists in every market category. Conviction scales with depth of mispricing and narrative salience.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Longshot Bias Trader
  difficulty: intermediate
---

# Longshot Bias Trader

> **This is a template.**
> The default signal is purely price-based — no external API required. The skill discovers liquid markets across all categories, identifies extreme probabilities where behavioral mispricing is strongest, and trades against the crowd.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Longshot bias is the single most replicated anomaly in betting market research. First documented by Griffith (1949) in horse racing, it has since been confirmed across sports betting, financial options (the volatility smile is its cousin), and prediction markets.

**The core finding:** Participants systematically overweight the excitement of low-probability outcomes and underweight the boring reliability of near-certainties.

- A market priced at **6%** is more likely to have a true probability of **2–3%** — retail bets the dream.
- A market priced at **91%** is more likely to have a true probability of **95–97%** — retail finds it too boring to back fully.

This creates two exploitable edges in opposite directions:

1. **Fade the longshot (buy NO when p is very low):** The crowd overprices rare events. Buying NO when p ≤ 10% gives you the opposite side of that overpriced bet.
2. **Back the near-certainty (buy YES when p is very high):** The crowd underprices likely outcomes. Buying YES when p ≥ 88% gives you the underpriced side.

These are not directional bets on events — they are **structural bets against a known behavioral bias** that regenerates in every market, every day.

## The Core Insight: Why Longshot Bias Exists

Three behavioral mechanisms drive the bias simultaneously:

**1. Probability distortion (Kahneman & Tversky)**
Humans do not perceive probabilities linearly. We treat 5% as "might happen" and 95% as "probably won't fail." This distorts prices in predictable ways: low probabilities are overweighted, high probabilities are underweighted.

**2. Narrative salience**
A 5% longshot has a compelling story. "Imagine if it happened." Retail pays a premium for the story. A 95% near-certainty is boring — retail won't pay full price for something "obviously going to happen anyway."

**3. Skewness preference**
Small chance of a large gain is psychologically attractive even at negative expected value. This is the same reason people buy lottery tickets. In prediction markets, the NO side of a longshot offers a small chance of a large gain in the *other direction* — but retail doesn't frame it that way.

## Signal Logic

### Default Signal: Conviction-Based Extreme Probability Fading

This skill uses **inverted thresholds** compared to standard prediction market traders:

| Standard trader | Longshot bias trader |
|---|---|
| Buy YES when p is low (you think it'll happen) | Buy NO when p is low (market overprices the longshot) |
| Buy NO when p is high (you think it won't happen) | Buy YES when p is high (market underprices the certainty) |

**Step 1 — Market discovery:**
Broad keyword sweep across all high-liquidity categories (politics, crypto, sports, macro, tech, geopolitics). Longshot bias is category-agnostic — it exists wherever retail trades.

**Step 2 — Signal gates:**
- Spread ≤ MAX_SPREAD (wide spreads eat the edge)
- Days to resolution ≥ MIN_DAYS (avoid near-resolution noise where convergence may have already started)

**Step 3 — Signal direction:**
- `p ≤ LONGSHOT_THRESHOLD` → buy **NO** (fade the overpriced longshot)
- `p ≥ CERTAINTY_THRESHOLD` → buy **YES** (back the underpriced near-certainty)
- Between thresholds → skip

**Step 4 — Conviction sizing:**

For NO (fading longshot):
```
conviction = (LONGSHOT_THRESHOLD - p) / LONGSHOT_THRESHOLD
```
At p=0%: conviction=1.0 → MAX_POSITION. At p=LONGSHOT_THRESHOLD: conviction=0.0 → MIN_TRADE floor.

For YES (backing near-certainty):
```
conviction = (p - CERTAINTY_THRESHOLD) / (1 - CERTAINTY_THRESHOLD)
```
At p=100%: conviction=1.0 → MAX_POSITION. At p=CERTAINTY_THRESHOLD: conviction=0.0 → MIN_TRADE floor.

**Step 5 — Quality multiplier (`_longshot_quality_mult`):**

Three factors adjust conviction up or down:

| Factor | What it captures | Range |
|---|---|---|
| Depth of mispricing | Deeper longshots / higher certainties are more mispriced | 1.00 → 1.25x |
| Narrative salience | Emotionally charged framing inflates longshot prices further | 1.00 → 1.15x |
| Resolution clarity | Objective criteria → cleaner edge; vague criteria → noise | 0.90 → 1.05x |

Combined and capped at 1.30x.

### How Sizing Works

With defaults (LONGSHOT_THRESHOLD=10%, CERTAINTY_THRESHOLD=88%, MIN_TRADE=$5, MAX_POSITION=$30):

**Fading longshots (buy NO):**

| Market price p | Conviction | Size |
|---|---|---|
| 10% (at threshold) | 0% | $5 (floor) |
| 7% | 30% | $9 |
| 4% | 60% | $18 |
| 1% | 90% | $27 |
| 0% | 100% | $30 |

**Backing near-certainties (buy YES):**

| Market price p | Conviction | Size |
|---|---|---|
| 88% (at threshold) | 0% | $5 (floor) |
| 92% | 33% | $10 |
| 96% | 67% | $20 |
| 99% | 92% | $28 |

### Keywords Monitored

```
president, election, congress, senate, federal reserve, rate cut, rate hike,
inflation, recession, gdp, unemployment,
bitcoin, ethereum, crypto, btc, eth,
championship, world cup, super bowl, nba finals, world series,
premier league, champions league,
ipo, acquisition, merger, bankruptcy, earnings,
agi, artificial intelligence, gpt, clinical trial, fda,
ceasefire, sanctions, invasion, treaty, nato
```

### Remix Signal Ideas

- **Calibration data from historical Polymarket markets**: If resolved markets show that markets priced at 5% resolved YES only 1.5% of the time, you have a precise expected-value edge to trade against — replace keyword thresholds with a calibration curve
- **Cross-category calibration**: The bias is stronger in some categories (sports, celebrity) than others (macro, crypto) — weight conviction by category-specific historical overpricing rates
- **Volume filter on longshots**: Very low-volume longshots may be mispriced for liquidity reasons rather than behavioral reasons — add a minimum volume gate specifically for sub-10% markets to separate behavioral edge from illiquidity risk
- **Resolution source quality**: Markets resolving via a single authoritative source (official election results, exchange close price) have cleaner edge than markets resolving via "admin discretion" — apply a resolution clarity multiplier to the conviction
- **Temporal decay toward resolution**: As a market approaches resolution, the bias should compress (less time for narrative to accumulate). Wire in a decay function: `mult *= max(0.7, days_to_resolution / 30)` to reduce size as markets near their end date

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
| `SIMMER_MAX_POSITION` | `30` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `10000` | Min market volume filter — higher bar to ensure genuine behavioral pricing, not illiquidity |
| `SIMMER_MAX_SPREAD` | `0.06` | Max bid-ask spread (6%) — tight to preserve statistical edge |
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution — avoid markets where convergence has already started |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_LONGSHOT_THRESHOLD` | `0.10` | Buy NO when market probability ≤ this value |
| `SIMMER_CERTAINTY_THRESHOLD` | `0.88` | Buy YES when market probability ≥ this value |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
