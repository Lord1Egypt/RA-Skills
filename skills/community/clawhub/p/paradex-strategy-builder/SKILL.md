---
name: paradex-strategy-builder
description: >
  Design, backtest, and reason about trading strategies for Paradex using MCP tools.
  Takes natural language strategy descriptions and turns them into structured trading
  plans with entry/exit rules, position sizing, risk parameters, and historical
  validation using Paradex kline and trade data. Supports strategy templates for
  common approaches (funding arb, mean reversion, momentum, grid trading, basis trading).
  Use this skill whenever the user asks to build a trading strategy for Paradex, wants
  to backtest an idea, asks about "how would X strategy work on Paradex", wants to design
  entry/exit rules, asks about grid trading, funding arbitrage, mean reversion, momentum
  strategies, or any systematic trading approach on Paradex markets. Also trigger for
  "build me a bot", "trading plan", "strategy for BTC-USD-PERP", "backtest this idea",
  or "how would I trade [pattern] on Paradex".
---

# Paradex Strategy Builder

Translates trading ideas into structured, testable strategy specifications.
Uses Paradex MCP tools for historical data analysis and validation.

## Important Boundary

This skill produces **strategy designs and historical analysis** — it does NOT
execute trades. If the user wants to execute, point them to the Paradex MCP
order management tools (available when authenticated) or the paradex-py SDK.

## Available MCP Tools for Strategy Development

| Tool | Strategy use |
|---|---|
| `paradex_klines` | Historical price data for backtesting signals |
| `paradex_trades` | Trade flow analysis for entry timing |
| `paradex_orderbook` | Liquidity analysis for execution planning |
| `paradex_funding_data` | Funding rate history for carry strategies |
| `paradex_market_summaries` | Cross-market screening for opportunity detection |
| `paradex_markets` | Tick sizes, position limits, min order sizes for realistic sizing |
| `paradex_bbo` | Current spread for execution cost estimation |

## Strategy Design Process

### Step 1: Capture the Idea

Extract from the user's description:
- **Market(s)**: Which Paradex market(s)? Or cross-market?
- **Thesis**: What market behavior does this exploit?
- **Direction**: Long-only, short-only, or both?
- **Timeframe**: Scalping (minutes), intraday (hours), swing (days), carry (weeks)?
- **Edge source**: Technical (price patterns), structural (funding), statistical (mean reversion)?

If the user's description is vague, ask clarifying questions.
If they want a template, offer one from the catalog below.

### Step 2: Define Rules

Structure every strategy as:

```
STRATEGY: [Name]
MARKET: [market_id]
TIMEFRAME: [resolution for signals]

ENTRY RULES:
- Condition 1: [specific, measurable]
- Condition 2: [specific, measurable]
- Entry type: [market/limit] at [price logic]
- Position size: [sizing rule]

EXIT RULES:
- Take profit: [condition or price level]
- Stop loss: [condition or price level]
- Time stop: [max holding period if applicable]
- Trailing stop: [if applicable]

RISK PARAMETERS:
- Max position size: [in base currency and USD]
- Max loss per trade: [dollar or percentage]
- Max concurrent positions: [number]
- Max daily loss: [dollar or percentage, then halt]

FILTERS:
- Only trade when: [market regime, volume, spread conditions]
- Avoid when: [conditions that invalidate the edge]
```

### Step 3: Historical Validation

Use MCP data to check if the strategy would have worked:

1. **Fetch historical data**: `paradex_klines` for the relevant period and resolution
2. **Compute signals**: apply the entry/exit rules to historical data
3. **Count opportunities**: how many entry signals in the lookback period?
4. **Check market context**: were the conditions favorable? (volatility, volume, spreads)
5. **Estimate outcomes**: for each signal, what would P&L have been?

Note: This is NOT a rigorous backtest — it's a sanity check. True backtesting
requires accounting for fills, slippage, fees, and execution timing that we
can't precisely simulate from kline data alone.

**What to report:**
- Number of signals generated in lookback period
- Win rate (% of signals where take-profit would have hit before stop-loss)
- Average winner size vs. average loser size
- Maximum consecutive losses
- Estimated total P&L (gross, before fees/slippage)
- Fee impact estimate (from trader profile rates)
- Realistic P&L estimate (after estimated fees and slippage)

### Step 4: Execution Planning

Using `paradex_markets` and `paradex_orderbook`:

- **Position sizing**: respect min_notional, order_size_increment, max_order_size
- **Spread cost**: current spread as % of expected profit per trade
- **Slippage estimate**: from orderbook depth vs. intended order size
- **Fee impact**: retail (zero for retail profile) vs. pro rates
- **Price bands**: ensure limit prices stay within price_bands_width of mark price

