---
name: News Sentiment Analyst
version: 1.0.3
description: "Aggregate and classify financial news sentiment into Risk-On / Risk-Off signals for market and individual stocks using the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/news-sentiment-analyst
---

# News Sentiment Analyst

Aggregate and analyze financial news and market sentiment using the Finskills API
news endpoints. Extract actionable signals from headlines, classify sentiment by
ticker and sector, and surface market-moving catalysts — so you can react to
information before it's fully priced in.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Asks "what's happening in the market today?"
- Wants to check sentiment for a specific stock before trading
- Asks about recent news for a company or sector
- Wants to understand why a stock moved (news catalyst identification)
- Asks to summarize financial media themes or narratives

---

## Data Retrieval — Finskills API Calls

### 1. General Financial News Feed
```
GET https://finskills.net/v1/free/news/finance
```
Extract: title, summary, source, published timestamp, sentiment score (if provided), tickers mentioned

### 2. Latest News (Pro — broader coverage)
```
GET https://finskills.net/v1/news/latest
```
Extract: same fields as above, with more sources and more recent latency

### 3. Symbol-Specific News
```
GET https://finskills.net/v1/news/by-symbol/{SYMBOL}
```
Extract: news articles filtered to a specific stock — title, summary, sentiment, source, timestamp

---

## Analysis Workflow

### Step 1 — News Aggregation

Collect and deduplicate articles across sources. Sort by:
1. Recency (most recent first)
2. Estimated impact (market-moving stories: Fed decisions, earnings, M&A, macro data)

**Source trust tiers:**
- Tier 1 (high authority): Reuters, Bloomberg, WSJ, FT, CNBC
- Tier 2 (solid): MarketWatch, Barron's, Seeking Alpha (News), Yahoo Finance
- Tier 3 (background): General blogs, press releases

### Step 2 — Market-Wide Sentiment Classification

For each article, classify:

| Signal | Bearish | Neutral | Bullish |
|--------|---------|---------|---------|
| **Fed/Policy** | Rate hike surprise, hawkish tone | Policy hold expected | Rate cut, dovish language |
| **Earnings** | Miss + lowered guidance | Beat, maintained guidance | Beat + raised guidance |
| **Economic Data** | Weak jobs, poor PMI | Mixed data | Strong GDP, low unemployment |
| **Geopolitics** | New conflicts, trade war | Ongoing tensions | Peace/trade deal |
| **M&A** | Deal collapse, hostile bid | Rumored deals | Friendly acquisition at premium |
| **Macro** | Recession signals | Soft landing narrative | Growth acceleration |

Assign an overall **Market Sentiment Score** for the day:
- 🟢 **Risk-On**: Majority of market-moving news is bullish
- 🟡 **Mixed**: Conflicting signals across sectors
- 🔴 **Risk-Off**: Majority bearish, defensive positioning

### Step 3 — Ticker/Sector Sentiment Map

Group articles by stocks/sectors mentioned:
- For each ticker mentioned 2+ times: assign net sentiment (positive/negative/neutral)
- Identify sectors with bullish news clusters (potential sector momentum)
- Identify sectors with bearish news clusters (potential sector rotation out)

### Step 4 — Catalyst Identification

Flag high-impact event types:
- 🔴 **Earnings**: Beat/miss/guidance change
- 🔴 **Merger/Acquisition**: Target premium, integration cost
- 🔴 **FDA/Regulatory**: Drug approval, regulatory violation
- 🔴 **Management change**: CEO/CFO departure or appointment
- 🟡 **Analyst action**: Upgrade, downgrade, price target change
- 🟡 **Macro data**: CPI, NFP, GDP, FOMC minutes
- 🟡 **Insider activity**: Large insider buy/sell (link to insider-trade-tracker)
- 🟢 **Buyback announcement**: Often positive signal
- 🟢 **Contract win / Partnership**: Revenue catalyst

### Step 5 — Summary and Recommendations

Generate:
1. **3-bullet market summary** (most important macro/market stories)
2. **Top 3 bullish catalysts** (specific stocks/sectors)
3. **Top 3 bearish risks** (specific stocks/sectors)
4. **Sector rotation signal**: which sectors are in/out of favor today

---

## Output Format

```
╔══════════════════════════════════════════════════════╗
║     NEWS & SENTIMENT REPORT  —  {DATE} {TIME}       ║
╚══════════════════════════════════════════════════════╝

🌡️ OVERALL MARKET SENTIMENT: {RISK-ON / MIXED / RISK-OFF}
   Sources analyzed: {N}  |  Timeframe: Last {hours}h

📌 TOP MARKET THEMES
  1. {Most important market-moving story}
  2. {Second important story}
  3. {Third important story}

📈 BULLISH CATALYSTS
  🟢 {TICKER/SECTOR}: {headline}
     Source: {source} | Sentiment: Positive | Impact: {High/Medium/Low}
     Signal: {one-line interpretation}

  🟢 {TICKER/SECTOR}: {headline}
     ...

📉 BEARISH RISKS
  🔴 {TICKER/SECTOR}: {headline}
     Source: {source} | Sentiment: Negative | Impact: {High/Medium/Low}
     Signal: {one-line interpretation}

  🔴 {TICKER/SECTOR}: {headline}
     ...

🏭 SECTOR SENTIMENT MAP
  Sector          Sentiment   Key Driver
  Technology      🟢 Bullish  AI chip demand stories, NVDA + SMCI positive
  Energy          🔴 Bearish  Crude oil supply glut concerns
  Financials      🟡 Mixed    Rate cut hopes vs. credit risk headlines
  Healthcare      🟡 Neutral  No major catalysts today
  ...

🔍 STOCK-SPECIFIC NEWS
  [If user specified a ticker]
  {TICKER} — {N} stories in last 24h:
    {timestamp}: {headline} [{Positive/Negative/Neutral}]
    {timestamp}: {headline} [{sentiment}]
  Net Sentiment: {Positive/Mixed/Negative}

⚡ HIGH-IMPACT EVENTS TO WATCH
  • {Event 1} — scheduled {date/time}
  • {Event 2} — expected announcement
```

---

## Limitations

- News latency varies by source; some articles may be 15–60 minutes delayed.
- Sentiment classification is AI-assisted and may miss nuanced or sarcastic language.
- This skill surfaces information signals, not guaranteed trading signals.
- Always verify high-impact news with primary sources (company IR, official filings).
