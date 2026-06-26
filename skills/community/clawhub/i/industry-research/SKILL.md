---
name: industry-research
description: "When the user wants to conduct industry research, keyword research for a campaign, search demand analysis, intent mapping, audience research, or understand what people are searching for. Also use when the user mentions 'industry research,' 'keyword clusters,' 'search intent,' 'what are people looking for,' 'audience questions,' 'content gaps,' 'competitor keywords,' 'SERP analysis,' or 'research before campaign.' This skill orchestrates multi-tool deep research using Ahrefs, Firecrawl, and Exa to produce a comprehensive intelligence brief. For raw web scraping, see firecrawl-cli; for competitor analysis, see competitive-intelligence; for market sizing, see market-research."
metadata:
  version: 1.0.0
---

# Industry Research

You conduct deep, intent-driven industry research. The core question is "what are people looking for?" -- not "what are competitors doing?" Keyword intent, search demand, and real audience language are the primary signals. Competitor analysis serves the intent research by finding gaps in what's being served.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Then determine:

1. **Client name** -- Which client to research for
2. **Industry/market** -- The market category and key services/products
3. **Seed keywords** -- 5-8 starting keyword phrases reflecting core services
4. **Competitor URLs** -- 3-5 known competitor websites to analyze
5. **Geographic focus** -- Target region for keyword data (default: US)

If dispatched via cron or orchestrator with a specific client name, use the product-marketing-context for that client to derive seed keywords and competitors automatically.

---

## Workflow

### Step 1: Keyword Research (Ahrefs)

Use Ahrefs to gather keyword data. Try the Ahrefs MCP server first (if available via mcporter or MCP tools list). If MCP is not available, fall back to the Ahrefs REST API at `https://api.ahrefs.com/v3` with `Authorization: Bearer $AHREFS_API_KEY`.

Regardless of access method, gather data from these endpoints/capabilities:

**Keywords Explorer overview** -- seed keywords (batch up to 10 per request) for volume, difficulty, traffic potential:
```
POST /keywords-explorer/overview
Body: { "keywords": ["seed1", "seed2", ...], "country": "us" }
```

**Keywords Explorer matching terms** -- for each seed keyword, find related keywords (limit: 100 results per seed):
```
POST /keywords-explorer/matching-terms
Body: { "keyword": "seed keyword", "country": "us", "limit": 100 }
```

**Keywords Explorer related terms** -- semantically similar keywords:
```
POST /keywords-explorer/related-terms
Body: { "keyword": "seed keyword", "country": "us", "limit": 100 }
```

Cluster results by topic (group keywords sharing the same parent topic or SERP overlap).

Classify each keyword's intent:
- **Informational** -- how/what/why questions, guides, educational content
- **Transactional** -- near me, cost, buy, hire, service, pricing queries

**Rate limit:** Max 60 requests/min. **Budget cap:** 15 API calls per research run.

**If neither Ahrefs MCP nor AHREFS_API_KEY is available**, skip this step and note "Ahrefs data unavailable -- no MCP server or API key configured" in the artifact. Continue with Firecrawl+Exa only.

### Step 2: Audience Research (Firecrawl + Exa)

Use `exa.js search` to find Reddit threads, forum posts, Quora answers about the industry/problem space:

```bash
exa.js search "[industry] questions problems reddit" --num-results 10
```

```bash
exa.js search "[industry] advice forum" --num-results 10
```

```bash
exa.js search "site:reddit.com [service] experience" --num-results 10
```

Use `firecrawl.js scrape` to extract content from top 5 most relevant results:

```bash
firecrawl.js scrape --url "https://reddit.com/r/relevant-thread"
```

Extract:
- Exact questions people ask
- Pain points in their own words
- Emotional language
- Common objections

Cross-reference with Google's People Also Ask (search for each seed keyword via Exa and extract PAA-style questions):

```bash
exa.js search "[seed keyword] questions people also ask" --num-results 5
```

### Step 3: Content Gap Analysis

For each top keyword cluster, use `exa.js search` to find what currently ranks:

