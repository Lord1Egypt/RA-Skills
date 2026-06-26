---
name: polymarket-equity-markets-trader
description: Trades Polymarket prediction markets on stock index milestones, major IPOs, earnings surprises, analyst upgrades, and company-specific financial events. Exploits two structural edges — earnings base rate mispricing (S&P companies beat consensus ~73–75% of the time; retail prices it as a coin flip) and macro calendar timing lag (futures market reprices CPI/FOMC/NFP 20–60 min before Polymarket does).
metadata:
  author: snetripp
  version: "1.0"
  displayName: Equity Markets & IPO Trader
  difficulty: advanced
---

# Equity Markets & IPO Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with conviction-based sizing and `equity_bias()` — two structural edges that work without any external API.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Equity prediction markets are unique: they run alongside the deepest, most quantified financial markets in the world. The edge is not in predicting markets better than Wall Street — it is in the **lag** between professional data (earnings base rates, options implied volatility, futures moves) and what Polymarket retail knows. Two structural edges compound cleanly:

1. **Earnings base rate correction** — The most underknown stat in equity markets: S&P 500 companies beat analyst consensus EPS estimates approximately 73–75% of the time, sustained across multiple economic cycles. Large-cap tech (NVDA, AAPL, MSFT, META, GOOG, AMZN) beats ~80–85%. Retail prices earnings beat markets as roughly 50–50. That 20–30 percentage point gap is structural edge that replenishes every earnings season.

2. **Macro calendar timing lag** — S&P 500 futures trade 24/7. When CPI prints, payrolls drop, or FOMC speaks, futures reprice instantly. Polymarket index threshold markets take 20–60 minutes to catch up, especially during pre-market hours. Quarter-start months (Jan, Apr, Jul, Oct) have maximum macro catalyst density — GDP advance estimate, full earnings flood, FOMC decision, and NFP all land within weeks of each other.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Equity Bias

1. Discover active equity and financial markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `equity_bias()` — market type correction × earnings calendar timing
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Equity Bias (built-in, no API required)

**Factor 1 — Market Type / Earnings Base Rate**

| Market type | Multiplier | The structural reality |
|---|---|---|
| Large-cap tech earnings (NVDA, AAPL, MSFT, META, GOOG, AMZN, TSLA) | **1.25x** | ~80–85% beat rate sustained 2020–2024; retail prices as 50–60%; Nvidia beat consensus 7 consecutive quarters |
| General S&P 500 earnings beat | **1.15x** | ~73–75% historical beat rate across multiple cycles; retail treats as coin flip; every "will X beat earnings?" is a structural YES lean |
| Index level milestone (S&P 500, Nasdaq, Dow reaching X) | **1.15x** | Futures market is a 24-hour reference; Polymarket lags macro catalysts 20–60 min; pre-market hours especially exploitable |
| Dividend / buyback / stock split | **0.90x** | Some insider buying signal but corporate decision timing is genuinely uncertain |
| IPO by date / IPO valuation milestone | **0.85x** | Window-driven; S-1 filing to pricing gap is highly variable; banker incentives dominant |
| Market crash / correction / bear market by date | **0.75x** | Most reliably overpriced category; crashes are vivid but rare in any specific window; VIX-spike retail anchors to worst case when mean reversion is likelier |
| Short squeeze / meme stock milestone | **0.65x** | Pure social coordination; requires specific short float data, borrow rate spikes, coordinated buying — none predictable from question text |

**The Crash Overpricing Rule** — "Will the S&P fall 20% by [date]?" is almost always overpriced on Polymarket. Retail's fear-anchoring after every VIX spike causes these markets to trade at 15–30% when the actual base rate for a 20%+ drawdown in any specific 3-month window is far lower. The vivid availability of 2008, 2020, and 2022 makes retail systematically pessimistic on specific-window crash markets. Dampen every crash/bear market question to 0.75x regardless of current probability.

**The Beat Rate Rule** — Analyst estimates are deliberately set to be beatable. Companies guide conservatively; analysts shade their models to match guidance; management sandbagging is a documented, multi-decade practice. The 73–75% aggregate beat rate is not a fluke — it is structural. Every "will X beat earnings?" market that prices below 50% is almost certainly mispriced unless the company has a specific documented miss history (e.g., retail, biotech pre-approval).

**Factor 2 — Earnings Calendar Timing**

| Condition | Multiplier | Why |
|---|---|---|
| Earnings-type question + peak season (Jan, Feb, Apr, May, Jul, Aug, Oct, Nov) | **1.20x** | Maximum signal density: fresh analyst estimates, current management guidance, live options implied volatility |
| Earnings-type question + off-season (Mar, Jun, Sep, Dec) | **0.85x** | Sparse pre-announcements; stale estimates; options vol compressed; base rate edge noisier |
| Index/macro question + quarter-start month (Jan, Apr, Jul, Oct) | **1.10x** | GDP advance estimate + full earnings flood + FOMC + NFP all land; maximum macro catalyst density |

### Combined Examples

| Market | Type mult | Calendar mult | Final bias |
|---|---|---|---|
| "Will Nvidia beat Q3 earnings?" — October | 1.25x | 1.20x (peak season) | **1.40x cap** |
| "Will S&P 500 reach 6,000 by year end?" — January | 1.15x | 1.10x (quarter-start) | **1.27x** |
| "Will Apple beat Q1 earnings?" — March | 1.25x | 0.85x (off-season) | **1.06x** |
| "Will there be a market crash by December?" | 0.75x | 1.0x | **0.75x** — always skeptical |
| "GameStop short squeeze to $100?" | 0.65x | 1.0x | **0.65x** — near floor |
| "Will Amazon IPO a subsidiary this year?" | 0.85x | 1.0x | **0.85x** |

### Keywords Monitored

```
S&P 500, Dow Jones, Nasdaq, stock market, bull market, bear market,
market crash, correction, IPO, earnings, revenue miss, beat,
Berkshire, Warren Buffett, Apple earnings, Tesla earnings,
Nvidia earnings, stock split, buyback, dividend, short squeeze,
all-time high, market cap trillion, index rebalance, EPS beat,
earnings surprise, guidance raised, revenue beat, beat estimates,
CPI, inflation, non-farm payroll, NFP, Fed rate, FOMC,
recession, VIX, volatility, circuit breaker
```

### Remix Signal Ideas

- **Yahoo Finance options chain**: Free unofficial API gives implied volatility and options-implied earnings move — compare the options-implied probability band to Polymarket price for earnings beat/miss markets; the gap is consistently 15–25% for mid-cap companies
- **CBOE VIX data feed**: VIX level and futures term structure — when VIX spikes, crash markets overprice; when VIX term structure inverts, macro catalyst timing signal for index threshold markets
- **SEC EDGAR 8-K filings**: Real-time earnings releases hit EDGAR before press coverage — earnings results are public on EDGAR minutes before Polymarket reprices
- **CME FedWatch**: Fed rate probability from federal funds futures — direct input for "will the Fed cut/hike?" markets; far more precise than Polymarket retail pricing


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
| `SIMMER_MAX_POSITION` | `35` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `15000` | Min market volume filter (USD) — equity markets need liquidity |
| `SIMMER_MAX_SPREAD` | `0.07` | Max bid-ask spread (7%) |
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
