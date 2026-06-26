# Technical Indicator Reference

Detailed computation steps and parameter guidance for all indicators used by the
Market Analyst skill. All formulas assume input from `paradex_klines` OHLCV data
unless noted otherwise.

---

## RSI — Relative Strength Index

Measures momentum by comparing the magnitude of recent gains to recent losses.

### Computation

1. **Price changes**: for each candle, compute `change = close - prev_close`
2. **Separate gains and losses**:
   - `gain = change` if change > 0, else 0
   - `loss = |change|` if change < 0, else 0
3. **First average** (period N, default 14):
   - `avg_gain = sum(gains over first N periods) / N`
   - `avg_loss = sum(losses over first N periods) / N`
4. **Subsequent averages** (Wilder's smoothing):
   - `avg_gain = (prev_avg_gain * (N - 1) + current_gain) / N`
   - `avg_loss = (prev_avg_loss * (N - 1) + current_loss) / N`
5. **Relative Strength**: `RS = avg_gain / avg_loss`
6. **RSI**: `RSI = 100 - (100 / (1 + RS))`

If avg_loss is 0, RSI = 100. If avg_gain is 0, RSI = 0.

### Interpretation

| RSI Range | Reading | Typical Action |
|---|---|---|
| > 80 | Extremely overbought | Strong reversal warning |
| 70 - 80 | Overbought | Watch for bearish divergence |
| 50 - 70 | Bullish momentum | Trend continuation likely |
| 40 - 50 | Neutral / weak | No clear signal |
| 30 - 40 | Bearish momentum | Trend continuation likely |
| 20 - 30 | Oversold | Watch for bullish divergence |
| < 20 | Extremely oversold | Strong reversal warning |

**Divergence**: price makes new high but RSI does not (bearish divergence) or
price makes new low but RSI does not (bullish divergence). Divergences are
among the most reliable RSI signals.

**Note**: in strong trends, RSI can stay overbought or oversold for extended
periods. Do not blindly fade extremes without confirming the regime.

---

## MACD — Moving Average Convergence Divergence

Measures trend direction, momentum, and potential reversals by comparing two
exponential moving averages.

### Computation

1. **Fast EMA**: 12-period EMA of close prices
2. **Slow EMA**: 26-period EMA of close prices
3. **MACD line**: `MACD = fast_EMA - slow_EMA`
4. **Signal line**: 9-period EMA of the MACD line
5. **Histogram**: `histogram = MACD - signal`

See the EMA section below for the EMA formula.

### Signals

- **Bullish signal crossover**: MACD crosses above the signal line. Stronger
  when both are below zero (reversal from bearish territory).
- **Bearish signal crossover**: MACD crosses below the signal line. Stronger
  when both are above zero (reversal from bullish territory).
- **Zero line crossover**: MACD crossing above zero confirms uptrend; crossing
  below confirms downtrend.
- **Histogram expansion**: increasing histogram bars confirm momentum is building.
- **Histogram contraction**: shrinking bars warn that momentum is fading, even
  if the trend hasn't reversed yet.
- **Divergence**: price makes new high but MACD does not (bearish) or price
  makes new low but MACD does not (bullish).

### Practical Notes

MACD is a lagging indicator — it confirms trends rather than predicting them.
In ranging markets, MACD generates frequent whipsaws. Combine with a regime
filter (ADX < 20 = ranging, skip MACD crossover signals).

---

## Bollinger Bands

Envelope indicator that adapts to volatility, useful for identifying
overbought/oversold conditions and volatility squeezes.

### Computation

1. **Middle band**: 20-period SMA of close prices
2. **Standard deviation**: 20-period standard deviation of close prices
3. **Upper band**: `SMA + (2 * std_dev)`
4. **Lower band**: `SMA - (2 * std_dev)`

### Derived Metrics

- **%B** (percent B): `%B = (close - lower_band) / (upper_band - lower_band)`
  - %B > 1: price above upper band (overbought)
  - %B < 0: price below lower band (oversold)
  - %B = 0.5: price at middle band

- **Bandwidth**: `bandwidth = (upper_band - lower_band) / middle_band`
  - Measures how wide the bands are relative to the average

- **Squeeze detection**: bandwidth falls to its lowest value in the last 20
  periods. A squeeze signals that volatility is compressing — a breakout
  (direction unknown) is likely imminent.

### Interpretation

- **Band walk (upper)**: price consistently closes near or above the upper band.
  This is a sign of a strong uptrend, not necessarily a sell signal.
- **Band walk (lower)**: price consistently closes near or below the lower band.
  Strong downtrend signal.
- **Mean reversion**: price touches upper/lower band and reverses back toward the
  middle band. Works best in ranging regimes (ADX < 20).
- **Squeeze breakout**: after a squeeze, the first decisive close outside either
  band indicates the breakout direction. Volume confirmation strengthens the signal.

### Why 2 Sigma?

With normally distributed data, ~95% of values fall within 2 standard deviations.
Price touching or exceeding the bands is statistically unusual — but crypto is
fat-tailed, so bands are breached more often than the normal distribution predicts.

---

## ATR — Average True Range

Measures volatility as the average range of price movement, accounting for gaps.

### Computation

1. **True Range** for each candle (pick the largest of three):
   - `high - low` (intrabar range)
   - `|high - prev_close|` (gap up impact)
   - `|low - prev_close|` (gap down impact)

2. **First ATR**: simple average of the first N true range values (N = 14 default)

3. **Subsequent ATR** (Wilder's smoothing):
   `ATR = (prev_ATR * (N - 1) + current_TR) / N`

### Derived Metrics

- **ATR%**: `ATR / close * 100` — normalized volatility for cross-market comparison.
  A market with ATR% of 3% is more volatile than one with 1%, regardless of
  absolute price levels.

- **ATR ratio**: `current_ATR / 20-period SMA of ATR` — how current volatility
  compares to recent average. Used for regime classification:
  - Ratio > 1.5: volatile regime
  - Ratio 0.5 - 1.5: normal
  - Ratio < 0.5: quiet regime

### Uses

- **Stop placement**: a common approach is to set stops at 1.5-2x ATR from entry.
  This adapts stops to current market volatility.
- **Position sizing**: smaller positions when ATR is high, larger when ATR is low,
  to keep dollar risk per trade consistent.
- **Regime filter**: high ATR environments favor trend-following; low ATR favors
  mean reversion and breakout anticipation.

---

## VWAP — Volume-Weighted Average Price

The average price weighted by volume. Institutional benchmark for intraday fair value.

### Computation

1. **Typical price** for each candle: `TP = (high + low + close) / 3`
2. **Cumulative TP x Volume**: running sum of `TP * volume` from the start of the period
3. **Cumulative Volume**: running sum of `volume` from the start of the period
4. **VWAP**: `cumulative(TP * volume) / cumulative(volume)`

VWAP resets at the start of each trading day (00:00 UTC for crypto).

### Interpretation

- **Price above VWAP**: buyers are in control on average — bullish intraday bias
- **Price below VWAP**: sellers are in control on average — bearish intraday bias
- **Price crossing VWAP**: potential shift in intraday direction
- **VWAP as support/resistance**: price often reacts to VWAP on first touch,
  especially in ranging conditions

### Practical Notes

VWAP is most useful on intraday timeframes (1m to 1h candles). On daily or
weekly charts, it becomes less actionable. For crypto, the "daily reset" at
00:00 UTC means VWAP is freshest (and least meaningful) right after midnight UTC.

---

## ADX/DI — Average Directional Index

Measures trend strength (not direction). Used primarily for regime classification.

### Computation

1. **Directional Movement**:
   - `+DM = high - prev_high` (if positive and > `prev_low - low`, else 0)
   - `-DM = prev_low - low` (if positive and > `high - prev_high`, else 0)
   - If both are positive, keep only the larger one; set the other to 0

2. **Smooth over N periods** (default 14) using Wilder's smoothing:
   - `smoothed_+DM = prev_smoothed_+DM - (prev_smoothed_+DM / N) + current_+DM`
   - `smoothed_-DM = prev_smoothed_-DM - (prev_smoothed_-DM / N) + current_-DM`
   - `smoothed_TR = prev_smoothed_TR - (prev_smoothed_TR / N) + current_TR`

3. **Directional Indicators**:
   - `+DI = (smoothed_+DM / smoothed_TR) * 100`
   - `-DI = (smoothed_-DM / smoothed_TR) * 100`

4. **DX**: `DX = |+DI - -DI| / (+DI + -DI) * 100`

5. **ADX**: 14-period Wilder's smoothed average of DX
   - First ADX = simple average of first 14 DX values
   - Subsequent: `ADX = (prev_ADX * (N - 1) + current_DX) / N`

### Interpretation

| ADX Value | Trend Strength | Regime |
|---|---|---|
| 0 - 15 | Absent or very weak | Ranging / choppy |
| 15 - 20 | Weak | Transitional |
| 20 - 25 | Emerging | Early trend |
| 25 - 50 | Strong | Trending |
| 50 - 75 | Very strong | Strong trend |
| > 75 | Extremely strong | Rare, often near exhaustion |

**+DI vs -DI**:
- `+DI > -DI`: upward pressure dominates
- `-DI > +DI`: downward pressure dominates
- Crossovers of +DI/-DI with ADX > 25 are directional signals

**Note**: ADX measures trend strength, not direction. A falling ADX means the
trend is weakening, not that the market is going down.

---

## EMA — Exponential Moving Average

Weighted moving average that gives more weight to recent prices, making it more
responsive than an SMA.

### Computation

1. **Multiplier**: `k = 2 / (period + 1)`
2. **First EMA**: SMA of the first N values (seed value)
3. **Subsequent EMA**: `EMA = close * k + prev_EMA * (1 - k)`

### Common Periods

- **9 EMA**: very short-term, used by scalpers
- **20 EMA**: short-term trend, used for regime classification
- **50 EMA/SMA**: medium-term trend
- **200 SMA**: long-term trend benchmark ("the 200-day")

### EMA vs SMA

EMA reacts faster to recent price changes, producing earlier signals but more
whipsaws. SMA is smoother and better for identifying sustained trends. In
practice, use EMA for shorter periods (9, 20) and SMA for longer periods
(50, 200) to balance responsiveness and stability.

---

## Parameter Recommendations by Timeframe

Different trading timeframes benefit from different indicator periods. The
standard parameters (RSI 14, BB 20, etc.) are designed for daily charts.
Shorter timeframes need shorter lookbacks; longer timeframes benefit from
wider windows.

### Scalping (1m - 5m candles)

| Indicator | Adjusted Period | Notes |
|---|---|---|
| RSI | 7 | Faster response to micro-moves |
| MACD | 6, 13, 5 | Halved periods for quicker signals |
| Bollinger Bands | 10, 2 sigma | Tighter window, more touches |
| ATR | 7 | Recent volatility for tight stops |
| EMA | 9 / 21 | Short-term trend |
| VWAP | Standard | Always cumulative from session start |

**Notes**: at 1m-5m, noise is high. Use indicators as confirmation, not primary
signals. Orderbook data and trade flow are often more valuable at this timeframe.

### Intraday (15m - 1h candles)

| Indicator | Period | Notes |
|---|---|---|
| RSI | 14 | Standard works well |
| MACD | 12, 26, 9 | Standard parameters |
| Bollinger Bands | 20, 2 sigma | Standard parameters |
| ATR | 14 | Standard parameters |
| EMA | 20 / 50 | Short and medium trend |
| VWAP | Standard | Primary fair-value reference |

**Notes**: the sweet spot for most technical analysis. Standard parameters were
largely designed for this range (originally daily, but crypto's 24/7 nature
makes 15m-1h analogous to daily in traditional markets).

### Swing Trading (4h - 1d candles)

| Indicator | Adjusted Period | Notes |
|---|---|---|
| RSI | 21 | Smoother, fewer false signals |
| MACD | 12, 26, 9 | Standard holds up at this timeframe |
| Bollinger Bands | 30, 2 sigma | Wider window captures bigger moves |
| ATR | 21 | Smoothed volatility for wider stops |
| EMA/SMA | 50 / 200 | Major trend levels |
| VWAP | Less useful | Resets daily, less meaningful on multi-day |

**Notes**: at 4h-1d, focus on trend direction and key levels rather than
precise entries. Indicators serve as confirmation for macro thesis. ADX is
particularly useful here for regime classification over the medium term.

---

## General Notes

- **Wilder's smoothing** (used in RSI, ATR, ADX) is equivalent to an EMA with
  period `2N - 1`. For RSI 14, the effective EMA length is 27 periods. This
  means these indicators need ~50+ candles of data to stabilize.

- **Lookback requirements**: to compute indicators reliably, fetch at least 2-3x
  the longest indicator period in candles. For standard parameters, 100 candles
  is a good minimum. For 200 SMA, fetch 250+ candles.

- **All indicators lag** to some degree. They describe what has happened, not
  what will happen. The value is in identifying the current market state and
  likely continuation or reversal patterns — probabilities, not certainties.
