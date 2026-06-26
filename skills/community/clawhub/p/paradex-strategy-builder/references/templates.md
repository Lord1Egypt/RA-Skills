# Expanded Strategy Templates

Detailed parameter ranges, example calculations, and trade walkthroughs for each
strategy template defined in the Strategy Builder skill.

---

## 1. Funding Rate Arbitrage

### Overview

Collect funding payments by taking the opposite side of crowded positions. When the
market is overwhelmingly long, funding rates are positive, and short positions receive
payment. Vice versa when the market is overwhelmingly short.

### Parameter Ranges

| Parameter | Conservative | Moderate | Aggressive |
|---|---|---|---|
| Entry threshold (annualized rate) | > 30% | > 20% | > 10% |
| Exit threshold (annualized rate) | < 10% | < 5% | < 0% (rate flips) |
| Max position size | 5% of equity | 10% of equity | 20% of equity |
| Stop loss (price move) | -3% | -5% | -8% |
| Max holding period | 7 days | 14 days | 30 days |

### Annualized Rate Calculation

```
annualized_rate = 8h_funding_rate × 3 × 365 × 100%
```

Example: 8h rate of 0.01% = 0.01% × 3 × 365 = 10.95% annualized

### Example Calculation

**Scenario:** BTC-USD-PERP 8h funding rate = 0.03% (annualized ~32.85%)

1. **Signal:** Rate > 30% annualized threshold. Open a short position to receive funding.
2. **Position:** Short 0.1 BTC at $65,000. Notional = $6,500.
3. **Per funding interval (8h):** $6,500 × 0.0003 = $1.95 received
4. **Daily income:** $1.95 × 3 = $5.85
5. **7-day income (if rate persists):** $5.85 × 7 = $40.95
6. **Annualized yield on notional:** ~32.85%
7. **Stop loss:** If BTC moves up 3% ($66,950), close for -$195 loss
   - Break-even holding period at this rate: $195 / $5.85 = ~33 days

### Variants

#### Pure Funding Capture (Directional)

- Take the funding-receiving side only
- Accept directional price risk
- Higher yield but exposed to adverse price moves
- Best when you also have a directional view aligned with the funding trade

#### Delta-Neutral Funding Capture

- Short the perp (receive funding) + hold equivalent spot position
- Net directional exposure ≈ 0
- Profit = funding received - trading costs - any basis risk
- Requires spot market access (Paradex supports spot trading)
- Lower yield but minimal price risk
- Watch for basis widening between spot and perp

### Risk Factors

- Funding rates can reverse within a single interval
- In trending markets, funding-receiving side faces persistent price losses
- High funding often coincides with strong directional moves — fighting the trend
- Delta-neutral variant ties up 2x capital (perp margin + spot purchase)

### Strategy Specification

```
STRATEGY: Funding Rate Arbitrage
MARKET: [highest funding rate market from screening]
TIMEFRAME: 8h (funding intervals)

ENTRY RULES:
- Condition 1: Annualized funding rate > 20% (moderate threshold)
- Condition 2: Rate has been elevated for at least 3 consecutive intervals (persistent)
- Entry type: Market order (speed > price for funding capture)
- Position size: 10% of equity notional

EXIT RULES:
- Take profit: None (hold while rate remains elevated)
- Stop loss: -5% adverse price move from entry
- Time stop: Close if rate < 5% annualized for 24h
- Trailing stop: None (funding is the profit source)

RISK PARAMETERS:
- Max position size: 10% of equity
- Max loss per trade: 5% of position notional
- Max concurrent positions: 3 (across different markets)
- Max daily loss: 2% of equity, then halt new entries

FILTERS:
- Only trade when: Funding rate is persistent (3+ intervals above threshold)
- Avoid when: Major news events, rate just spiked (likely to mean-revert quickly)
```

---

## 2. Mean Reversion

### Overview

Prices tend to revert to a moving average after overextension. This strategy buys at
support (lower Bollinger Band + oversold RSI) and sells at resistance (upper Bollinger
Band + overbought RSI), targeting the middle band.

### Parameterizations

#### Tight Parameters (Ranging Markets)

| Parameter | Value |
|---|---|
| BB period | 20 |
| BB width | 1.5 standard deviations |
| RSI period | 14 |
| RSI oversold | < 35 |
| RSI overbought | > 65 |
| Target | Middle band (20 SMA) |
| Stop | 1.0 ATR beyond entry |
| Best for | Low-volatility, range-bound conditions |

