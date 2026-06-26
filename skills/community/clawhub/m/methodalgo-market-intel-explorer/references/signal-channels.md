# Signal Channels Detailed Reference

## Breakout Signals (Breakout)

### breakout-htf (High Timeframe Breakout)
- **Timeframes**: 1D / 3D
- **Mechanism**: Detects breakouts of the high/low points within a 100-candle rolling window.
- **`details` Fields**: `Symbol`, `TimeFrame`, `Type` (UP/DOWN), `BreakPrice`, `Exchange`

### breakout-mtf (Medium Timeframe Breakout)
- **Timeframes**: 1H / 4H
- **Mechanism**: Detects breakouts of the high/low points within a 100-candle rolling window.
- **`details` Fields**: Same as `breakout-htf`

### breakout-24h (24-hour Breakout)
- **Timeframes**: Based on a rolling 24-hour window.
- **Mechanism**: Continuously monitors for breakouts based on the high/low prices of the past 24 hours.
- **`details` Fields**: Same as `breakout-htf`

---

## Liquidation Signals (Liquidation)

### liquidation (Large Liquidation)
- **Mechanism**: Real-time alerts for large liquidation orders.
- **`details` Fields**: `Symbol`, `Side`, `Quantity`, `Average Price`, `Liquidation Price`, `Position Total`

---

## Exhaustion Signals (Reversal)

### exhaustion-buyer
- **Mechanism**: Based on the Liquidation Heatmap, it detects if the single-sided buyer liquidation inventory is <10% or <5%.
- **Meaning**: Buyer exhaustion → Price may reverse and drop.
- **`details` Fields**: `Type`, `Timeframe`, `Exhaustion Side`, `Safety`, `Tip`, `Exchange`

### exhaustion-seller
- **Mechanism**: Based on the Liquidation Heatmap, it detects if the single-sided seller liquidation inventory is <10% or <5%.
- **Meaning**: Seller exhaustion → Price may reverse and rise.
- **`details` Fields**: `Type`, `Timeframe`, `Exhaustion Side`, `Safety`, `Tip`, `Exchange`

> ⚠️ Exhaustion signals are **reversal signals**. For example, when an `exhaustion-buyer` signal is issued, the price may be rising, but the algorithm has detected limited buying pressure ahead, suggesting a potential downward reversal.

---

## Golden Pit Signals (Golden Pit)

### golden-pit-mtf (Medium Timeframe Golden Pit)
- **Timeframes**: 30m / 1h / 4h
- **Mechanism**: Smart Cloud pattern detection, indicating significant programmatic volatility to follow.
- **Bull Pit**: A brief dip followed by a price pump.
- **Bear Pit**: A brief bounce followed by a price dump.
- **`details` Fields**: `Pattern`, `Safety`

### golden-pit-ltf (Low Timeframe Golden Pit)
- **Timeframes**: 5m / 15m
- **Mechanism**: Same as `golden-pit-mtf`
- **`details` Fields**: Same as `golden-pit-mtf`

---

## Token Unlock (Token Unlock)

### token-unlock
- **Data Structure**: Unlike other channels, it returns `{ signals: [...], updatedAt: timestamp }`.
- **`details` Fields**: `symbol`, `perc`, `progress`, `circSup`, `countDown`, `marketCap`, `unlockToken`, `unlockTokenVal`

---

## ETF Tracker (ETF Tracker)

### etf-tracker
- **Mechanism**: Daily fund inflow and outflow tracking for BTC/ETH/SOL/XRP.
- **`details` Fields**: `Net Inflow`, `7 Days Avg.`

---

## Market Comprehensive Metrics (Market Today)

### market-today
- **Mechanism**: Discord-style published market summary stream. It may include images and narrative market sentiment content.
- Use `methodalgo totals --json` for structured BTC dominance, ETH dominance, total market cap, Fear & Greed, and Altseason Index values.
- **`details` Fields**: Varies by published summary item. Do not rely on this channel for structured metric values.
