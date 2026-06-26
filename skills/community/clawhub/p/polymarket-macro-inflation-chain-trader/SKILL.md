---
name: polymarket-macro-inflation-chain-trader
description: Three-step macro chain reaction trader for Polymarket. Chains commodity pressure (oil, WTI, crude) through inflation and rate expectations (Fed, FOMC) to equity-threshold markets (NVIDIA, S&P, Nasdaq). When commodities surge but equities havent corrected, sells equity optimism. When commodities crash and equities overreact, buys the oversold dip. Most traders think in single categories -- this skill chains three macro layers to find divergence alpha.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Macro Inflation Chain Trader
  difficulty: advanced
---

# Macro Inflation Chain Trader

> **This is a template.**
> The default signal chains commodity pressure through rate expectations to equity markets -- remix it with real-time CPI data feeds, Fed funds futures, or Treasury yield curve signals.
> The skill handles all the plumbing (market discovery, classification, chain logic, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Most Polymarket traders analyze markets in isolation: oil markets, Fed markets, or equity markets separately. But macro economics is a chain reaction:

1. **Oil/commodity prices rise** -- input costs increase across the economy
2. **Inflation expectations rise** -- the Fed holds or hikes rates instead of cutting
3. **Rate-sensitive equities should fall** -- higher rates compress equity valuations

This skill monitors all three layers simultaneously and trades the **divergence** when one layer hasn't caught up to the others.

## Signal Logic

### Step 1: Classify Markets

All markets from `get_markets(limit=200)` are classified into three buckets:

- **Commodity**: oil, WTI, crude, brent, natural gas, copper, gold, OPEC
- **Monetary**: Fed, rate cut/hike, FOMC, inflation, CPI, interest rate, Powell
- **Equity**: NVIDIA, Amazon, S&P, Nasdaq, stock, earnings, market cap

### Step 2: Compute Aggregate Indicators

| Indicator | Calculation |
|---|---|
| `commodity_pressure` | Average probability of commodity markets (high = commodities rising) |
| `rate_hawkish` | Average hawkish probability (rate hold/hike markets + inverse of rate cut markets) |
| `equity_optimism` | Average probability of equity-above-threshold markets |

### Step 3: Chain Logic

| Condition | Signal | Reasoning |
|---|---|---|
| `commodity_pressure > 0.50` AND `equity_optimism > 0.55` | Sell NO on equity thresholds | Equities haven't priced in commodity pain |
| `commodity_pressure < 0.30` AND `equity_optimism < 0.40` | Buy YES on equity thresholds | Equities overreacted to low commodity pressure |
| Neither condition met | Fall back to standard conviction signals | No macro divergence detected |

### Conviction-Based Sizing

- Chain signals scale with the magnitude of the divergence between commodity and equity layers
- Standard signals use the CLAUDE.md formula: `conviction = (threshold - p) / threshold`
- Size = `max(MIN_TRADE, conviction * MAX_POSITION)` -- never flat sizing

### Remix Ideas

- **Fed funds futures**: Replace `rate_hawkish` with CME FedWatch implied probabilities
- **Treasury yield curve**: Use 2y-10y spread as a direct hawkish/dovish indicator
- **CPI nowcasting**: Feed Cleveland Fed CPI nowcast into `commodity_pressure` for real-time inflation signals
- **Supply chain indices**: Add Baltic Dry Index or semiconductor lead times for deeper commodity pressure

## Market Categories Tracked

```python
COMMODITY_KW = ['oil', 'wti', 'crude', 'brent', 'commodity', 'commodities',
                'natural gas', 'copper', 'gold price', 'silver price',
                'oil price', 'barrel', 'opec']
MONETARY_KW  = ['fed', 'federal reserve', 'rate cut', 'rate hike', 'fomc',
                'inflation', 'cpi', 'interest rate', 'monetary policy',
                'powell', 'rate hold', 'basis points', 'hawkish', 'dovish']
EQUITY_KW    = ['nvidia', 'amazon', 's&p', 'sp500', 'nasdaq', 'stock',
                'dow jones', 'apple', 'tesla', 'microsoft', 'google',
                'meta', 'equity', 'market cap', 'ipo', 'earnings',
                'above', 'below', 'stock price']
```

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Max position size | $40 USDC | Per market, reached at max conviction |
| Min market volume | $3,000 | Liquidity filter |
| Max bid-ask spread | 10% | Macro markets are typically liquid |
| Min days to resolution | 7 | Chain reactions need time to propagate |
| Max open positions | 8 | Diversify across equity targets |

## Installation & Setup

```bash
clawhub install polymarket-macro-inflation-chain-trader
```

Requires: `SIMMER_API_KEY` environment variable.

## Cron Schedule

Runs on demand or via automaton. Cron is set to `null` -- configure it in the Simmer UI when ready.

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only execute when `--live` is passed explicitly.**

| Scenario | Mode | Financial risk |
|----------|------|----------------|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

The automaton cron is set to `null` -- it does not run on a schedule until you configure it in the Simmer UI. `autostart: false` means it won't start automatically on install.

## Required Credentials

| Variable | Required | Notes |
|----------|----------|-------|
| `SIMMER_API_KEY` | Yes | Trading authority -- keep this credential private. |

## Tunables (Risk Parameters)

All risk parameters are declared in `clawhub.json` as `tunables` and adjustable from the Simmer UI without code changes. They use `SIMMER_`-prefixed env vars so `apply_skill_config()` can load them securely.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (0.10 = 10%) |
| `SIMMER_MIN_DAYS` | `7` | Min days until market resolves |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price <= this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price >= this value |
| `SIMMER_COMMODITY_PRESSURE` | `0.50` | Commodity pressure threshold to trigger sell-equity chain |
| `SIMMER_EQUITY_OPTIMISM_HIGH` | `0.55` | Equity optimism above this = overpriced if commodities high |
| `SIMMER_EQUITY_OPTIMISM_LOW` | `0.40` | Equity optimism below this = oversold if commodities low |
| `SIMMER_COMMODITY_LOW` | `0.30` | Commodity pressure below this = deflationary signal |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
