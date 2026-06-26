---
name: paradex-market-analyst
description: >
  Technical analysis, market screening, and regime classification for Paradex
  perpetual futures markets. Computes indicators (RSI, MACD, Bollinger Bands,
  ATR, VWAP) from kline data, scans funding rates for arbitrage opportunities,
  analyzes orderbook depth and imbalances, classifies market regimes (trending,
  ranging, volatile), and screens across all markets for trading opportunities.
  Use this skill when the user asks about technical analysis on Paradex, market
  conditions, support/resistance levels, indicators, funding rate screening,
  orderbook depth, "what's the market doing", "is BTC trending", "find me
  opportunities", "market overview", "top movers", or any analytical question
  about Paradex market data and conditions.
---

# Paradex Market Analyst

Turns raw Paradex market data into actionable technical analysis and market intelligence.
Answers "what's the market doing?" with indicators, regime context, and opportunities.

## Available MCP Tools

| Tool | Market data it provides |
|---|---|
| `paradex_klines` | Historical OHLCV candles for indicator computation |
| `paradex_orderbook` | Depth analysis, imbalance detection |
| `paradex_bbo` | Real-time best bid/ask, spread |
| `paradex_market_summaries` | Cross-market screening, 24h stats, funding rates |
| `paradex_funding_data` | Funding rate history for carry analysis |
| `paradex_trades` | Trade flow, volume profile |
| `paradex_markets` | Market specs, available markets list |

## Capabilities

### 1. Technical Indicator Computation

Compute indicators from `paradex_klines` data. Fetch candles at the appropriate
resolution for the analysis timeframe, then calculate in-context:

- **RSI (14-period)**: Relative Strength Index via Wilder's smoothing.
  Overbought above 70, oversold below 30. Divergences between price and RSI
  are stronger signals than absolute levels alone.

- **MACD (12, 26, 9)**: MACD line = 12-EMA minus 26-EMA. Signal line = 9-EMA
  of MACD. Histogram = MACD minus signal. Watch for signal line crossovers
  and histogram direction changes.

- **Bollinger Bands (20, 2 sigma)**: Middle band = 20-period SMA, upper/lower = +/- 2
  standard deviations. Squeeze detection: bandwidth contracting to a 20-period low
  signals an impending breakout. Band walks (price hugging upper or lower band)
  indicate strong trends.

- **ATR (14-period)**: Average True Range for volatility measurement and stop
  placement. Normalize as ATR% = ATR / close x 100 for cross-market comparison.

- **VWAP**: Cumulative(typical_price x volume) / cumulative(volume). Intraday
  fair value reference. Price above VWAP = bullish bias, below = bearish bias.

- **SMA/EMA**: Simple and exponential moving averages for trend direction and
  dynamic support/resistance. Key levels: 20 EMA (short-term), 50 SMA
  (medium-term), 200 SMA (long-term trend).

- **Volume analysis**: Compute relative volume from `paradex_trades` data.
  Current volume vs. 20-period average volume ratio. Spikes above 2x average
  confirm breakouts; declining volume warns of fading moves.

### 2. Market Regime Classification

Classify the current market state for each market. This drives which strategies
and indicators are most useful.

**Trending:**
- ADX > 25
- Price consistently above (uptrend) or below (downtrend) 20 EMA
- Higher highs and higher lows (up) or lower highs and lower lows (down)
- MACD histogram expanding in one direction
- Action: favor trend-following indicators, avoid mean reversion

**Ranging:**
- ADX < 20
- RSI oscillating around 50, bouncing between 40-60
- Price contained within Bollinger Bands, no band walks
- Well-defined support and resistance levels
- Action: favor mean reversion, support/resistance plays

**Volatile:**
- ATR > 1.5x its 20-period average
- Wide Bollinger Bands (bandwidth expanding)
- Large candle bodies and wicks
- Action: widen stops, reduce position sizes, wait for regime clarity

**Quiet:**
- ATR < 0.5x its 20-period average
- Bollinger Band squeeze (bandwidth at 20-period low)
- Low volume relative to average
- Action: watch for breakout, prepare directional entries, tighten entries

### 3. Funding Rate Arbitrage Scanning

Systematic scan for funding rate opportunities across all Paradex markets:

1. **Fetch current rates**: `paradex_market_summaries` for all markets — extract
   funding rates and mark prices
2. **Identify extremes**: rank markets by absolute funding rate, flag top and
   bottom outliers
3. **Check persistence**: use `paradex_funding_data` to pull recent history for
   flagged markets — is the rate consistently extreme or a one-off spike?
4. **Annualize**: 8h funding rate x 3 = daily rate, x 365 = annualized rate
5. **Report**: for each opportunity, include market, direction to receive funding,
   current rate, annualized yield, persistence (how many of the last N periods
   were in the same direction), and any directional risk context

A funding rate of 0.01% per 8h = 0.03% daily = 10.95% annualized.
Rates above 0.05% per 8h (~55% annualized) are worth flagging.

### 4. Orderbook Analysis

Use `paradex_orderbook` to analyze market microstructure:

- **Depth at key levels**: aggregate liquidity at 0.5%, 1%, and 2% from mid-price
  on both bid and ask sides. Report in USD notional.

- **Bid/ask imbalance ratio**: total bid depth / total ask depth within 2% of mid.
  Ratio > 1.5 suggests buying pressure, < 0.67 suggests selling pressure.

- **Large resting orders (walls)**: identify individual price levels with
  outsized resting quantity — potential support/resistance that algorithms and
  traders watch.

- **Slippage estimation**: for a given trade size, walk the book to estimate
  execution price and slippage in basis points. Report as:
  "A $100K market buy would fill at an average price of $X (Y bps slippage)."

