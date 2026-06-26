---
description: Multi-Symbol Batch Analysis Workflow - Batch analyze technical and quote data for multiple symbols
---

# Multi-Symbol Batch Analysis Workflow

Batch analyze technical analysis, quote data for multiple symbols, perform horizontal comparison and comprehensive evaluation.

## Execution Steps

### Step 1: Collect Symbol List

Extract list of symbols to analyze from user input:
- Support up to 10 symbols for simultaneous analysis
- Symbol format: EXCHANGE:SYMBOL (e.g., NASDAQ:AAPL)

### Step 2: Batch Get Real-time Quotes

Call `tradingview_get_quote_batch` to get real-time quotes for all symbols:

```
Parameter description:
- symbols: Array of symbols (1-10)
- session: Trading session (default: regular)
- fields: Return fields (default: all)
```

### Step 3: Batch Get Historical Charts

Call `tradingview_get_price_batch` to get historical data for all symbols:

```
Parameter description:
- requests: Request array (each contains symbol, timeframe, range)
- Maximum 10 requests
```

### Step 4: Get Technical Analysis Individually

For each symbol, call `tradingview_get_ta` to get technical analysis signals:
- Aggregate buy/sell/neutral signals
- Calculate comprehensive technical score

### Step 5: Horizontal Comparison Analysis

Compare key metrics across symbols:
- **Price change comparison**: Who gained/lost the most
- **Trading activity**: Who has the highest volume
- **Technical signal comparison**: Who has the strongest technicals
- **Volatility comparison**: Who has the highest volatility

### Step 6: Generate Comparison Report

Output comprehensive comparison report:
- Quote comparison table
- Technical score ranking
- Investment value ranking
- Risk-reward ratio comparison
- Recommended priority symbols

## Example Conversations

**User**: "Compare and analyze AAPL, MSFT, GOOGL stocks"

**Execution**:
1. Call `tradingview_get_quote_batch` to get real-time quotes
2. Call `tradingview_get_price_batch` to get daily chart data
3. Call `tradingview_get_ta` individually to get technical analysis
4. Generate comparison table, highlighting best performers for each metric

---

**User**: "Batch analyze tech leader stocks"

**Execution**:
1. Confirm tech leader list (AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA, etc.)
2. Batch get quotes and technical analysis
3. Sort by price change and technical score
4. Recommend symbols with strongest technicals

---

**User**: "Compare BTC and ETH technicals"

**Execution**:
1. Call `tradingview_get_quote_batch`, symbols=["BINANCE:BTCUSDT", "BINANCE:ETHUSDT"]
2. Call `tradingview_get_price_batch` to get historical charts
3. Get technical analysis signals individually
4. Compare trend strength and overbought/oversold conditions
