---
name: market-open-watch
description: Get pre-market updates and news for Hong Kong stocks and US stocks. Provides structured briefings including market overview, key events, potential impacts, watchlists, and sources.
homepage: https://clawhub.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "tools": ["web_search"] },
        "description": "Retrieve and analyze pre-market information for HK and US stock markets",
      },
  }
---

# Market Open Watch

Get real-time pre-market updates for Hong Kong and US stock markets with structured reports.

## When to Use

✅ **USE this skill when:**

- "How's the pre-market look for HK stocks?"
- "What's driving US futures this morning?"
- "Any major news impacting the markets before open?"
- "Pre-market briefing brief"
- "What stocks should I watch today?"
- "Get me the pre-market outlook"

## When NOT to Use

❌ **DON'T use this skill when:**

- Historical market data → use financial databases
- Real-time trading data → use broker APIs
- Company fundamental analysis → use financial reports
- Portfolio management → use portfolio tools
- Technical analysis charts → use charting tools

## How It Works

This skill uses web_search to:
1. **Find** latest pre-market news and data from multiple sources
2. **Analyze** key events and potential impacts
3. **Structure** into a clear, organized briefing
4. **Include** sources for transparency

## Command Usage

### HK Pre-Market Briefing
```bash
# HK stock briefing
./market-open-watch/main.sh --market hk
```

### US Pre-Market Briefing
```bash
# US stock briefing  
./market-open-watch/main.sh --market us
```

### Combined Briefing
```bash
# Both markets combined
./market-open-watch/main.sh --market both
```

## Briefing Structure

Each briefing includes these sections:

### 1. Market Overview
- Current trends
- Index direction
- Trading sentiment
- Futures performance

### 2. Key Events
- Major news headlines
- Economic data releases
- Central bank announcements
- Corporate news

### 3. Potential Impact
- How events may affect specific sectors
- Expected volatility
- Catalysts to monitor

### 4. Watchlist/Topics
- Key individual stocks
- Industry themes
- Trading ideas

### 5. Sources
- News outlets
- Financial indices
- Data providers

## Notes

- Uses public web sources via web_search
- Updates as market news develops
- Time-sensitive information (best morning of trading days)
