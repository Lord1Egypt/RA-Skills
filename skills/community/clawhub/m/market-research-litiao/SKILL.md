---
name: market-research-litiao
slug: market-research
description: "Size markets, analyze competitors, and validate opportunities with practical frameworks and free data sources. Uses Tavily API (preferred) for research."
metadata: {"clawdbot":{"emoji":"📊","requires":{"env":["TAVILY_API_KEY"]}}}
---

## Core Framework

**Before any research:** Clarify the question. "How big is the market?" is useless. "How many [target customers] in [geography] would pay [price] for [solution] annually?" is actionable.

## Data Collection with Tavily

**Preferred: Use Tavily Search** for comprehensive market research:

```bash
cd ~/.openclaw/workspace/skills/tavily-search-litiao

# Market size and trends
node scripts/search.mjs "[industry] market size growth rate 2024 2025" --deep -n 15

# Competitor analysis
node scripts/search.mjs "[competitor name] revenue market share funding" -n 10

# Customer insights
node scripts/search.mjs "[target audience] pain points buying behavior" -n 10

# Industry reports
node scripts/search.mjs "[industry] report analysis trends forecast" --deep -n 10

# Recent news
node scripts/search.mjs "[industry] news developments" --topic news --days 30 -n 15
```

**Tavily advantages for market research:**
- `--deep` mode for comprehensive industry reports
- Cleaner data extraction from financial sources
- Better clustering of competitor information
- Time-filtered news for recent market developments

## Market Sizing

| Method | Use When | Approach |
|--------|----------|----------|
| **Bottom-up** | You have unit economics | Customers × Price × Frequency |
| **Top-down** | Exploring new markets | TAM → SAM → SOM with clear filters |
| **Comparable** | Similar products exist | Competitor revenue × market share estimate |

**Free data sources:** Government census, industry associations, public company filings (10-K), Statista free tier, Google Trends, LinkedIn Sales Navigator (company counts), **Tavily Search** (aggregates multiple sources).

**Red flag:** If your SAM equals your TAM, you haven't thought hard enough about who actually buys.

## Competitor Analysis

1. **Map the landscape:** Direct, indirect, potential entrants
2. **Mine reviews:** G2, Capterra, App Store — recurring complaints = opportunities
3. **Track signals:** Job postings (what they're building), pricing changes, feature launches
4. **Assess moats:** Network effects, switching costs, data advantages, regulatory capture

For detailed competitor frameworks, see `competitor-analysis.md`.

## Customer Validation

**Before building:** Talk to 20+ potential customers. Use Jobs-to-be-Done or Mom Test frameworks.

**Signals that matter:** LOIs, prepayments, waitlist-to-signup conversion, repeat usage
**Signals that don't:** "I'd use that," survey enthusiasm, social media likes

For interview scripts and survey templates, see `validation.md`.

## Common Traps

- **Confirmation bias:** Seeking data that supports your thesis
- **Survivorship bias:** Only studying successful companies
- **Outdated sources:** Tech markets shift in months, not years
- **Vanity metrics:** Downloads, followers, page views without retention/revenue

## Boundaries

- **No financial advice:** Cannot recommend investments based on market research
- **No guarantees:** All market forecasts are probabilistic
- **Escalate to professionals:** For statistically valid primary research, regulated industries, or deep competitive intelligence