- **Support/resistance from order clusters**: price levels where resting orders
  are significantly above average depth — these act as short-term support
  (bid clusters) or resistance (ask clusters).

### 5. Cross-Market Screening

Use `paradex_market_summaries` to scan across all markets and surface opportunities:

- **Top movers**: rank by 24h price change (both gainers and losers)
- **Volume leaders**: rank by 24h trading volume — where is the action?
- **Funding rate extremes**: highest and lowest current funding rates
- **Volatility ranking**: rank by implied or realized volatility (from price
  change magnitude and spread width)
- **Spread comparison**: tightest and widest spreads (from BBO data) as a
  proxy for liquidity and trading cost

Present as a screening table. Highlight anything unusual: sudden volume spikes,
funding rate flips, or outsized moves relative to BTC.

### 6. Multi-Timeframe Analysis

Layer analysis across multiple timeframes to build a complete picture:

1. **Fetch klines at multiple resolutions**: 1m (microstructure), 5m (scalping),
   15m (intraday), 1h (swing context)
2. **Compute indicators at each timeframe**: RSI, MACD, trend direction
3. **Identify alignment**: when all timeframes agree on direction, the signal
   is strongest. Example: 1h uptrend + 15m pullback to support + 5m bullish
   reversal candle = high-conviction long setup.
4. **Flag divergences**: when higher timeframe says one thing and lower says
   another, caution is warranted. Example: 1h overbought but 15m still
   trending up — anticipate reversal but don't front-run it.

## Output Formats

### Quick Market Check ("How's BTC?")

Pull `paradex_bbo` + `paradex_market_summaries` for a concise snapshot. 3-4 sentences:

```
BTC-USD-PERP is trading at $X, [up/down] X% in the last 24h.
The market is in a [trending/ranging/volatile/quiet] regime — [1 sentence of evidence].
Key levels: support near $X (orderbook cluster / BB lower), resistance near $X.
Funding is [positive/negative] at X% (annualized X%) — [longs/shorts] are paying.
```

### Technical Analysis Report

Full indicator suite for a specific market, structured for readability:

```
## Technical Analysis — [MARKET]

**Price**: $X | **24h Change**: X% | **Volume**: $X (Xh avg: $X)

### Trend
- Regime: [Trending Up / Trending Down / Ranging / Volatile / Quiet]
- 20 EMA: $X (price [above/below] by X%)
- 50 SMA: $X | 200 SMA: $X
- ADX: X ([strong trend / weak trend / no trend])

### Momentum
- RSI (14): X ([overbought / neutral / oversold])
- MACD: [bullish/bearish] — signal [above/below] line, histogram [expanding/contracting]

### Volatility
- ATR (14): $X (X% of price) — [high/normal/low] vs. 20-period average
- Bollinger Bands: upper $X / mid $X / lower $X
- Bandwidth: X% — [squeeze / normal / expanded]

### Key Levels
- Resistance: $X [source: BB upper / orderbook wall / recent high]
- Support: $X [source: BB lower / orderbook wall / recent low]
- VWAP: $X (price [above/below])

### Funding
- Current rate: X% per 8h (X% annualized)
- Trend: [rising/falling/stable] over last 24h
```

### Market Screening Table

Cross-market overview for "what's moving" or "find me opportunities":

```
## Paradex Market Screening — [date/time]

| Market | Price | 24h Chg | Volume | Funding (8h) | Ann. Rate | Regime |
|---|---|---|---|---|---|---|
| BTC-USD-PERP | $X | X% | $X | X% | X% | Trending |
| ETH-USD-PERP | $X | X% | $X | X% | X% | Ranging |
| ... | ... | ... | ... | ... | ... | ... |

**Top Mover**: [MARKET] at X%
**Volume Leader**: [MARKET] at $X
**Funding Opportunity**: [MARKET] at X% annualized ([long/short] to collect)
```

### Funding Arbitrage Scan

Dedicated funding rate opportunity table:

```
## Funding Rate Scan — [date/time]

| Market | Current 8h Rate | Annualized | Direction to Collect | Persistent? | Notes |
|---|---|---|---|---|---|
| MARKET-A | 0.XX% | XX% | Short | 8/8 last periods | Strong |
| MARKET-B | -0.XX% | XX% | Long | 5/8 last periods | Moderate |

**Strongest opportunity**: [MARKET] — X% annualized by going [long/short].
Rate has been consistent for [N periods]. Watch for reversal if [condition].
```

### Regime Summary

Current regime classification across all markets:

```
## Market Regime Summary

| Market | Regime | ADX | RSI | ATR vs Avg | Trend Direction |
|---|---|---|---|---|---|
| BTC-USD-PERP | Trending | 32 | 58 | 1.1x | Up |
| ETH-USD-PERP | Ranging | 15 | 48 | 0.8x | Neutral |
| SOL-USD-PERP | Volatile | 28 | 72 | 1.8x | Up (overextended) |

**Overall market tone**: [risk-on / risk-off / mixed / uncertain]
```

## Caveats

- Indicators are computed from available kline data — limited by API history depth
  and resolution. Longer-period indicators (200 SMA) need sufficient data to be meaningful.
- Technical analysis is probabilistic, not predictive. Indicators describe current
  conditions and historical tendencies, not future certainty.
- Funding rates can reverse quickly — a rate that looks attractive now can flip
  direction within a single funding period.
- Orderbook depth is a snapshot in time. Large resting orders can be pulled
  before they fill. Do not treat orderbook walls as guaranteed support/resistance.
- Cross-market screening shows current conditions. By the time you act, the data
  may have shifted. Always re-check before entering.
- This is market analysis, not trading advice.

## References

See [indicators.md](references/indicators.md) for detailed indicator formulas and parameter guidance.
