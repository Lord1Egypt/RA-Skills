---
name: polymarket-macro-weekend-momentum-trader
description: Trades altcoin (ETH/SOL/XRP) Up/Down markets based on BTC weekend price threshold momentum drift. BTC leads altcoins by 6-24 hours on weekends because altcoin market makers are less active. Calculates BTC drift direction from the threshold ladder and trades altcoins that havent caught up yet.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Macro Weekend Momentum Trader
  difficulty: advanced
---

# Macro Weekend Momentum Trader

> **This is a template.**
> The default signal uses BTC price threshold ladder drift to predict altcoin direction on weekends -- remix it with real-time Binance data, funding rates, or on-chain whale flow.
> The skill handles all the plumbing (market discovery, drift calculation, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Every weekend, Polymarket lists BTC price threshold markets ("Will BTC trade above $66k?") AND altcoin Up/Down markets ("Ethereum Up or Down - Saturday 2:00PM"). BTC leads altcoins by 6-24 hours on weekends because altcoin market makers are less active -- they reduce liquidity provision on Saturdays and Sundays, creating a systematic lag in price discovery.

The BTC threshold ladder acts as a real-time sentiment thermometer. When P(above $66k) rises from 40% to 60% over a few hours, that signals bullish weekend drift. But ETH/SOL/XRP Up/Down markets are still priced at ~50% because altcoin market makers haven't repriced yet. By the time they do, the opportunity is gone.

## Edge

BTC weekend drift predicts altcoin direction with a 6-24 hour lag:

1. **BTC leads, altcoins lag** -- On weekends, BTC price moves propagate to altcoins with a delay because altcoin market makers reduce their weekend presence. Polymarket altcoin Up/Down markets are priced by the same thin weekend liquidity.

2. **Threshold ladder as drift signal** -- BTC threshold markets form a probability ladder (P(above 60k) > P(above 65k) > P(above 70k)). When the AVERAGE probability across the ladder shifts upward, it signals bullish momentum. When it steepens (low thresholds rising, high thresholds falling), it signals bearish.

3. **Weekend-only timing** -- The edge exists ONLY on weekends and Monday early hours. Weekday market makers are active and reprice altcoins quickly, closing the lag window.

4. **Cross-category macro signal** -- Using BTC threshold markets (a DIFFERENT market category) to predict altcoin Up/Down markets creates an information advantage that single-category traders miss entirely.

## Signal Logic

1. Discover active BTC price threshold markets AND altcoin Up/Down markets via keyword search + `get_markets(limit=200)` fallback
2. Extract BTC threshold levels and probabilities to build the "ladder"
3. Compute BTC "weekend drift":
   - Average probability across all thresholds (>0.5 = bullish, <0.5 = bearish)
   - Slope of the ladder (higher thresholds gaining = bullish)
   - Drift magnitude must exceed `DRIFT_THRESHOLD` (default 0.08)
4. Weekend/Monday gate: only active Saturday, Sunday, or Monday before 12:00 UTC
5. For each altcoin Up/Down market:
   - BTC bullish drift + altcoin at low p (below YES_THRESHOLD) -> buy YES
   - BTC bearish drift + altcoin at high p (above NO_THRESHOLD) -> buy NO
   - Conviction = distance from threshold, boosted by drift magnitude
   - Size = `max(MIN_TRADE, conviction * MAX_POSITION)`

### How Drift Calculation Works

| BTC Ladder State | Avg P | Drift | Action |
|---|---|---|---|
| P(60k)=80%, P(65k)=60%, P(70k)=40% | 0.60 | Bullish +0.10 | Buy YES on lagging altcoins |
| P(60k)=40%, P(65k)=25%, P(70k)=10% | 0.25 | Bearish -0.25 | Buy NO on lagging altcoins |
| P(60k)=55%, P(65k)=50%, P(70k)=45% | 0.50 | Neutral 0.00 | No trades |

### How Sizing Works

With defaults (YES_THRESHOLD=0.38, MIN_TRADE=$5, MAX_POSITION=$40, drift boost):

| Altcoin p | Base conviction | With drift=0.20 boost | Size |
|---|---|---|---|
| 38% (threshold) | 0% | 0% | $5 (floor) |
| 30% | 21% | 25% | $10 |
| 20% | 47% | 57% | $23 |
| 10% | 74% | 88% | $35 |

### Keywords Monitored

```
bitcoin above, btc above, BTCUSDT above, bitcoin reach, btc reach,
bitcoin hit, btc hit, bitcoin price, btc price, btc threshold,
Ethereum Up or Down, Solana Up or Down, XRP Up or Down,
ETH Up or Down, SOL Up or Down,
ethereum up, solana up, xrp up
```

### Remix Signal Ideas

- **Binance real-time BTCUSDT price**: Wire spot price deltas into the drift calculation for a more responsive signal than Polymarket threshold probabilities alone
- **Funding rates**: Positive BTC funding + bullish threshold drift = double confirmation; negative funding weakens the signal
- **On-chain whale flow**: Large BTC inflows to exchanges on weekends often precede sell pressure -- use as a counter-signal to bearish drift
- **Historical lag measurement**: Track how many hours each altcoin typically lags BTC on weekends to time entries more precisely

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
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread (8%) |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price <= this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price >= this value |
| `SIMMER_DRIFT_THRESHOLD` | `0.08` | Minimum BTC drift magnitude to trigger altcoin trades |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
