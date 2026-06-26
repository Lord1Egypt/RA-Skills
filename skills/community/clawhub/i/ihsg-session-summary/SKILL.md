---
name: ihsg-session-summary
description: IHSG Closing Summary Agent untuk OpenClaw. Menghasilkan laporan sesi pagi dan closing dengan Top 10 Net Buy/Sell, Foreign Flow, YTD data, dan insights dalam Bahasa Indonesia. Menggunakan Tavily API untuk web search dan extract. Gunakan skill ini untuk cron job ringkasan pasar saham Indonesia (IHSG) dua kali sehari.
license: MIT
---

# IHSG Session Closing Summary - OpenClaw Skill

## Metadata
- Name: `ihsg_session_summary`
- Version: 4.0.1
- Description: IDX session closing summary with narrative market analysis using Tavily API
- Author: IHSG Agent
- Tags: finance, stocks, indonesia, market-analysis, idx, tavily

---

## Schedule

| Session | Trading Hours | Closing | Agent Run | Cron |
|---------|---------------|---------|-----------|------|
| **Session 1 (Morning)** | 09:00 - 11:30 | 11:30 WIB | **12:30 WIB** | `30 12 * * 1-5` |
| **Session 2 (Closing)** | 13:30 - 16:00 | 16:00 WIB | **16:30 WIB** | `30 16 * * 1-5` |

---

## When to Use

Use this skill when:
- Cron trigger for session closing (12:30 or 16:30 WIB)
- User requests session/market summary for today
- User wants to know top net buy/sell with price change

---

## Data Requirements

### Session 1 (Morning) - 12:30 WIB
- IHSG: current, open, high, low, change %
- Top 10 Net Buy: code, value, volume, price change %
- Top 10 Net Sell: code, value, volume, price change %
- Foreign Flow: buy, sell, net
- **Insights: SHORT** - focus on what's actionable for Session 2

### Session 2 (Closing) - 16:30 WIB
- All data from Session 1, plus:
- YTD Foreign Flow
- Domestic Flow
- Market Breadth: advancing, declining (if available)
- **Insights: FULL** - comprehensive analysis with outlook for tomorrow

---

## Data Sources

### Primary Sources

1. **IHSG Index Data**
   - Source: Yahoo Finance API
   - URL: `https://query1.finance.yahoo.com/v8/finance/chart/%5EJKSE`
   - Data: current, open, high, low, previous close, change %

2. **Top 10 Net Buy/Sell** (via Tavily Search)
   - API: Tavily Search API
   - Query: `"top 10 net buy sell saham Indonesia hari ini"`
   - Query: `"top foreign net buy sell IDX today"`
   - Sources to look for: kontan.co.id, investing.com, idx.co.id, stockbit.com

3. **Foreign Flow Data** (via Tavily Search + Extract)
   - Search Query: `"net foreign flow Bursa Efek Indonesia hari ini"`
   - Extract from: Kontan, Kompas, CNBC Indonesia

4. **YTD Foreign Flow** (via Tavily Search)
   - Query: `"YTD foreign flow Indonesia stock exchange"`
   - Query: `"akumulasi dana asing BEI tahun ini"`

5. **Stock Price Changes** (via Tavily Extract)
   - Extract from: Yahoo Finance, Investing.com for individual stocks

---

## Environment Variables Required

Set the `TAVILY_API_KEY` environment variable with your Tavily API key.

Get your API key from: https://app.tavily.com

---

## Instructions

### Step 1: Run Extraction Script

```bash
cd ~/.openclaw/skills/ihsg-session-summary/scripts
python3 ihsg_session_extractor.py [morning|closing]
```

### Step 2: Use Tavily API for Missing Data

The script will indicate missing data. Use Tavily to fill gaps:

**Tavily Search** - For finding information:
```python
from tavily import TavilyClient
import os

client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

# Search for top net buy/sell
response = client.search(
    query="top 10 net buy sell saham Indonesia hari ini",
    search_depth="advanced",
    max_results=10,
    include_raw_content=True
)

# Search for foreign flow
response = client.search(
    query="net foreign flow Bursa Efek Indonesia hari ini miliar",
    search_depth="advanced",
    max_results=10
)
```

**Tavily Extract** - For extracting content from URLs:
```python
# Extract content from financial news sites
response = client.extract(
    urls=["https://investasi.kontan.co.id/news/..."],
    extract_depth="advanced"
)
```

### Step 3: Generate Complete Output

