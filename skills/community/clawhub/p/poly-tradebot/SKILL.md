---
name: poly-tradebot
description: Automated news analysis pipeline that fetches CNBC world news, classifies articles by topic (geopolitics vs macroeconomics), and invokes specialized skills (geopolitics-expert or the-fed-agent) to produce structured trading analysis. Use when you need systematic news-to-trading-signal workflow for Iran war, US economy, Fed policy, and market impact assessment.
---

# Poly Tradebot

## Overview

Poly-tradebot automates the news-to-trading-analysis workflow: fetches CNBC world news, filters by relevant tags (us, iran, war, market, the fed), classifies each article as geopolitics or macroeconomics, invokes the appropriate specialized skill (geopolitics-expert or the-fed-agent), discovers related Polymarket markets, and produces a unified trading analysis table with market data and expert recommendations.

## Workflow

### 1. Fetch CNBC World News

```
poly-tradebot fetch
```

Fetches articles from `https://www.cnbc.com/world/?region=world` using `web_fetch` tool. Extracts at least 3 articles matching tags: `us`, `iran`, `war`, `market`, `the fed`.

**Article Selection Criteria:**
- Headline or content contains at least one tag keyword
- Published within last 24-48 hours (freshness)
- Substantive content (not brief mentions)

### 2. Classify Article Topic

For each fetched article, classify as:

| Topic | Classification Triggers | Skill to Invoke |
|-------|------------------------|-----------------|
| **Geopolitics** | Iran, war, military, conflict, sanctions, regime, IRGC, drone, missile, Strait of Hormuz, UAE, Middle East tensions | `geopolitics-expert` |
| **Macroeconomics** | Fed, Treasury yields, interest rates, inflation, central bank, CPI, employment, GDP, monetary policy, oil price (economic impact) | `the-fed-agent` |

### 3. Invoke Specialized Skill

**For Geopolitics Articles:**
```
geopolitics-expert <article_url>
```

Produces 5-section output:
1. Conclusion
2. Economic/Commodity Impact
3. Commodity Trading Odds
4. War Duration Categorization
5. Termination Scenarios

**For Macroeconomics Articles:**
```
the-fed-agent <article_url>
```

Produces 4-section output:
1. Conclusion
2. Economic/Commodity Impact
3. Commodity Trading Odds
4. What's Next Can Be Happened? (policy path scenarios)

### 4. Discover Polymarket Markets

For each analyzed article, search Polymarket for related prediction markets:

```
web_search query="<topic> Polymarket market" site:polymarket.com
web_fetch url=<polymarket_market_url> extractMode=markdown
```

Extract market metadata:
- Market Title
- Market URL
- Resolve Date
- Current Odds (Yes/No probabilities)
- **Trading Volume** (24h + total volume)

**Search Strategy:**
- Use article keywords (e.g., "Iran war", "Fed rate hike", "Oil prices")
- Filter to active/open markets
- **Volume Filter**: Only include markets with total volume > $1,000,000
- **Odds Filter**: Only include markets with Yes% probability < 70% (contrarian edge)
- **Minimum Markets**: Discover at least 10 qualifying markets across all articles
- Prioritize high-liquidity markets for reliable odds

### 5. Output Per News Article

Each article produces a standalone analysis file saved to `memory/`:
- Geopolitics: `memory/geopolitics-YYYY-MM-DD-cnbc-<topic>.md`
- Macroeconomics: `memory/macro-YYYY-MM-DD-cnbc-<topic>.md`

**Output Format:** Follows exact skill output format (geopolitics: 5 sections, macro: 4 sections) PLUS a unified trading table.

### 6. Unified Trading Table Output

After all articles are analyzed and Polymarket markets discovered, produce a summary table:

| Market Title | Market URL | Resolve Date | Market Odds | Volume | Recommendation | Reason |
|--------------|------------|--------------|-------------|--------|----------------|--------|
| <market name> | <polymarket URL> | <date> | <Yes%> | $<volume> | **YES** or **NO** | <expert reasoning> |

