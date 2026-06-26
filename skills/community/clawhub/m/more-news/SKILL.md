---
name: more-news
description: Fetch, aggregate, and rank AI/tech news from multiple sources listed in `workspace/source.md`. Use when the user asks to get AI news, tech news digest, aggregate news, latest news from sources, fetch news headlines, or compile news from a source list. Triggers on phrases like "get AI news from source.md", "fetch news from my sources", "aggregate tech news", "more-news". NOT for: generic web search queries, single article lookups.
---

# More News

Aggregate AI/tech news from user-defined sources in `source.md`. For broad AI news without a source file, consider using `big-ai-news` or `ai-news` skills instead.

## Workflow

### 1. Load Sources

Read `workspace/skills/more-news/source.md` to extract all source entries. The file uses a markdown table format with columns: #, Source, URL, Type/Focus. Extract all URLs.

### 2. Fetch Articles

For each source URL, use `web_fetch` in parallel batches (5 at a time):
- `maxChars`: 15000
- `extractMode`: "markdown"

**Handle failures gracefully:**
- If fetch returns 403/429/geo-block → skip and note as "blocked"
- If fetch returns navigation-only content with no articles → skip and note
- If fetch succeeds but has no recent articles → skip

### 3. Filter to Last 24 Hours

Only include articles published within 24 hours of the current time. Use article date stamps, relative timestamps ("2 hours ago" / "Apr 3"), or publication sections to determine recency.
For articles that lack full details (no URL, no full headline details), skip it.

### 4. Compile & Rank

Output ranked newest-to-oldest. Each entry must include:
- Numbered ranking (1, 2, 3...)
- Headline
- Brief summary (2-3 sentences)
- Source URL (clickable link — prefer original article URL)
- Approximate date/time

### 5. Report Skipped Sources

At the end, list which sources from `source.md` were skipped and why (blocked, no articles, stale).

## Output Format

```markdown
# 📰 AI News — Last 24 Hours (Ranked by datetime)

## [Date]

**1. Headline**
Brief summary here (2-4 sentences).
🔗 [Source Name](URL)

## Summary

| Metric | Count |
|--------|-------|
| Stories found | X |
| Sources fetched | Y of Z |
| Sources skipped | W |
```

## Tips

- For best results, keep `source.md` updated with reachable URLs
- RSS feeds or API endpoints work better than article listing pages
- If the user wants 50-100+ stories, recommend adding RSS feeds or using Tavily search skill as supplement
- De-duplicate across sources (same story from multiple outlets → list once with multiple links)
- If all sources are blocked, fall back to `web_search` for the news