#### Standard Parameters (Normal Markets)

| Parameter | Value |
|---|---|
| BB period | 20 |
| BB width | 2.0 standard deviations |
| RSI period | 14 |
| RSI oversold | < 30 |
| RSI overbought | > 70 |
| Target | Middle band (20 SMA) |
| Stop | 1.5 ATR beyond entry |
| Best for | Most market conditions |

#### Wide Parameters (Volatile Markets)

| Parameter | Value |
|---|---|
| BB period | 20 |
| BB width | 2.5 standard deviations |
| RSI period | 14 |
| RSI oversold | < 25 |
| RSI overbought | > 75 |
| Target | Middle band (20 SMA) |
| Stop | 2.0 ATR beyond entry |
| Best for | High-volatility conditions where standard params give false signals |

### RSI Thresholds by Market

| Market | Oversold | Overbought | Notes |
|---|---|---|---|
| BTC-USD-PERP | 30 | 70 | Standard — BTC trends but reverts reliably |
| ETH-USD-PERP | 28 | 72 | Slightly wider — ETH overshoots more |
| SOL-USD-PERP | 25 | 75 | Higher volatility, needs wider thresholds |
| DOGE-USD-PERP | 20 | 80 | Very volatile, only extreme readings are meaningful |
| Stablecoin pairs | 35 | 65 | Tight range, smaller deviations are significant |

### Example Trade Walkthrough

**Market:** ETH-USD-PERP, 4h klines

1. **Setup:** ETH trading in a range between $3,200 and $3,600 for 2 weeks.
   20-period BB on 4h chart: upper band $3,580, middle $3,400, lower $3,220.

2. **Signal (Long Entry):**
   - 4h candle closes at $3,228 — touching lower Bollinger Band ($3,220)
   - RSI(14) = 27 — below 28 oversold threshold for ETH
   - Both conditions met. Enter long.

3. **Entry:** Buy 2.0 ETH at $3,228. Notional = $6,456.
   ATR(14) on 4h = $85.

4. **Stop loss:** $3,228 - (1.5 × $85) = $3,100.50
   Risk per trade = 2.0 × ($3,228 - $3,100.50) = $255

5. **Target:** Middle band at $3,400
   Reward = 2.0 × ($3,400 - $3,228) = $344

6. **Risk:Reward = 1:1.35**

7. **Outcome:** Over the next 20 hours, ETH reverts to $3,395.
   Close at $3,395. Profit = 2.0 × ($3,395 - $3,228) = $334.
   Fees (if applicable): ~$3.87 round trip (0.03% taker each way).
   Net profit: ~$330.

### Strategy Specification

```
STRATEGY: Mean Reversion (Standard)
MARKET: ETH-USD-PERP
TIMEFRAME: 4h candles for signals

ENTRY RULES:
- Long: Price touches lower BB(20, 2.0) AND RSI(14) < 28
- Short: Price touches upper BB(20, 2.0) AND RSI(14) > 72
- Entry type: Limit order at the band level (for better fill)
- Position size: Risk $250 per trade (size = $250 / stop_distance)

EXIT RULES:
- Take profit: Middle band (20-period SMA)
- Stop loss: 1.5 ATR(14) beyond entry price
- Time stop: Close after 48h if neither TP nor SL hit
- Trailing stop: None (fixed target)

RISK PARAMETERS:
- Max position size: $10,000 notional
- Max loss per trade: $250
- Max concurrent positions: 2 (one long setup, one short setup)
- Max daily loss: $500 then halt

FILTERS:
- Only trade when: BB width > 2% of price (enough volatility for profit)
- Avoid when: BB width expanding rapidly (trend forming, not range)
- Avoid when: Major support/resistance break on daily chart
```

---

## 3. Momentum / Trend Following

### Overview

Enter in the direction of strong price moves, using breakout confirmation and trailing
stops to ride trends while cutting losers quickly.

### Breakout Confirmation Criteria

A valid breakout requires multiple confirming signals:

| Criterion | Threshold | Purpose |
|---|---|---|
| Price breakout | Close above 20-period high (or below 20-period low) | Core signal |
| Confirmation | 2 consecutive closes beyond the level | Reduce false breakouts |
| Volume spike | Volume > 1.5x 20-period average | Confirms participation |
| Spread check | Current spread < 0.1% | Ensures adequate liquidity |
| ATR filter | ATR(14) > ATR(50) | Volatility is expanding, not contracting |

