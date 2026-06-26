---
description: Deep Stock Analysis Workflow - Comprehensive analysis of individual stocks using multiple tools
---

# Deep Stock Analysis Workflow

Combine multiple API data sources to perform comprehensive analysis on individual stocks, outputting integrated reports and trading recommendations.

## Execution Steps

### Step 1: Confirm Symbol

If user input is Chinese name/abbreviation, search to confirm accurate symbol:

```
tradingview_search_market(query="user input", filter="stock", lang="zh")
```

Confirm symbol format is `EXCHANGE:SYMBOL` (e.g., `SSE:688118`, `NASDAQ:AAPL`).

### Step 2: Get Real-time Quote

```
tradingview_get_quote(symbol, session="regular")
```

Extract key data:
- Current price, change %, volume, turnover
- Bid/ask price, bid/ask volume
- 52-week high/low, market cap

### Step 3: Get Multi-Timeframe Charts

Call in parallel to get data for different periods:

```
tradingview_get_price(symbol, timeframe='D', range=120)   # Daily - medium-term trend
tradingview_get_price(symbol, timeframe='W', range=52)    # Weekly - medium to long-term
tradingview_get_price(symbol, timeframe='60', range=100)  # 60-minute - short-term details
```

Optional: `type='HeikinAshi'` to get Heikin Ashi candles for clearer trend visualization.

### Step 4: Get Detailed Technical Analysis

```
tradingview_get_ta(symbol, include_indicators=true)
```

**Key Indicator Interpretation**:
- Multi-timeframe signal summary (1min/5min/15min/1hour/4hour/daily/weekly/monthly)
- RSI(14): >70 overbought, <30 oversold
- MACD: Golden cross/death cross, DIF relationship with zero line
- ADX(14): >25 trending, >50 strong trend
- Moving average alignment: SMA5/10/20/60 relative relationships

See `references/technical-analysis.md` for detailed scoring methodology.

### Step 5: Related News Analysis

**News Data Requirements**:
- Symbol-specific news (recent 5-10 items)
- News title, summary, and publication time
- Related symbols and tags

**Analysis Focus**:
- Major company announcements
- Earnings reports and guidance
- Industry developments
- Regulatory changes

For important news, analyze full content details for deeper context.

### Step 6: Upcoming Events Calendar

**Calendar Data Types**:
- Earnings releases (next 30 days)
- Dividend distributions
- Corporate actions
- Industry events

Check for upcoming events that may impact stock price.

### Step 7: Generate Comprehensive Report

Output structure:

```markdown
# [Stock Name] (Symbol) Deep Analysis

## Basic Information
- Current price / Change % / Volume
- Market cap / 52-week range

## Technical Analysis
- Multi-timeframe trend assessment (monthly/weekly/daily/hourly)
- Key indicator status (RSI, MACD, ADX, moving averages)
- Support levels / Resistance levels
- Overall technical score (0-100)

## Pattern Recognition
- Current pattern identification
- Confidence assessment

## News Analysis
- Recent important news summary
- Impact assessment

## Upcoming Events
- Earnings date / Dividend date

## Trading Recommendations
- Action direction (Buy/Hold/Sell)
- Suggested entry price
- Stop loss / Target price
- Position size recommendation
- Risk-reward ratio

## Risk Warnings
```

## Example

**User**: "Help me analyze Primeton"

**Execution**:
1. `search_market(query="普元信息", filter="stock")` → SSE:688118
2. `get_quote(symbol="SSE:688118")` → Real-time quote
3. `get_price` × 3 timeframes → Chart data
4. `get_ta(include_indicators=true)` → Detailed technical indicators
5. `get_news(symbol="SSE:688118", lang="zh-Hans")` → Related news
6. Comprehensive scoring, generate report
