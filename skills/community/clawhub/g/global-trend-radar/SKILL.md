---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_10c7befb5d0711f1abc85254006c9bbf
    ReservedCode1: 2OfMfKlBmLlt9kSjzELiThSr4n04lVRjTgPzOzciCleT6F2hF4pVmSc665eQASAlclw84EdBFn37o0T5hmuPUAMZKyIL3XQhCGoZi5sRTXsO77A/c0kaPiWo47g8s95d7knUeCWsFj9D/56/4hL45FPGV8I3tCkwlU9yqRZL6B+x6j8jau0v7zkLuVg=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_10c7befb5d0711f1abc85254006c9bbf
    ReservedCode2: 2OfMfKlBmLlt9kSjzELiThSr4n04lVRjTgPzOzciCleT6F2hF4pVmSc665eQASAlclw84EdBFn37o0T5hmuPUAMZKyIL3XQhCGoZi5sRTXsO77A/c0kaPiWo47g8s95d7knUeCWsFj9D/56/4hL45FPGV8I3tCkwlU9yqRZL6B+x6j8jau0v7zkLuVg=
---

# Global Trend Radar (鍏ㄧ悆瓒嬪娍闆疯揪)

## Description
A comprehensive trend intelligence skill that monitors, analyzes, and synthesizes emerging global trends across technology, economics, geopolitics, climate, demographics, and innovation. Powered by multi-source web intelligence and structured trend taxonomy, it provides forward-looking analysis with actionable insights for decision-makers, researchers, and strategists worldwide.

**Keywords**: trends, global, forecasting, technology, innovation, market intelligence, future, megatrends, horizon scanning

## Triggers
- "what are the latest trends in [domain]"
- "analyze global [industry/sector] trends"
- "is [technology] trending worldwide"
- "compare trends between [region A] and [region B]"
- "what megatrends will shape the next [N] years"
- "emerging technologies to watch in [year]"
- "global market forecast for [sector]"

## Capabilities

### 1. Trend Discovery & Monitoring
- Execute multi-source web searches across 10+ authoritative trend data sources (Google Trends, Gartner, WIPO, WEF, OECD, McKinsey, Pew Research, arXiv, CB Insights, Statista)
- Track 8 persistent trend categories: AI & Automation, Climate & Sustainability, Digital Transformation, Biotech & Health, Geopolitics & Economics, Future of Work, Space & Deep Tech, Global Demographics
- Perform cross-regional trend comparison (US, EU, China, India, SE Asia, MENA, LATAM)
- Detect early signals via patent data analysis (WIPO PatentScope) and academic preprint surges (arXiv)

### 2. Trend Analysis Framework
- **Hype Cycle Assessment**: Map technologies to Gartner-style maturity phases (Innovation Trigger 鈫?Peak of Inflated Expectations 鈫?Trough of Disillusionment 鈫?Slope of Enlightenment 鈫?Plateau of Productivity)
- **Adoption S-Curve**: Estimate current adoption phase and trajectory for any trend
- **Impact 脳 Probability Matrix**: Score trends on potential impact (economic, social, environmental) vs. realization probability
- **Cross-Domain Ripple Analysis**: Identify second-order effects where trends in one domain cascade into others

### 3. Output Formats
Always structure trend reports with:
1. **Executive Summary** (3-5 bullet points)
2. **Trend Landscape** (categorized table with urgency/impact scores)
3. **Deep Dives** (2-3 most significant trends with evidence, data points, and timeline)
4. **Regional Comparison** (heatmap table: US vs EU vs APAC)
5. **Actionable Implications** (for businesses, policymakers, individuals)
6. **Monitoring Dashboard** (key metrics and indicators to watch going forward)

### 4. Data-Driven Requirements
- Cite at least 3 distinct sources per trend (URLs + publication dates required)
- Include quantitative data points where available (market size, growth rate, adoption %)
- Note conflicting viewpoints and uncertainties explicitly
- Distinguish between consensus trends and speculative projections
- Flag data freshness: mark sources older than 6 months as potentially stale

## Workflow

```
User Query
    鈫?[Step 1] Identify trend category & regions from structured taxonomy
    鈫?[Step 2] Execute parallel web_search across 3-5 relevant data sources
    鈫?[Step 3] Execute web_fetch on top 2-3 most promising results for depth
    鈫?[Step 4] Cross-reference findings: compare data points, identify consensus
    鈫?[Step 5] Apply analysis frameworks (Hype Cycle, S-Curve, Impact Matrix)
    鈫?[Step 6] Generate structured report with citations, tables, and visual indicators
    鈫?Final Output: Formatted report + monitoring recommendations
```

## Usage Guidelines
1. **Default scope**: When user doesn't specify timeframe, default to 1-3 year outlook
2. **Default regions**: When user doesn't specify region, cover global + regional highlights
3. **Confidence levels**: Always self-assess confidence (HIGH: multiple corroborating sources, MEDIUM: 2 sources aligned, LOW: single source or speculative)
4. **Language**: Match response language to user's query language; support multi-language trend searches using keyword translations from references/data_sources.json
5. **Persistence**: This skill tracks long-cycle trends (5-20 year horizons); avoid chasing viral fads

## Examples

**Query**: "What are the top AI trends shaping the next 3 years globally?"

**Response Structure**:
1. Executive Summary with top 5 AI trends ranked by impact
2. Trend Landscape table with columns: Trend | Maturity Phase | Impact Score | Adoption Velocity | Key Players
3. Deep Dive on #1 trend: Multi-modal AI / AI Agents - market data, patent surge, key papers
4. Regional comparison: US (foundation models, venture funding) vs EU (regulation-first, industrial AI) vs China (application layer, manufacturing AI)
5. Actionable implications for software companies, enterprises, and regulators
6. Metrics to watch: GPU shipments, AI patent filings, AI regulation milestones

## References
- `references/data_sources.json`: Complete data source catalog with URLs, coverage regions, and keyword mappings for 10 authoritative sources across 8 trend categories
*锛堝唴瀹圭敱AI鐢熸垚锛屼粎渚涘弬鑰冿級*
