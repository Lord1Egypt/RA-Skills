---
name: nature
description: Fetch and summarize the latest AI-related articles from Nature's RSS feed and the top 7 AI news from New Scientist Technology. Use when the user asks for Nature AI news, Nature science news, New Scientist AI news, or wants the latest research headlines from nature.com or newscientist.com. Triggers on phrases like "Nature AI news", "get AI news from Nature RSS", "New Scientist AI news", "latest Nature publications", "merge Nature and New Scientist AI news". Uses direct web_fetch only — never uses web_search.
---

# Nature + New Scientist AI News

Fetches AI news from two sources and merges results. Uses `web_fetch` only — no `web_search`.

## Sources

1. **Nature RSS**: `https://www.nature.com/nature.rss`
2. **New Scientist Tech**: `https://www.newscientist.com/subject/technology/`

## Workflow

### Step 1 — Fetch Nature RSS

```
web_fetch(url="https://www.nature.com/nature.rss", extractMode="text", maxChars=50000)
```

Parse the XML. Each `<item>` has `<title>`, `<link>`, `<dc:date>` (YYYY-MM-DD).

**Filter keywords**: ai, artificial intelligence, machine learning, deep learning, neural network, quantum computing, llm, agi, chip, data centre, data center, algorithm, automation, generative, transformer, gpt, agent, autonomous, cybersecurity, encryption.

**Date rule**: keep only items from the last 3 days (Nature posts infrequently — 24h yields too little).

### Step 2 — Fetch New Scientist Technology

```
web_fetch(url="https://www.newscientist.com/subject/technology/", extractMode="markdown", maxChars=50000)
```

Extract article links and headlines from the markdown output. For the top items, also fetch the individual article pages to get summaries:

```
web_fetch(url="<article-link>", extractMode="markdown", maxChars=5000)
```

**Filter**: Keep only AI-related articles (same keyword list as Nature). Return **top 7** by recency.

### Step 3 — Merge & Present

Combine results from both sources into a single digest, grouped by source:

```
## 🟢 New Scientist — AI News

**Headline** (date if available)
One-sentence summary.
→ URL

## 🔵 Nature — AI News

**Headline** (date)
One-sentence summary.
→ URL
```

**Rules**:
- Max 7 items per source
- If one source has zero AI items, say so honestly — don't pad
- Always indicate which source each item came from