## Strategy Templates

### Template 1: Funding Rate Arbitrage

**Thesis**: Collect funding payments by taking the opposite side of crowded positions.

**Implementation:**
1. Scan all markets via `paradex_market_summaries` for extreme funding rates
2. Enter a position opposite to the funding direction (if funding is positive, go short to receive)
3. Hedge directional risk (if desired) via correlated asset or options
4. Exit when funding normalizes or trade becomes unprofitable

**Key data:**
- `paradex_funding_data`: historical funding to check if rates are mean-reverting
- `paradex_market_summaries`: current rates across all markets for screening
- 8h funding rate × 3 = daily rate × 365 = annualized rate

**Risk factors:**
- Funding rates can reverse quickly — you pay what you were collecting
- Directional exposure means price moves can overwhelm funding income
- Works best in ranging markets with persistent funding imbalance

### Template 2: Mean Reversion

**Thesis**: Prices tend to revert to a mean after overextension.

**Implementation:**
1. Calculate Bollinger Bands (20-period, 2σ) from klines
2. Enter long when price touches lower band + RSI < 30
3. Enter short when price touches upper band + RSI > 70
4. Target: middle band (20-period SMA)
5. Stop: 1.5 ATR beyond entry

**Key data:**
- `paradex_klines`: compute bands, RSI, ATR
- `paradex_orderbook`: check liquidity at entry/exit levels

**Risk factors:**
- Trending markets destroy mean reversion — use regime filter
- Requires tight stops which get hit frequently in volatile markets

### Template 3: Momentum / Trend Following

**Thesis**: Strong moves tend to continue.

**Implementation:**
1. Detect breakout: price closes above 20-period high with volume > 1.5x average
2. Enter on breakout confirmation (2 consecutive closes above level)
3. Trail stop: 2 ATR below highest close since entry
4. No fixed take-profit — let winners run, trail protects

**Key data:**
- `paradex_klines`: price highs, volume
- `paradex_trades`: confirm volume spike is real trades, not wash

**Risk factors:**
- Many false breakouts in ranging markets
- Requires patience — low win rate, large winners

### Template 4: Grid Trading

**Thesis**: Profit from price oscillation within a range.

**Implementation:**
1. Define range: support at $X, resistance at $Y (from kline analysis)
2. Place buy orders at N evenly spaced levels from support to midpoint
3. Place sell orders at N evenly spaced levels from midpoint to resistance
4. Each buy has a corresponding sell (take-profit) a grid step higher
5. Each sell has a corresponding buy (take-profit) a grid step lower

**Key data:**
- `paradex_klines`: identify the range bounds
- `paradex_markets`: min_notional and tick_size for grid spacing
- `paradex_orderbook`: ensure grid levels have liquidity

**Risk factors:**
- Range breakouts cause significant losses on one side
- Capital-intensive — funds spread across many open orders
- Best for ranging, low-volatility periods

### Template 5: Basis Trading (Spot vs. Perp)

**Thesis**: Exploit price differences between spot and perpetual markets.

**Implementation:**
1. Monitor basis: perp_price - underlying_price (from market_summaries)
2. When basis is high (perp premium): short perp, long spot equivalent
3. When basis is low (perp discount): long perp, short spot equivalent
4. Collect funding while basis normalizes

**Key data:**
- `paradex_market_summaries`: mark_price vs underlying_price
- `paradex_funding_data`: funding rate trend
- Requires spot market access (Paradex supports spot trading)

**Risk factors:**
- Basis can widen before converging
- Execution risk: need to enter both legs simultaneously

## Output Format

### Strategy Specification
```
## Strategy: [Name]
### Thesis
[1-2 sentences: what market behavior does this exploit?]

### Rules
[Structured entry/exit/risk rules as above]

### Historical Check
[Results from validation using MCP data]

### Execution Notes
[Practical considerations: fees, sizing, spread costs]

### Risk Summary
- Max expected loss per trade: $X
- Win rate estimate: X%
- Key risk: [biggest thing that can go wrong]
- Kill condition: [when to abandon the strategy entirely]
```

## Caveats

- Historical validation from kline data is NOT a proper backtest — it doesn't account
  for execution quality, fills, queue priority, or concurrent position effects
- All P&L estimates are gross approximations — actual results depend on execution
- Strategy edge can decay — what worked historically may not work going forward
- Paradex retail traders get zero fees, but pro/API traders pay maker/taker fees
  that can significantly impact high-frequency strategies
- This skill designs strategies, not financial advice. Users trade at their own risk.
- For actual execution, the user needs to use the authenticated MCP order tools or
  build a bot using the paradex-py SDK

See [templates.md](references/templates.md) for expanded strategy templates with parameter ranges and example calculations.