Format output in **PLAIN TEXT** with ASCII tables.

**IMPORTANT**: Output must be in **Bahasa Indonesia** (Indonesian language)

### Step 4: Write Insights

Generate insights in Bahasa Indonesia:
- **Morning**: 1 paragraph, 2-3 sentences, actionable for Session 2
- **Closing**: 2-3 paragraphs, comprehensive with outlook

---

## Tavily API Usage Examples

### Search for Top Net Buy/Sell

```python
from tavily import TavilyClient
import os
import json

client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

# Search queries for different data
queries = [
    "top 10 net buy sell saham Indonesia hari ini 2026",
    "top foreign net buy sell IDX Indonesia today",
    "net foreign flow Bursa Efek Indonesia hari ini miliar",
    "YTD foreign flow Indonesia stock exchange 2026",
    "akumulasi dana asing BEI tahun ini"
]

all_results = []
for query in queries:
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=10,
        include_raw_content=True
    )
    all_results.extend(response.get('results', []))
```

### Extract from Financial News

```python
# Extract detailed content from URLs found in search
urls_to_extract = [
    "https://investasi.kontan.co.id/news/...",
    "https://money.kompas.com/read/...",
    "https://www.cnbcindonesia.com/market/..."
]

extracted = client.extract(
    urls=urls_to_extract,
    extract_depth="advanced"
)

for item in extracted.get('results', []):
    content = item.get('raw_content', '')
    # Parse content for stock data
```

### Extract Stock Price Changes

```python
# Get price changes for specific stocks
stock_codes = ["GOTO", "BUMI", "BMRI", "BBRI", "BBCA"]

for code in stock_codes:
    response = client.search(
        query=f"{code} stock price change Indonesia today",
        search_depth="basic",
        max_results=5
    )
    # Parse response for price change %
```

---

## Output Format

### SESSION 1 (Morning) - 12:30 WIB

```
📊 IHSG PAGI SUMMARY
[Hari, Tanggal dalam Bahasa Indonesia]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[🟢/🔴] IHSG: [nilai] ([+/-]X.XX%)
Open: [nilai] | High: [nilai] | Low: [nilai]
Prev Close: [nilai]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 TOP 10 NET BUY (by Value)
┌────┬────────┬────────────┬───────────┬──────────┐
│ No │ Kode   │ Net Value  │ Net Vol   │ Chg %    │
├────┼────────┼────────────┼───────────┼──────────┤
│  1 │ BBCA   │ IDR 125.5B │ 45.2M     │ +1.25%   │
│  2 │ TLKM   │ IDR 98.3B  │ 125.8M    │ +0.85%   │
... (10 stocks)
└────┴────────┴────────────┴───────────┴──────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📉 TOP 10 NET SELL (by Value)
┌────┬────────┬────────────┬───────────┬──────────┐
│ No │ Kode   │ Net Value  │ Net Vol   │ Chg %    │
├────┼────────┼────────────┼───────────┼──────────┤
│  1 │ GOTO   │ IDR 85.5B  │ 180.5M    │ -2.35%   │
... (10 stocks)
└────┴────────┴────────────┴───────────┴──────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 FOREIGN FLOW

Foreign:
• Buy:  IDR [X,XXX.X]B
• Sell: IDR [X,XXX.X]B
• Net:  IDR [+/-XXX.X]B [📈INFLOW/📉OUTFLOW]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 INSIGHTS SESI PAGI

[ONE SHORT PARAGRAPH - 2-3 sentences max]
[Focus: What happened + What to watch in Session 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Session: PAGI | Generated: [HH:MM] WIB
Data Source: Tavily API
```

---

### SESSION 2 (Closing) - 16:30 WIB

```
📊 IHSG CLOSING SUMMARY
[Hari, Tanggal dalam Bahasa Indonesia]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[🟢/🔴] IHSG: [nilai] ([+/-]X.XX%)
Open: [nilai] | High: [nilai] | Low: [nilai]
Prev Close: [nilai]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 TOP 10 NET BUY (by Value)
... (same format)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📉 TOP 10 NET SELL (by Value)
... (same format)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 FOREIGN vs DOMESTIC FLOW

Foreign:
• Buy:  IDR 8,250.5B
• Sell: IDR 8,500.2B
• Net:  IDR -249.7B 📉 OUTFLOW

Domestic:
• Net:  IDR +249.7B

YTD Foreign: IDR +2,459.7B

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 INSIGHTS CLOSING

[2-3 PARAGRAPHS - Full analysis]
[Paragraph 1: Full day summary + what happened]
[Paragraph 2: Connect the dots - patterns, rotation, themes]
[Paragraph 3: Outlook for tomorrow + actionable recommendations]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Session: CLOSING | Generated: [HH:MM] WIB
Data Source: Tavily API
```

