---
name: plusefin-analysis
description: >
  Financial data research via PlusE API. Provides stock fundamentals,
  options analysis, market sentiment (Fear & Greed), institutional
  holdings, insider trades, financial statements, macroeconomic data
  (FRED), ML price predictions, and market news.
  Use when user asks about: stock analysis, ticker research, options
  trading, options Greeks, implied volatility, market sentiment, Fear
  & Greed index, earnings reports, financial statements (income/
  balance/cash flow), insider trading, institutional holders, 13F,
  GDP, inflation, CPI, unemployment, interest rates, macroeconomics,
  CNBC news, Reddit stock discussions, or price prediction forecast.
metadata:
  openclaw:
    emoji: "📈"
    homepage: "https://github.com/plusefin/plusefin-skill"
    requires:
      bins: [python3]
      env: [PLUSEFIN_API_KEY]
    primaryEnv: PLUSEFIN_API_KEY
---

# PlusE Financial Analysis

AI-ready financial data research skill. All data is ML-preprocessed and
token-optimized for direct AI consumption — no raw JSON parsing needed.

## Setup

```bash
export PLUSEFIN_API_KEY=your_api_key
```

Get a free API key at [console.plusefin.com](https://console.plusefin.com).

## Usage

There are three ways to access PlusE data. Use whichever your agent supports.

### Option A: MCP (Claude Code / OpenCode)

If the PlusE MCP server is connected, call tools directly. MCP server URL:

```
https://mcp.plusefin.com/mcp/?apikey=$PLUSEFIN_API_KEY
```

Each tool is listed in the Data Reference below with its MCP tool name.
Call tools like: `get_ticker_data("AAPL")`

### Option B: CLI (Any agent — recommended fallback)

```bash
python plusefin.py <command> [args]
```

The `plusefin.py` script is bundled with this skill directory.

### Option C: curl (Any agent)

```bash
curl -s -H "Authorization: Bearer $PLUSEFIN_API_KEY" \
  "https://mcp.plusefin.com/api/tools/<endpoint>"
```

## Data Reference

### 📊 Company Fundamentals

| Data | MCP Tool | CLI Command | curl Endpoint |
|------|----------|-------------|---------------|
| Overview, valuation, ratings | `get_ticker_data("AAPL")` | `python plusefin.py ticker AAPL` | `/tools/ticker/AAPL` |
| Price history + TA indicators | `get_price_history("AAPL", "1y")` | `python plusefin.py price-history AAPL 1y` | `/tools/price-history?ticker=AAPL&period=1y` |
| Financial statements | `get_financial_statements("AAPL", "income", "annual")` | `python plusefin.py statements AAPL income` | `/tools/statements/AAPL?type=income&frequency=annual` |
| Earnings history | `get_earnings_history("AAPL")` | `python plusefin.py earnings AAPL` | `/tools/earnings/AAPL` |
| Stock news | `get_ticker_news_tool("AAPL")` | `python plusefin.py news AAPL` | `/tools/news/AAPL` |

### 📈 Options

| Data | MCP Tool | CLI Command | curl Endpoint |
|------|----------|-------------|---------------|
| Options analysis (Greeks, IV, OI) | `super_option_tool("TSLA")` | `python plusefin.py options-analyze TSLA` | `/tools/options/analyze/TSLA` |
| Options chain | — | `python plusefin.py options TSLA 20` | `/tools/options/TSLA?num_options=20` |

### 🏛️ Institutional Activity

| Data | MCP Tool | CLI Command | curl Endpoint |
|------|----------|-------------|---------------|
| Top 25 institutional holders | `get_top25_holders("AAPL")` | `python plusefin.py top25 AAPL` | `/tools/top25/AAPL` |
| Insider trades | `get_insider_trades("AAPL")` | `python plusefin.py insiders AAPL` | `/tools/insiders/AAPL` |
| Institutional holders | `(same as top25)` | `python plusefin.py holders AAPL` | `/tools/holders/AAPL` |

### 😱 Market Sentiment

| Data | MCP Tool | CLI Command | curl Endpoint |
|------|----------|-------------|---------------|
| Fear & Greed, VIX, market breadth | `get_overall_sentiment_tool()` | `python plusefin.py sentiment` | `/tools/sentiment` |
| Historical Fear & Greed | — | `python plusefin.py sentiment-history 30` | `/tools/sentiment/history?days=30` |
| Sentiment trend analysis | — | `python plusefin.py sentiment-trend 30` | `/tools/sentiment/trend?days=30` |
| CNBC market news | `cnbc_news_feed()` | `python plusefin.py news-market` | `/tools/news/market` |
| Reddit discussions | `social_media_feed(["AAPL","TSLA"])` | `python plusefin.py news-social AAPL` | `/tools/news/social?keywords=AAPL` |

### 🌍 Macroeconomic Data (FRED)

| Data | MCP Tool | CLI Command | curl Endpoint |
|------|----------|-------------|---------------|
| FRED series by ID | `get_fred_series("GDP")` | `python plusefin.py fred GDP` | `/tools/fred/GDP` |
| Search FRED series | `search_fred_series("CPI")` | `python plusefin.py fred-search CPI` | `/tools/fred/search?q=CPI` |

Common FRED series IDs: `GDP` (GDP), `CPIAUCSL` (CPI), `UNRATE` (unemployment), `FEDFUNDS` (interest rate), `DGS10` (10Y Treasury), `SP500` (S&P 500), `T10YIE` (10Y breakeven inflation).

### 🔮 Price Prediction

| Data | MCP Tool | CLI Command | curl Endpoint |
|------|----------|-------------|---------------|
| ML price forecast + probability | `price_prediction("AAPL")` | `python plusefin.py prediction AAPL` | `/tools/prediction/AAPL` |

### 🧮 Calculator

| Data | MCP Tool |
|------|----------|
| Execute Python expressions | `calculate("2 + 2")` |

No CLI/curl equivalent needed. Use the `calculate` tool directly in MCP-native agents.

### ⏰ Time

| Data | MCP Tool |
|------|----------|
| Current time (ISO 8601) | `get_current_time()` |

## Research Workflows

### Workflow 1: Stock Deep Dive

When user asks "analyze AAPL" or "what do you think about TSLA":

```
1. Fundamentals    → ticker(symbol)           → overview, valuation, ratings
2. Technicals      → price-history(symbol, 1y) → price data + TA indicators
3. Sentiment check → sentiment()               → Fear & Greed, VIX
4. Institution     → top25(symbol)             → who holds it, recent changes
5. Options market  → options-analyze(symbol)   → IV, Greeks, OI
6. Macro context   → fred(GDP), fred(UNRATE)   → economic backdrop
7. Synthesize into structured report with bull/base/bear cases
```

### Workflow 2: Earnings Preparation

When user asks "earnings coming up for MSFT" or "what to expect from NVDA earnings":

```
1. Past earnings   → earnings(symbol)          → surprise history, trend
2. Recent news     → news(symbol)              → developments, catalysts
3. Options market  → options-analyze(symbol)    → IV crush, expected move
4. Social buzz     → news-social(symbol)        → retail sentiment
5. ML forecast     → prediction(symbol)         → probability of decline
6. Summarize expectations with key levels to watch
```

### Workflow 3: Market Pulse

When user asks "how's the market looking today":

```
1. Fear & Greed    → sentiment()                → overall market mood
2. Market news     → news-market()              → CNBC headlines
3. Social pulse    → news-social("market,economy,stocks") → Reddit sentiment
4. Key indicators  → fred(DGS10), fred(FEDFUNDS), fred(T10YIE)
5. Quick summary of risk-on/risk-off environment
```

### Workflow 4: Macroeconomic Context

When user asks "what's the macro picture" or "how's the economy":

```
1. GDP             → fred(GDP)                   → economic growth
2. Inflation       → fred(CPIAUCSL)              → CPI trend
3. Employment      → fred(UNRATE)                → unemployment
4. Rates           → fred(FEDFUNDS), fred(DGS10) → monetary policy
5. Markets         → fred(SP500)                 → market level context
6. Synthesize macro regime and implications for equities
```

### Workflow 5: Options Strategy Research

When user asks "analyze options for AAPL" or "find options opportunities":

```
1. Options analysis → options-analyze(symbol)   → full Greeks, IV, OI
2. Options chain    → options(symbol, 20)       → specific strikes/expiry
3. Price context    → price-history(symbol, 6mo) → recent price action
4. Sentiment check  → sentiment()                → market mood alignment
5. Report: IV rank, put/call skew, key strikes, implied move
```

## Analysis Framework

When producing a research report, structure output with these sections:

### Core Thesis
- Direction: bullish / bearish / neutral
- Key drivers: valuation, earnings growth, catalyst, sentiment reversal
- Confidence level and time horizon

### Evidence Summary
- Cite specific data points from tools used (fundamentals, technicals, options, sentiment)
- Note conflicting signals if any

### Valuation Scenarios
- **Bull case**: upside catalysts, target valuation, key levels
- **Base case**: expected outcome under current conditions
- **Bear case**: downside risks, key levels to watch
- Assign probability weights to each scenario

### Risk Assessment
- Company-specific risks
- Macro/industry risks
- Key assumptions that, if wrong, change the thesis

### Actionable Recommendation
- Directional view with conviction level
- Suggested position sizing guidance
- Key levels and triggers to monitor
