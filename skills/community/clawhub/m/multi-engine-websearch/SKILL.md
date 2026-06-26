---
name: websearch
version: 2.0.0
description: "Multi-engine web search across 6 engines: DuckDuckGo, DDG Lite, Yahoo, Yahoo JP, Startpage, and Google (headless Chromium). No API keys required. Returns 10+ results per engine, ranked by cross-engine frequency."
author: nirvesh-dagar
repository: https://github.com/nirveshdagar/multi-engine-websearch
tags: [search, web, research, google, multi-engine]
---

# WebSearch — Multi-Engine Search Aggregator

**🔗 GitHub:** https://github.com/nirveshdagar/multi-engine-websearch

**📦 Git Install:**
```bash
git clone https://github.com/nirveshdagar/multi-engine-websearch.git
```

**📦 ClawHub Install:**
```bash
npx clawhub@latest install multi-engine-websearch
```

---

A free, local web search skill that queries 6 reliable search engines simultaneously (in parallel), merges results, deduplicates URLs, and ranks by cross-engine frequency.

No API keys required. No paid subscriptions. Runs entirely on your machine.

## Requirements

- Python 3.9+
- Playwright (`pip3 install playwright && python3 -m playwright install chromium`)

Playwright is needed for the Google engine (headless Chromium renders JS-based results). All other engines use lightweight HTTP scraping with zero dependencies.

## When to Use

Use this skill whenever the user asks you to:
- Search the web for anything
- Find recent news, articles, or information
- Look up a topic, person, product, or event
- Verify a fact with current web results
- Research a topic with multiple sources

## Command

```bash
python3 ~/.openclaw/workspace/skills/websearch/scripts/search.py "your query" --json
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--json` / `-j` | off | Output as JSON |
| `--num` / `-n` | 10 | Results per engine |
| `--max` / `-m` | 50 | Max total results |
| `--engines` / `-e` | all 6 | Comma-separated engine list |
| `--list-engines` | — | Show available engines |

## Engines

| Engine | Method | Reliability |
|--------|--------|-------------|
| DuckDuckGo | HTML scrape | ⭐⭐⭐⭐⭐ |
| DDG Lite | HTML scrape | ⭐⭐⭐⭐ |
| Yahoo | HTML scrape | ⭐⭐⭐⭐ |
| Yahoo JP | HTML scrape | ⭐⭐⭐⭐ |
| Startpage | HTML scrape | ⭐⭐⭐⭐ |
| Google | Headless Chromium | ⭐⭐⭐⭐ |

All engines run in parallel using ThreadPoolExecutor for maximum speed.

## Output Format

```json
{
  "query": "your search",
  "total": 35,
  "engines": {"duckduckgo": 10, "google": 8, "yahoo": 10, ...},
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com",
      "snippet": "Description...",
      "engines": ["duckduckgo", "google", "yahoo"]
    }
  ]
}
```

Results appearing in more engines are ranked higher (cross-engine consensus).

## Core Rules

1. Always use `--json` flag when parsing results programmatically
2. Summarize top results in natural language for the user
3. Always cite sources with URLs
4. If one engine fails, others compensate — the system is resilient
5. Google engine is slower (~5s) due to headless browser; other engines are fast (~1-2s)
