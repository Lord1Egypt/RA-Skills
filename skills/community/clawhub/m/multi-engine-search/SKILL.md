---
name: web-search
description: Unified multi-engine web search. Use when the user wants to search the web, find information, look up sources, or perform research. Supports Tavily API (fast) and browser-based search (Google, Bing, Baidu, DuckDuckGo). Can aggregate results from multiple engines. Triggers on "搜索", "search", "查一下", "找一下", "搜一下", "查找", "search the web", "look up", "google it", "bing", "百度".
---

# Web Search

Unified search interface across multiple search engines with result aggregation support.

## Quick Start

```bash
# Default search (Tavily API - fastest)
python3 {baseDir}/scripts/web_search.py --query "your search query"

# Specify engine
python3 {baseDir}/scripts/web_search.py --query "你的搜索内容" --engine baidu
python3 {baseDir}/scripts/web_search.py --query "search terms" --engine google

# Aggregate from multiple engines
python3 {baseDir}/scripts/web_search.py --query "关键词" --engine all

# Limit results
python3 {baseDir}/scripts/web_search.py --query "..." --max-results 10
```

## Search Engines

| Engine | Method | Best For | Speed |
|--------|--------|----------|-------|
| tavily | API | General web search, fast results | ⚡ Fastest |
| google | Browser | Comprehensive results, international | 🐢 Slow |
| bing | Browser | Microsoft ecosystem, image search | 🐢 Slow |
| baidu | Browser | Chinese content, domestic sites | 🐢 Slow |
| duckduckgo | Browser | Privacy-focused, no tracking | 🐢 Slow |
| all | Aggregated | Maximum coverage, research | 🐌 Slowest |

## Commands

### Tavily Search (Recommended)

Fast API-based search, best for most use cases:

```bash
python3 {baseDir}/scripts/web_search.py --query "..." --engine tavily

# With answer summary
python3 {baseDir}/scripts/web_search.py --query "..." --engine tavily --include-answer

# Markdown output
python3 {baseDir}/scripts/web_search.py --query "..." --engine tavily --format md
```

**Requirements:** `TAVILY_API_KEY` in environment or `~/.openclaw/.env`

### Browser-Based Search

Use agent-browser to access search engines directly:

```bash
# Google search
python3 {baseDir}/scripts/web_search.py --query "..." --engine google

# Baidu (for Chinese content)
python3 {baseDir}/scripts/web_search.py --query "关键词" --engine baidu

# Bing
python3 {baseDir}/scripts/web_search.py --query "..." --engine bing

# DuckDuckGo (privacy-focused)
python3 {baseDir}/scripts/web_search.py --query "..." --engine duckduckgo
```

### Aggregated Search

Search multiple engines and combine results:

```bash
python3 {baseDir}/scripts/web_search.py --query "..." --engine all --max-results 5
```

This searches Tavily + Google + Baidu and deduplicates results.

## Output Format

### JSON (default)

```json
{
  "query": "search query",
  "engine": "tavily",
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com",
      "snippet": "Brief description..."
    }
  ]
}
```

### Markdown (`--format md`)

```markdown
## Search Results: "query"

1. **[Title](url)**
   Description...

2. **[Title](url)**
   Description...
```

## Decision Guide

**Use Tavily when:**
- Need quick results
- General web search
- API available

**Use Google when:**
- Need comprehensive results
- International content
- Tavily unavailable

**Use Baidu when:**
- Searching Chinese content
- Looking for domestic Chinese sites
- Researching Chinese topics

**Use DuckDuckGo when:**
- Privacy is important
- Avoiding tracking
- Alternative perspective

**Use Aggregated when:**
- Research needs comprehensive coverage
- Important topic requiring multiple sources
- Comparing results across engines

## Workflow

1. **Determine engine preference**
   - Default: Tavily (fastest)
   - Chinese content: Baidu
   - Research: all engines

2. **Run search**
   ```bash
   python3 {baseDir}/scripts/web_search.py --query "..." --engine tavily --max-results 5
   ```

3. **If more depth needed**
   - Increase `--max-results`
   - Switch to `--engine all`
   - Use agent-browser directly for interactive search

## Integration with agent-browser

For complex search tasks requiring interaction:

```bash
# Open Google
agent-browser open "https://www.google.com/search?q=query"

# Open Baidu
agent-browser open "https://www.baidu.com/s?wd=关键词"

# Extract results
agent-browser snapshot -i
```

See [Agent Browser skill](../agent-browser/SKILL.md) for full browser automation capabilities.

## Notes

- Keep `--max-results` small (3-5) by default to reduce token usage
- Browser-based searches are slower due to page loading
- Aggregated search combines and deduplicates results from multiple engines
- For Chinese queries, Baidu often returns better localized results
