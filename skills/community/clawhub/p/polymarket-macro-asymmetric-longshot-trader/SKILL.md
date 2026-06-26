---
name: polymarket-macro-asymmetric-longshot-trader
description: Systematically finds markets with huge asymmetric payoff -- markets priced at 2-10% where cross-category macro analysis suggests the REAL probability is 15-30%. Uses related markets in other categories (crypto ladders, health escalation, geopolitical heating) to identify which longshots have hidden support. Small bets with 5-20x potential payoff.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Macro Asymmetric Longshot Trader
  difficulty: advanced
---

# Macro Asymmetric Longshot Trader

> **This is a template.**
> The default signal scans for longshot markets (2-10% probability) and scores their macro support using cross-category related markets -- remix it with news sentiment analysis, social media signals, or expert forecaster aggregation.
> The skill handles all the plumbing (market discovery, category classification, macro scoring, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Most prediction market participants avoid longshots entirely ("5% means it won't happen") or pick them randomly based on gut feeling ("wouldn't it be cool if..."). Neither approach is systematic.

This trader scans ALL markets for longshots priced between 2% and 10%, then uses CROSS-CATEGORY macro signals to identify which longshots are systematically underpriced. A $5 bet at 5% returns $100 if right. The edge isn't in predicting any single longshot correctly -- it's in finding the ones where the market is pricing 5% but the macro context suggests 15-30%.

## Edge

Cross-category macro support scoring separates randomly cheap markets from systematically underpriced ones:

1. **Crypto ladder effect** -- If "BTC above $60k" is at 80% and "BTC above $65k" is at 50%, then "BTC above $70k" at 6% is likely underpriced. The probability ladder should be smoother than what retail prices -- they dramatically underweight tail scenarios when the body of the distribution is already moving.

2. **Health escalation cascades** -- If "measles > 500 cases" is at 85% and "measles > 1000" is at 60%, then "measles > 2000" at 5% is underpriced. Epidemics have exponential growth dynamics that make escalation more likely than linear extrapolation suggests.

3. **Geopolitical heating** -- If multiple escalation markets (sanctions, troop movements, diplomatic breakdowns) are above 40%, then extreme outcome longshots (war, invasion, regime change) carry more probability than standalone analysis suggests. Geopolitical events cluster.

4. **Economic contagion** -- If recession indicators, rate expectations, and trade war markets are all heating up, extreme economic longshots (sovereign default, currency crisis) have hidden support.

5. **Asymmetric payoff** -- Even with a 20% hit rate on longshots that pay 10x, expected value is 2x. The strategy is profitable in aggregate, not on any single bet.

## Signal Logic

1. Discover ALL active markets via keyword search + `get_markets(limit=200)` fallback
2. Filter for longshots: p between 0.02 and `LONGSHOT_CEILING` (default 0.10)
3. Classify each longshot into a category (crypto, health, geopolitics, economic, political)
4. Compute `macro_support_score` (0.0 to 1.0) by checking related markets:
   - **Crypto**: Check if lower threshold markets are likely (ladder analysis)
   - **Health**: Check if lower case-count markets are likely (escalation ladder)
   - **Geopolitics**: Check if related escalation markets are heating up
   - **Economic**: Check if related macro indicators are heating up
   - **Political**: Check if related political markets show instability
5. Only trade longshots with `macro_support >= MIN_SUPPORT` (default 0.40)
6. Size = `max(MIN_TRADE, conviction * LONGSHOT_SIZE_CAP * MAX_POSITION)`
7. Sort by support score descending -- best-supported longshots first

### How Macro Support Scoring Works

**Crypto Ladder Example:**

| Market | P | Role |
|---|---|---|
| BTC above $60k | 80% | Lower threshold (support) |
| BTC above $65k | 50% | Lower threshold (support) |
| BTC above $70k | 6% | LONGSHOT -- avg lower = 65%, score = 0.78 |
| BTC above $80k | 3% | LONGSHOT -- avg lower = 45%, score = 0.54 |

**Health Escalation Example:**

| Market | P | Role |
|---|---|---|
| Measles > 500 | 85% | Lower threshold (support) |
| Measles > 1000 | 60% | Lower threshold (support) |
| Measles > 2000 | 5% | LONGSHOT -- avg lower = 72%, score = 0.94 |

**Geopolitics Heating Example:**

| Market | P | Role |
|---|---|---|
| New sanctions on X? | 65% | Escalation signal |
| Troops deployed to Y? | 45% | Escalation signal |
| Full-scale war in Z? | 4% | LONGSHOT -- 2 signals avg 55%, score = 0.66 |

### How Sizing Works

Position size is capped at `LONGSHOT_SIZE_CAP` (30%) of `MAX_POSITION` because longshots are inherently risky. With defaults (MIN_TRADE=$5, MAX_POSITION=$40, cap=30% -> max=$12):

| p | Support | Conviction | Size | Payoff if right |
|---|---|---|---|---|
| 10% (ceiling) | 0.80 | 0% | $5 (floor) | $50 |
| 8% | 0.80 | 16% | $5 (floor) | $63 |
| 5% | 0.80 | 40% | $5 (floor) | $100 |
| 3% | 0.90 | 63% | $8 | $267 |
| 2% | 1.00 | 80% | $10 | $500 |

### Keywords Monitored

```
bitcoin above, btc above, ethereum above, eth above,
solana above, sol above, xrp above, crypto price,
measles, bird flu, avian flu, pandemic, outbreak,
war, invasion, escalation, sanctions, nuclear,
tariff, trade war, embargo, coup, resign,
impeach, default, recession, rate cut, rate hike
```

### Remix Signal Ideas

- **News sentiment NLP**: Score longshot markets against recent news headlines -- a sudden spike in news mentions of a topic dramatically increases the probability of related longshots
- **Expert forecaster aggregation**: Cross-reference Polymarket longshot prices with Metaculus, Good Judgment Open, or Manifold Markets -- if experts price the event at 15% but Polymarket prices it at 5%, strong support signal
- **Historical base rates**: For recurring events (annual measles counts, quarterly GDP, monthly employment), check the historical frequency of extreme outcomes -- longshots on events that happen 15% of the time historically but are priced at 5% are systematically underpriced
- **Social media spike detection**: Track Twitter/Reddit mention velocity for longshot topics -- viral attention often precedes probability repricing by 12-48 hours

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
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (10% -- wider for thin longshot markets) |
| `SIMMER_MIN_DAYS` | `1` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Standard YES threshold (used for non-longshot fallback) |
| `SIMMER_NO_THRESHOLD` | `0.62` | Standard NO threshold (used for non-longshot fallback) |
| `SIMMER_LONGSHOT_CEILING` | `0.10` | Max probability to qualify as a longshot (10%) |
| `SIMMER_MIN_SUPPORT` | `0.40` | Min macro support score to trade a longshot |
| `SIMMER_LONGSHOT_SIZE_CAP` | `0.30` | Max fraction of MAX_POSITION for longshot sizing (30%) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