### ATR-Based Stop Calculations

```
initial_stop_long  = entry_price - (ATR_multiplier × ATR(14))
initial_stop_short = entry_price + (ATR_multiplier × ATR(14))

trailing_stop_long  = highest_close_since_entry - (ATR_multiplier × ATR(14))
trailing_stop_short = lowest_close_since_entry + (ATR_multiplier × ATR(14))
```

| Risk Profile | ATR Multiplier | Characteristics |
|---|---|---|
| Tight | 1.5x | More frequent stops, catches smaller moves |
| Standard | 2.0x | Balanced — default recommendation |
| Wide | 3.0x | Stays in trends longer, larger drawdowns per trade |

### Example with Real Kline Scenario

**Market:** BTC-USD-PERP, 1h klines

**Setup phase (hours 1-20):**
BTC consolidating between $63,500 and $65,000. 20-period high = $65,000.
ATR(14) on 1h = $320. Volume average (20-period) = 45 BTC/hour.

**Breakout (hour 21):**
- 1h candle closes at $65,180 (above 20-period high of $65,000)
- Volume: 82 BTC (1.82x average) — confirmed
- Not yet entering — need 2nd confirmation close

**Confirmation (hour 22):**
- 1h candle closes at $65,420 (second close above $65,000)
- Volume: 68 BTC (1.51x average) — still elevated
- **ENTRY: Buy 0.2 BTC at $65,420**

**Stop and position sizing:**
- ATR(14) = $320
- Initial stop: $65,420 - (2.0 × $320) = $64,780
- Risk per unit: $65,420 - $64,780 = $640
- If risking $300 per trade: size = $300 / $640 = 0.47 BTC
- Capped at 0.2 BTC per risk rules. Actual risk = 0.2 × $640 = $128

**Trade progression:**
- Hour 24: BTC at $65,900. Trail stop to $65,900 - $640 = $65,260
- Hour 30: BTC at $66,800. Trail stop to $66,800 - $640 = $66,160
- Hour 36: BTC at $67,500. Trail stop to $67,500 - $640 = $66,860
- Hour 40: BTC pulls back to $66,700. Trailing stop at $66,860 hit.

**Result:**
- Entry: $65,420, Exit: $66,860
- Profit: 0.2 × ($66,860 - $65,420) = $288
- R-multiple: $288 / $128 = 2.25R

### Strategy Specification

```
STRATEGY: Momentum Breakout
MARKET: BTC-USD-PERP
TIMEFRAME: 1h candles for signals

ENTRY RULES:
- Long: Close above 20-period high + next candle confirms above level
- Short: Close below 20-period low + next candle confirms below level
- Volume filter: > 1.5x 20-period average volume on breakout candle
- Entry type: Market order on confirmation candle close
- Position size: Risk $300 per trade (size = $300 / (2 × ATR))

EXIT RULES:
- Take profit: None (let winners run)
- Stop loss: 2.0 × ATR(14) from entry
- Time stop: None
- Trailing stop: 2.0 × ATR(14) from highest close since entry

RISK PARAMETERS:
- Max position size: $15,000 notional
- Max loss per trade: $300
- Max concurrent positions: 2
- Max daily loss: $600 then halt

FILTERS:
- Only trade when: ATR(14) > ATR(50) — volatility expanding
- Only trade when: Spread < 0.1% of price
- Avoid when: Inside a well-defined range (no trend)
```

---

## 4. Grid Trading

### Overview

Place buy and sell orders at regular price intervals within a defined range, profiting
from price oscillation. Each buy has a paired sell (and vice versa), capturing small
profits on each oscillation.

### Grid Spacing Formulas

```
grid_range    = upper_bound - lower_bound
grid_spacing  = grid_range / num_levels
capital_per_level = total_allocated_capital / num_levels
size_per_level = capital_per_level / level_price
```

### Grid Design Parameters

| Parameter | Conservative | Standard | Aggressive |
|---|---|---|---|
| Number of levels | 5-8 | 10-15 | 20-30 |
| Grid spacing (% of range) | 2-4% | 1-2% | 0.3-1% |
| Take-profit per grid | 1 grid step | 1 grid step | 1 grid step |
| Capital allocation | 30% of equity | 50% of equity | 70% of equity |
| Range width | ~10% of price | ~15% of price | ~20% of price |

