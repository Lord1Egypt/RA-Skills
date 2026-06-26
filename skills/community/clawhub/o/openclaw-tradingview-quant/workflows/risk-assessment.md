---
description: Risk assessment workflow - Position management and risk control recommendations
---

# Risk Assessment Workflow

Professional position management and risk control recommendation system. For detailed risk management methodology, see `references/risk-management.md`.

## Execution Steps

### Step 1: Get Historical K-line Data

Get sufficiently long daily data for volatility calculation:

```python
tradingview_get_price(symbol, timeframe='D', range=250)  # Approximately 1 year daily data
```

### Step 2: Get Real-time Quotes

```python
tradingview_get_quote(symbol, session='regular')
```

Extract: Current price, 52-week high/low, volume, bid/ask.

### Step 3: Get Technical Indicators

```python
tradingview_get_ta(symbol, include_indicators=true)
```

Key indicators for stop loss calculation:
- **Pivot Points**: Support/resistance levels (S1/S2/S3, R1/R2/R3)
- **SMA/EMA**: Moving average support (SMA20/50/200)
- **ATR**: Average True Range (for dynamic stop loss)
- **Beta**: Relative market volatility (for position adjustment)

### Step 4: Calculate Volatility

Based on daily data calculation:
- **Daily return standard deviation** = std(daily change percentage)
- **Annualized volatility** = Daily std × √252
- **Maximum drawdown** = max(historical peak to trough drawdown)
- **Beta coefficient**: Reference Beta value in TA indicators

### Step 5: Calculate Position Recommendations

Based on user's total capital and risk preference (see `references/risk-management.md`):

**Kelly Formula**:
```python
f = (bp - q) / b
where: b=odds, p=win rate, q=1-p
Recommend using half Kelly (f/2) for more conservative approach
```

**Volatility-adjusted Position Sizing**:
```python
Recommended position % = Target daily volatility / Instrument daily volatility
Example: Target daily volatility 2%, instrument daily volatility 4% → Max position 50%
```

**Staggered Entry Recommendations**:
- First position: 30-40% of total position
- Add position 1: Add 30% after trend confirmation
- Add position 2: Add another 30% after breaking key levels

### Step 6: Calculate Stop Loss and Take Profit

**Stop Loss Calculation** (choose the most reasonable one):
- ATR stop: Current price - 2×ATR
- MA stop: Below recent moving average support (SMA20 or SMA50)
- Pivot stop: Below S1 or S2
- Pattern stop: Below pattern low

**Take Profit Calculation**:
- ATR target: Current price + 3×ATR
- Pivot target: R1, R2, R3
- Measured target: Calculate based on pattern height

**Risk-Reward Ratio**: Must be > 1.5, ideally > 2.0

### Step 7: Generate Risk Management Plan

```markdown
# [Instrument] Risk Assessment Report

## Volatility Analysis
- Annualized volatility: XX%
- Recent 20-day average daily range: XX%
- Beta coefficient: XX
- Maximum drawdown: XX%

## Position Recommendations (Based on total capital ¥XX ten thousand)
- Recommended total position: XX% (¥XX)
- Maximum single trade: ¥XX
- Staggered entry plan:
  - First position ¥XX @ ¥XX (current price)
  - Add position 1 ¥XX @ ¥XX (condition: XX confirmation)
  - Add position 2 ¥XX @ ¥XX (condition: break above XX)

## Stop Loss and Take Profit Plan
- Stop loss price: ¥XX (XX% below current)
  - Method: [ATR/MA/Pivot]
- Take profit target 1: ¥XX (+XX%)
- Take profit target 2: ¥XX (+XX%)
- Risk-reward ratio: 1:X.X

## Maximum Loss Estimation
- Maximum loss per trade: ¥XX (XX% of total capital)
- Recommend single trade risk not exceeding 2% of total capital

## Risk Warnings
- [Volatility risk/Liquidity risk/Event risk etc.]
```

## Example

**User**: "I have 100k capital, want to buy Puyuan Information, how much should I buy?"

**Execution**:
1. `search_market(query='普元信息')` → SSE:688118
2. `get_price(symbol='SSE:688118', timeframe='D', range=250)` → Daily K-lines
3. `get_quote(symbol='SSE:688118')` → Real-time price
4. `get_ta(symbol='SSE:688118', include_indicators=true)` → Technical indicators
5. Calculate volatility → Kelly formula → Position recommendations
6. Calculate stop loss/take profit levels → Risk-reward ratio
7. Generate complete risk management plan, stop loss/take profit strategy, risk-reward ratio plan.