**Column Definitions:**
1. **Market Title**: Polymarket market name
2. **Market URL**: Direct link to the Polymarket market
3. **Resolve Date**: When the market resolves
4. **Market Odds**: Current Polymarket probability (Yes%)
5. **Volume**: Total trading volume (must be > $1,000,000)
6. **Recommendation**: Bold **YES** or **NO** based on expert analysis
7. **Reason**: Concise reasoning from geopolitics-expert or the-fed-agent (e.g., "75% forever war probability", "65% single 25bp cut only")

**Output Requirements:**
- **Minimum Markets**: At least 10 markets in the table
- **Volume Filter**: All markets must have total trading volume > $1,000,000
- **Odds Filter**: All markets must have Yes% probability < 70% (contrarian opportunities)

**Recommendation Logic:**
- **YES**: Expert analysis supports the market outcome (expert probability > 60%)
- **NO**: Expert analysis contradicts the market outcome (expert probability < 40%)
- Include the key probability and rationale from the expert skill output

## Usage Examples

### Example 1: Full Pipeline Run

```
poly-tradebot
```

Fetches 3+ CNBC articles, classifies each, invokes appropriate skills, discovers Polymarket markets, outputs unified trading table (Yes/No recommendations with expert reasoning).

### Example 2: Re-run Workflow

```
poly-tradebot fetch
```

Re-fetches fresh articles from CNBC world page, re-runs classification, analysis, and market discovery pipeline.

### Example 3: Analyze Specific URL

```
poly-tradebot analyze <url>
```

Classifies and analyzes a single article URL, discovers related Polymarket markets, outputs Yes/No recommendation with expert reasoning.

### Example 4: Output Table Only

```
poly-tradebot table
```

Regenerates the unified trading table from existing memory analyses without re-fetching articles.

## Output Summary

After pipeline completion, produces **ONLY** the Unified Trading Table:

| Market Title | Market URL | Resolve Date | Market Odds | Volume | Recommendation | Reason |
|--------------|------------|--------------|-------------|--------|----------------|--------|
| <market name> | <polymarket URL> | <date> | <Yes%> | $<volume> | **YES** or **NO** | <concise expert rationale> |

**Format Rules:**
- **Table only** — no headers, no commentary, no additional sections
- **Minimum Markets**: At least 10 markets in the table
- **Volume Filter**: All markets must have total trading volume > $1,000,000
- **Odds Filter**: All markets must have Yes% probability < 70% (contrarian opportunities)
- **Recommendation**: Bold **YES** or **NO** based on expert analysis probability
- **Reason**: Concise expert rationale (e.g., "75% forever war probability", "65% single 25bp cut only")
- **Market Odds**: Current Polymarket Yes% probability
- **Volume**: Display total trading volume (e.g., "$2.4M")
- Saved to `memory/poly-tradebot-table-YYYY-MM-DD.md`

## Skill Dependencies

- `geopolitics-expert` — Required for geopolitics articles
- `the-fed-agent` — Required for macroeconomics articles
- `web_fetch` — Built-in tool for article retrieval
- `web_search` — Built-in tool for Polymarket market discovery (optional)

## Resources

### references/
- `classification_rules.md` — Topic classification heuristics
- `output_templates.md` — Format templates per skill type (geopolitics: 5 sections, macro: 4 sections)

### scripts/
- `fetch_cnbc.py` — Article fetching and parsing utility
- `classify_topic.py` — Geopolitics vs macroeconomics classifier

---

**Skill Version:** 3.1  
**Created:** 2026-03-17  
**Updated:** 2026-03-18 (v3.1: odds filter <70% for contrarian edge; v3.0: minimum 10 markets, volume filter >$1M, added Volume column)  
**Author:** poly-tradebot skill creator