```bash
exa.js search "[keyword]" --num-results 10
```

Use `firecrawl.js scrape` on top 3 ranking pages per cluster to analyze content depth:

```bash
firecrawl.js scrape --url "https://top-ranking-page.com/article"
```

Identify gaps:
- Topics with search demand but weak/missing/outdated content from competitors
- Flag underserved angles -- queries where top results are generic directories (Yelp, WebMD) rather than authoritative guides
- Note city-specific opportunities if geographic focus applies

### Step 4: Competitor Landscape

Use `firecrawl.js map` on each competitor URL to discover their site structure:

```bash
firecrawl.js map --url "https://competitor.com"
```

Use `firecrawl.js scrape` on their key pages (homepage, services, blog, pricing) -- max 5 pages per competitor:

```bash
firecrawl.js scrape --url "https://competitor.com/services"
```

Analyze:
- Positioning/messaging
- Content strategy (blog frequency, topics)
- SEO approach (city pages, programmatic content)

If Ahrefs is available (MCP or API), use Site Explorer organic-keywords to see what keywords competitors rank for:
```
GET /site-explorer/organic-keywords?target=competitor.com&limit=50
```

Identify messaging patterns and gaps -- what positioning angles are unclaimed.

### Step 5: Compile Artifact

Write the output to `.agents/industry-research-{client}.md` where `{client}` is the lowercase client name (e.g., `allcare`).

Use this artifact template:

```markdown
# Industry Research: {Client Name}

*Client: {Client Full Name}*
*Last full refresh: YYYY-MM-DD*

## 1. Keyword Clusters & Intent Map

*Last researched: YYYY-MM-DD*

### Cluster: {Topic Name}
| Keyword | Monthly Volume | Difficulty | Intent | Traffic Potential |
|---------|---------------|------------|--------|-------------------|
| keyword phrase | X,XXX | XX | Informational/Transactional | X,XXX |

**Intent distribution:** X% informational, X% transactional
**Primary opportunities:** Summary of top keyword opportunities

## 2. Questions & Pain Points

*Last researched: YYYY-MM-DD*

### What people ask (from PAA, Reddit, forums)
- "Exact question from audience?" (volume: X,XXX)

### Pain points (exact audience language)
- "Verbatim quote from real person" -- Source (Reddit, forum, etc.)

## 3. Content Gaps & Opportunities

*Last researched: YYYY-MM-DD*

### Underserved angles
- **Gap description:** Why it matters and the opportunity

### What's ranking (and what's weak)
| Query | Top Result | Gap/Opportunity |
|-------|-----------|-----------------|
| search query | Current top result | What's missing or weak |

## 4. Competitor Landscape

*Last researched: YYYY-MM-DD*

### Who ranks for our keywords
| Competitor | Ranks For | Positioning | Content Strategy |
|-----------|-----------|-------------|------------------|
| Competitor name | Key keywords | How they position | Blog, city pages, etc. |

### Messaging patterns
- Competitor: "Their messaging angle" -- framing type
- **Gap:** Unclaimed positioning angle
```

**Target artifact size:** 3,000-5,000 words. Synthesize and distill -- do not dump raw scraped content.

Each section has its own `Last researched:` timestamp so consuming skills can verify recency.

---

## Tips

- Focus on intent, not just volume -- a 500-volume transactional keyword outperforms a 5,000-volume informational one for conversions
- Capture exact audience language -- "my mom can barely get to the doctor" is more valuable than "transportation barriers to healthcare access"
- Budget API calls carefully -- 15 Ahrefs calls per run, scrape selectively (use `firecrawl.js map` before `scrape`)
- Keep the artifact scannable -- downstream skills read specific sections, not the whole document

---

## Related Skills

- **competitive-intelligence** -- For detailed competitor analysis (company-level deep dives)
- **market-research** -- For market sizing, TAM/SAM/SOM, and industry trends
- **firecrawl-cli** -- For raw Firecrawl scraping (detailed tool documentation)
- **exa-company-research** -- For raw Exa web search on specific companies
- **product-marketing-context** -- For foundational product/service context that feeds into research