---

## 🎯 Insights Writing Guidelines

### SESSION 1 (Morning) - SHORT & ACTIONABLE

**Length:** 1 paragraph, 2-3 sentences max

**Focus:**
1. Brief summary of what happened in morning session
2. What to watch/do in Session 2

---

### SESSION 2 (Closing) - FULL & COMPREHENSIVE

**Length:** 2-3 paragraphs

**Structure:**

**Paragraph 1: The Big Picture**
- Full day summary (open to close)
- Sentiment and overall market behavior
- Connect IHSG movement with foreign flow

**Paragraph 2: Connecting the Dots**
- Interesting patterns from top net buy/sell
- Sector rotation? Flight to quality? Profit taking?
- Why certain stocks accumulated/sold?

**Paragraph 3: Outlook & Actionable**
- What might happen tomorrow
- Important levels to watch
- Specific recommendations

---

## Rules

1. **10 STOCKS** for each top net buy/sell - use Tavily Search if needed
2. **PRICE CHANGE %** must be included for each stock - use Tavily Extract
3. Output in **PLAIN TEXT** with ASCII table
4. **Bahasa Indonesia** for all output and insights
5. **Session 1: SHORT insights** (1 paragraph, 2-3 sentences)
6. **Session 2: FULL insights** (2-3 paragraphs, comprehensive)
7. **Connect the dots** - link data, find patterns
8. **Use Tavily API** for all web data - search, extract, crawl
9. **Never leave data incomplete** - always fill via Tavily

---

## Jobs Configuration

```json
{
  "jobs": [
    {
      "name": "ihsg_session_morning",
      "schedule": { "kind": "cron", "expr": "30 12 * * 1-5" },
      "timezone": "Asia/Jakarta",
      "prompt": "Use skill ihsg_session_summary to create MORNING session summary. Run extraction script first, then use Tavily API (search & extract) to fill any missing data. Generate SHORT insights (1 paragraph) in Bahasa Indonesia.",
      "enabled": true
    },
    {
      "name": "ihsg_session_closing",
      "schedule": { "kind": "cron", "expr": "30 16 * * 1-5" },
      "timezone": "Asia/Jakarta",
      "prompt": "Use skill ihsg_session_summary to create CLOSING session summary. Run extraction script first, then use Tavily API (search & extract) to fill any missing data (Top 10, Foreign Flow, YTD, Price Changes). Generate FULL insights (2-3 paragraphs) in Bahasa Indonesia.",
      "enabled": true
    }
  ]
}
```

---

## File Structure

```
~/.openclaw/
├── skills/
│   └── ihsg-session-summary/
│       ├── SKILL.md
│       └── scripts/
│           ├── ihsg_session_extractor.py
│           └── requirements.txt
└── cron/
    └── jobs.json
```

---

## Installation

```bash
# 1. Create skill directory
mkdir -p ~/.openclaw/skills/ihsg-session-summary/scripts

# 2. Copy files
cp SKILL.md ~/.openclaw/skills/ihsg-session-summary/
cp ihsg_session_extractor.py ~/.openclaw/skills/ihsg-session-summary/scripts/
cp requirements.txt ~/.openclaw/skills/ihsg-session-summary/scripts/

# 3. Install dependencies
cd ~/.openclaw/skills/ihsg-session-summary/scripts
pip install -r requirements.txt

# 4. Set Tavily API key (use your actual key)
# On Linux/Mac: export TAVILY_API_KEY="your-key"
# On Windows: set TAVILY_API_KEY=your-key

# 5. Test
python3 ihsg_session_extractor.py morning
python3 ihsg_session_extractor.py closing
```

---

## Dependencies

- Python 3.8+
- requests
- beautifulsoup4
- tavily-python (Tavily SDK)
- Tavily API key (get from https://app.tavily.com)

---

## Tavily API Pricing

| Plan | Searches/month | Price |
|------|---------------|-------|
| Free | 1,000 | $0 |
| Pro | 10,000 | $29/mo |
| Enterprise | Unlimited | Custom |

For IHSG session summaries (2x daily on weekdays):
- ~40-50 searches per month
- Free tier is sufficient for testing
- Pro recommended for production
