---
name: keyword-optimize
description: Page-level keyword optimization using Ahrefs MCP data and GEO principles. Targets both traditional search (Google) and AI-powered search (ChatGPT, Perplexity, AI Overviews, Gemini, Claude). Invoke when optimizing any web page for search visibility.
version: 1.0.0
emoji: 🔑
homepage: https://github.com/antimoron/keyword-optimize
license: MIT
metadata:
  openclaw:
    requires:
      env:
        - name: AHREFS_API_KEY
          description: Ahrefs API key (Lite plan or higher)
          required: true
---

# SEO/GEO Page-Level Keyword Optimization Skill

## Overview

This skill drives page-level keyword optimization by combining Ahrefs MCP data with GEO (Generative Engine Optimization) principles. It targets both traditional search engines and AI-powered search (ChatGPT, Perplexity, Google AI Overviews, Claude, Gemini).

---

## Inputs Required

| Input | Source | Notes |
|-------|--------|-------|
| Target page URL | User | The specific page to optimize |
| Competitor URLs (3–5) | User or Ahrefs | Same search intent as target page |
| Primary keyword | User or derived | Main topic the page should rank for |
| Ahrefs MCP credentials | Environment | API key or MCP session |

---

## Workflow

### Phase 1 — Keyword Intelligence (Ahrefs MCP)

```
1. keywords_explorer(seed=primary_keyword)
   → Extract: volume, KD, CPC, related_terms, questions, parent_topic

2. site_explorer(url=competitor_url, mode="organic_keywords", limit=50)
   → Repeat for each competitor
   → Collect all keywords competitors rank for on this topic

3. content_gap(target=our_url, competitors=[url1, url2, ...], mode="page")
   → Output: keywords competitors rank for that our page does NOT cover
   → Filter by: volume > 100, KD < 60
```

**Deliverable**: A keyword matrix with three tiers:

| Tier | Type | Placement |
|------|------|-----------|
| Primary | Exact match, highest volume | Title, H1, meta desc, first 100 words |
| Secondary | Semantic cluster, related terms | H2/H3 headers, body paragraphs |
| Gap keywords | Missing vs. competitors | New sections, FAQ, supporting content |

---

### Phase 2 — On-Page Keyword Mapping

Map keywords to page structure following this hierarchy:

```
<title>          Primary keyword (≤60 chars)
<meta desc>      Primary + secondary keyword + CTA (≤155 chars)
<h1>             Primary keyword variant (natural language)
<h2> × N         One secondary keyword per sub-topic
First 100 words  Primary + 1 secondary keyword (natural, not forced)
Body             LSI / gap keywords distributed at ~1 per 200 words
<img alt>        Descriptive keyword-inclusive alt text
Internal links   Anchor text = target keyword of linked page
```

Rules:
- No keyword stuffing. Density is not a metric. Relevance and coverage are.
- Each H2 owns exactly one keyword intent. Do not blend intents in a single section.
- Internal link anchors must use the exact target keyword of the destination page.

---

### Phase 3 — GEO Layer (AI Search Citability)

This phase targets AI engines (ChatGPT, Perplexity, Gemini, AI Overviews).

**CITE Framework** (one application per major section):

```
C — Claim     : State the answer directly in the first sentence.
I — Insight   : Add a non-obvious detail or mechanism.
T — Trust     : Cite a source, statistic, or expert reference.
E — Evidence  : Back it up with data, example, or case.
```

**Structural requirements**:

1. **Opening definition block**: First 50 words must answer the primary keyword query in one authoritative sentence. This is what AI engines extract and cite.

2. **FAQ Schema**: Convert Ahrefs question-type keywords into FAQ markup.
   ```json
   {
     "@type": "FAQPage",
     "mainEntity": [
       {
         "@type": "Question",
         "name": "[keyword question from Ahrefs]",
         "acceptedAnswer": { "@type": "Answer", "text": "[CITE-structured answer]" }
       }
     ]
   }
   ```

3. **Table / List structures**: AI engines prefer extractable formats. Where the content allows, convert prose into a table or bulleted list with a clear header.

4. **Factual density**: Include at least 3 verifiable facts (statistics, dates, named entities) per 500 words. Vague content is not cited.

---

### Phase 4 — Monitoring (Ahrefs API)

```python
# Weekly page health check
results = ahrefs_api.get_organic_keywords(url=target_page, limit=100)

for kw in results:
    if kw["position"] > 10 and kw["volume"] > 200:
        trigger_reoptimize_alert(kw)

# Monthly content gap re-run
ahrefs_api.content_gap(target=our_url, competitors=competitor_list)
→ Flag any new gap keywords with volume > 300
```

Alert thresholds:
- Primary keyword drops below position 10 → immediate review
- Click share drops >20% month-over-month → full content audit
- New gap keyword with volume >500 appears → add FAQ or new section within 2 weeks

---

## Priority Order

| Priority | Action | Expected Impact |
|----------|--------|----------------|
| P0 | Content gap analysis (page vs. competitors) | Highest ROI — covers missing intent fast |
| P0 | FAQ Schema from question keywords | GEO citability + featured snippet eligibility |
| P1 | Title / H1 / H2 keyword remapping | Ranking signal alignment |
| P1 | Opening 50-word authoritative answer block | AI Overview / LLM citation rate |
| P2 | Internal link anchor text optimization | Distributes PageRank to target keywords |
| P2 | Alt text keyword coverage | Image search + accessibility |
| P3 | API-driven ranking monitor + alerts | Catch regressions early |

---

## Reference Projects

| Project | Stars | Use |
|---------|-------|-----|
| [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | ~7k | 25 sub-skills + 18 sub-agents, GEO/AEO, schema, semantic clustering |
| [serpapi/awesome-seo-tools](https://github.com/serpapi/awesome-seo-tools) | ~863 | Tool discovery: keyword research, rank tracking, GEO trackers |
| [teles/awesome-seo](https://github.com/teles/awesome-seo) | ~600+ | Reference links for keyword research fundamentals |
| [amplifying-ai/awesome-generative-engine-optimization](https://github.com/amplifying-ai/awesome-generative-engine-optimization) | ~300+ | GEO methodology, AI citability patterns |
| [aaron-he-zhu/seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills) | ~51 | CORE-EEAT + CITE frameworks, rank tracking skills |

---

## Ahrefs MCP Endpoints Used

| Endpoint | Phase | Purpose |
|----------|-------|---------|
| `keywords_explorer` | 1 | Volume, KD, related terms, questions |
| `site_explorer` | 1 | Competitor organic keyword lists |
| `content_gap` | 1, 4 | Missing keyword identification |
| `get_organic_keywords` | 4 | Page ranking health monitoring |
| `rank_tracker` | 4 | Position trend over time |