### Example Grid for BTC-USD-PERP

**Assumptions:**
- BTC trading range: $62,000 - $68,000 (from 2-week kline analysis)
- Allocated capital: $10,000
- Grid levels: 10
- Grid spacing: ($68,000 - $62,000) / 10 = $600

**Grid Setup:**

| Level | Price | Order Type | Size (BTC) | Notional |
|---|---|---|---|---|
| 1 | $62,000 | Buy | 0.016 | $1,000 |
| 2 | $62,600 | Buy | 0.016 | $1,000 |
| 3 | $63,200 | Buy | 0.016 | $1,000 |
| 4 | $63,800 | Buy | 0.016 | $1,000 |
| 5 | $64,400 | Buy | 0.016 | $1,000 |
| 6 | $65,000 | Sell | 0.015 | $1,000 |
| 7 | $65,600 | Sell | 0.015 | $1,000 |
| 8 | $66,200 | Sell | 0.015 | $1,000 |
| 9 | $66,800 | Sell | 0.015 | $1,000 |
| 10 | $67,400 | Sell | 0.015 | $1,000 |

**Paired take-profits:** Each buy at level N has a sell TP at level N+1 ($600 higher).
Each sell at level N has a buy TP at level N-1 ($600 lower).

**Expected profit per grid fill:**
- Profit per round trip: $600 × 0.016 BTC = $9.60
- After fees (0.03% taker × 2): $9.60 - ($1,000 × 0.0006) = $9.60 - $0.60 = $9.00
- If price oscillates filling 3 grids/day: ~$27/day

**Risk scenario — range breakout:**
- If BTC drops below $62,000: all buy orders filled, holding 0.08 BTC in loss
  Max grid loss at $60,000: 0.08 × ($63,700 avg - $60,000) = $296
- If BTC rises above $68,000: all sell orders filled, missed upside

### Strategy Specification

```
STRATEGY: Grid Trading
MARKET: BTC-USD-PERP
TIMEFRAME: N/A (always-on within range)

ENTRY RULES:
- Define range from 2-week high/low with 5% buffer
- Place buy limits from lower_bound to midpoint
- Place sell limits from midpoint to upper_bound
- Grid spacing: range / num_levels

EXIT RULES:
- Take profit: Each grid order has paired TP one grid step away
- Stop loss: Close all if price breaks 3% beyond range boundary
- Time stop: Re-evaluate range weekly
- Trailing stop: N/A

RISK PARAMETERS:
- Max capital in grid: 50% of equity
- Max loss per grid cycle: N/A (individual fills are small)
- Max concurrent orders: num_levels × 2
- Max daily loss: If cumulative loss > 5% of grid capital, halt and re-evaluate range

FILTERS:
- Only trade when: ADX(14) < 25 (non-trending market)
- Only trade when: Range has held for at least 1 week
- Avoid when: Approaching major support/resistance on higher timeframe
```

---

## 5. Basis Trading

### Overview

Exploit the price difference (basis) between perpetual futures and the underlying spot
price. When the perp trades at a premium, short the perp and buy spot. When the perp
trades at a discount, long the perp and sell spot.

### Basis Calculation

```
basis         = perp_mark_price - underlying_price
basis_pct     = (basis / underlying_price) × 100%
annualized_basis = basis_pct × (365 / expected_convergence_days)
```

### Entry and Exit Thresholds

| Parameter | Conservative | Moderate | Aggressive |
|---|---|---|---|
| Entry basis (annualized) | > 25% | > 15% | > 8% |
| Exit basis (annualized) | < 5% | < 3% | < 0% (converged) |
| Max holding period | 14 days | 30 days | 60 days |
| Position size per leg | 5% of equity | 10% of equity | 15% of equity |
| Max basis widening tolerance | +50% of entry basis | +100% | +200% |

### Hedging Mechanics

**Premium trade (perp > spot):**
1. Short perp at mark_price (receives funding if rate positive)
2. Buy equivalent spot amount
3. Net delta ≈ 0
4. Profit = basis convergence + funding income - trading costs

**Discount trade (perp < spot):**
1. Long perp at mark_price (pays funding if rate positive)
2. Sell equivalent spot amount
3. Net delta ≈ 0
4. Profit = basis convergence - funding cost - trading costs

### Example Trade

**Scenario:** BTC perp mark = $65,500, BTC spot underlying = $65,200

1. **Basis:** $65,500 - $65,200 = $300 (0.46%)
2. **Annualized (assume 7-day convergence):** 0.46% × (365/7) = 24.0%
3. **Entry (premium trade):**
   - Short 0.1 BTC-USD-PERP at $65,500 (notional $6,550)
   - Buy 0.1 BTC spot at $65,200 (cost $6,520)
4. **Funding income:** If 8h rate = 0.01%, daily = $6,550 × 0.0003 = $1.97
5. **After 5 days:** Basis converges to $50 (0.08%)
   - Close short at $65,250: profit = 0.1 × ($65,500 - $65,250) = $25
   - Sell spot at $65,200: breakeven on spot (price unchanged for simplicity)
   - Funding collected: $1.97 × 5 = $9.85
   - **Total profit: $25 + $9.85 = $34.85**
   - **Annualized return on capital deployed: ~39%**

### Risk Factors

- Basis can widen before converging — mark-to-market losses on the perp leg
- Execution risk: both legs should be entered simultaneously
- Funding rates can flip — turning income into cost
- Spot leg requires actual token purchase (capital-intensive)
- Basis convergence timing is uncertain

### Strategy Specification

```
STRATEGY: Basis Trading
MARKET: BTC-USD-PERP + BTC spot
TIMEFRAME: Daily monitoring

ENTRY RULES:
- Condition 1: Annualized basis > 15%
- Condition 2: Basis has been positive for 3+ consecutive days (persistent)
- Entry type: Market orders on both legs simultaneously
- Position size: 10% of equity per leg

EXIT RULES:
- Take profit: Basis < 3% annualized
- Stop loss: Basis widens to 2x entry level
- Time stop: 30 days max hold
- Trailing stop: N/A

RISK PARAMETERS:
- Max position size: 10% of equity per leg (20% total capital)
- Max loss per trade: Basis widening to 2x entry = ~0.5% of notional
- Max concurrent positions: 2 basis pairs
- Max daily loss: N/A (delta neutral, P&L is slow-moving)

FILTERS:
- Only trade when: Funding rate aligns with basis direction
- Avoid when: High volatility periods (basis unstable)
- Avoid when: Low spot liquidity
```

---

## 6. Blank Strategy Template

Copy this template to design a custom strategy from scratch.

```
STRATEGY: [Name — descriptive, e.g., "BTC Range Scalper"]
MARKET: [market_id, e.g., BTC-USD-PERP]
TIMEFRAME: [signal resolution, e.g., 1h candles]

THESIS:
[1-2 sentences: What market behavior does this exploit? Why should it work?]

ENTRY RULES:
- Condition 1: [specific, measurable — e.g., "RSI(14) < 30 on 4h chart"]
- Condition 2: [additional confirmation — e.g., "Volume > 1.5x 20-period average"]
- Condition 3: [optional — e.g., "Price within 1% of support level"]
- Entry type: [market / limit] at [price logic, e.g., "limit at lower BB"]
- Position size: [sizing rule, e.g., "Risk $200 per trade, size = $200 / stop_distance"]

EXIT RULES:
- Take profit: [condition or price level — e.g., "Middle Bollinger Band"]
- Stop loss: [condition or price level — e.g., "1.5 ATR below entry"]
- Time stop: [max holding period — e.g., "Close after 48h if no TP/SL"]
- Trailing stop: [if applicable — e.g., "2 ATR from highest close since entry"]

RISK PARAMETERS:
- Max position size: [in base currency and/or USD notional]
- Max loss per trade: [dollar or percentage of equity]
- Max concurrent positions: [number]
- Max daily loss: [dollar or percentage, then halt trading]

FILTERS:
- Only trade when: [market regime, volatility, volume, spread conditions]
- Avoid when: [conditions that invalidate the edge]

HISTORICAL CHECK:
- Lookback period: [e.g., "30 days of 1h klines"]
- Signals generated: [count from paradex_klines data]
- Estimated win rate: [% of signals where TP hit before SL]
- Average winner / loser: [dollar amounts]
- Estimated total P&L: [gross, then net after fees]

EXECUTION NOTES:
- Fee impact: [estimated cost per round trip]
- Spread impact: [current spread vs. expected profit per trade]
- Slippage estimate: [from orderbook depth analysis]
- Min order size: [from paradex_markets]
- Price increment: [tick size from paradex_markets]
```
