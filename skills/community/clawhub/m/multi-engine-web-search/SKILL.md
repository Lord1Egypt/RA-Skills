---
name: Multi-Engine Web Search
slug: multi-engine-web-search
version: 1.0.0
homepage: https://clawic.com/skills/multi-engine-web-search
description: Search Google, Bing, DuckDuckGo, Brave, Startpage, Yahoo, Yandex, Baidu, Sogou, Qwant, Ecosia, Mojeek, and WolframAlpha from one skill.
changelog: Expanded engine coverage, added shortcut matrix, and improved operator examples for faster cross-check workflows.
metadata: {"clawdbot":{"emoji":"W","requires":{"bins":[]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` to define activation behavior and preferred engine order, then store the preference profile.

## When to Use

Use this when one engine is not enough and you need broader coverage, faster cross-checking, and cleaner verification.

## Architecture

Store minimal preferences in `~/multi-engine-web-search/`. See `memory-template.md`.

```text
~/multi-engine-web-search/
`-- memory.md   # activation mode, engine priority, blocked engines, and output style
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup flow and activation policy | `setup.md` |
| Minimal memory schema | `memory-template.md` |

## Search Engines

### Global Engines (12)
- **Google**: `https://www.google.com/search?q={keyword}`
- **Google HK**: `https://www.google.com.hk/search?q={keyword}`
- **Bing**: `https://www.bing.com/search?q={keyword}`
- **Yahoo**: `https://search.yahoo.com/search?p={keyword}`
- **DuckDuckGo**: `https://duckduckgo.com/html/?q={keyword}`
- **Brave**: `https://search.brave.com/search?q={keyword}`
- **Startpage**: `https://www.startpage.com/sp/search?query={keyword}`
- **Qwant**: `https://www.qwant.com/?q={keyword}`
- **Ecosia**: `https://www.ecosia.org/search?q={keyword}`
- **Mojeek**: `https://www.mojeek.com/search?q={keyword}`
- **Swisscows**: `https://swisscows.com/web?query={keyword}`
- **AOL Search**: `https://search.aol.com/aol/search?q={keyword}`

### Regional Engines (9)
- **Baidu**: `https://www.baidu.com/s?wd={keyword}`
- **Bing CN**: `https://cn.bing.com/search?q={keyword}&ensearch=0`
- **Bing INT (CN endpoint)**: `https://cn.bing.com/search?q={keyword}&ensearch=1`
- **Sogou**: `https://www.sogou.com/web?query={keyword}`
- **360 Search**: `https://www.so.com/s?q={keyword}`
- **Yandex**: `https://yandex.com/search/?text={keyword}`
- **Naver**: `https://search.naver.com/search.naver?query={keyword}`
- **Seznam**: `https://search.seznam.cz/?q={keyword}`
- **CocCoc**: `https://coccoc.com/search?query={keyword}`

### Knowledge and Developer Engines (6)
- **WolframAlpha**: `https://www.wolframalpha.com/input?i={keyword}`
- **Wikipedia**: `https://en.wikipedia.org/w/index.php?search={keyword}`
- **GitHub Search**: `https://github.com/search?q={keyword}`
- **Stack Overflow Search**: `https://stackoverflow.com/search?q={keyword}`
- **Semantic Scholar**: `https://www.semanticscholar.org/search?q={keyword}`
- **PubMed**: `https://pubmed.ncbi.nlm.nih.gov/?term={keyword}`

## Engine Shortcuts

| Shortcut | Engine |
|----------|--------|
| `!g` | Google |
| `!ghk` | Google HK |
| `!b` | Bing |
| `!y` | Yahoo |
| `!ddg` | DuckDuckGo |
| `!br` | Brave |
| `!sp` | Startpage |
| `!qw` | Qwant |
| `!eco` | Ecosia |
| `!mj` | Mojeek |
| `!sw` | Swisscows |
| `!aol` | AOL Search |
| `!ba` | Baidu |
| `!bcn` | Bing CN |
| `!sg` | Sogou |
| `!360` | 360 Search |
| `!ydx` | Yandex |
| `!nav` | Naver |
| `!sz` | Seznam |
| `!cc` | CocCoc |
| `!wa` | WolframAlpha |
| `!w` | Wikipedia |
| `!gh` | GitHub Search |
| `!so` | Stack Overflow |
| `!ss` | Semantic Scholar |
| `!pm` | PubMed |

## Quick Examples

```javascript
// 1) Basic multi-engine pass
web_fetch({"url": "https://www.google.com/search?q=llm+agent+framework"})
web_fetch({"url": "https://duckduckgo.com/html/?q=llm+agent+framework"})
web_fetch({"url": "https://search.brave.com/search?q=llm+agent+framework"})

// 2) Site-specific verification
web_fetch({"url": "https://www.bing.com/search?q=site:github.com+fastapi+auth"})

// 3) Filetype query
web_fetch({"url": "https://www.google.com/search?q=rag+evaluation+filetype:pdf"})

// 4) Recency-focused query
web_fetch({"url": "https://www.google.com/search?q=ai+policy+2026&tbs=qdr:m"})

// 5) Knowledge query
web_fetch({"url": "https://www.wolframalpha.com/input?i=150+USD+to+EUR"})
```

## Advanced Operators

| Operator | Example | Purpose |
|----------|---------|---------|
| `site:` | `site:arxiv.org agentic ai` | Limit to one domain |
| `filetype:` | `filetype:pdf model card` | Find specific formats |
| `""` | `"context window"` | Exact phrase |
| `-` | `python -snake` | Exclude noisy term |
| `OR` | `llama OR mistral` | Alternative terms |
| `intitle:` | `intitle:benchmark llm` | Keyword in page title |
| `inurl:` | `inurl:docs authentication` | Keyword in URL |

## Time Filters

| Pattern | Example | Purpose |
|---------|---------|---------|
| `tbs=qdr:h` | Google past hour | Breaking updates |
| `tbs=qdr:d` | Google past day | Daily changes |
| `tbs=qdr:w` | Google past week | Weekly updates |
| `before:` | `ai act before:2026-03-01` | Upper date bound |
| `after:` | `ai act after:2025-01-01` | Lower date bound |

## Core Rules

### 1. Check Preferences First
Before searching, read memory preferences:
- activation mode (always, on-request, or mixed)
- preferred engine order
- blocked engines
- output style (fast summary or evidence-heavy)

### 2. Always Use Multi-Engine Batches
Run at least 3 engines per request: one mainstream, one privacy engine, and one alternate index.

### 3. Add a Contradiction Query
For every important claim, run one query that looks for disagreement, failures, or corrections.

### 4. Prefer Primary Sources
If sources conflict, prioritize original docs, direct announcements, and first-party datasets.

### 5. Verify Date Context
For current topics, verify publication date and event date before final conclusions.

### 6. Return Evidence First
Output must include direct answer, best links, and confidence in one concise block.

## Common Traps

- Using only one engine and assuming top results are correct.
- Forgetting contradiction queries on high-impact decisions.
- Treating copied news rewrites as independent confirmation.
- Ignoring date filters for rapidly changing topics.
- Returning link dumps without a clear recommendation.

## External Endpoints

| Endpoint Family | Data Sent | Purpose |
|-----------------|-----------|---------|
| Public search engines listed above | query text | Multi-engine retrieval and cross-checking |
| Knowledge and developer engines listed above | query text | Technical, scientific, and code verification |

No other data is sent externally.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `analysis` - Turn search findings into clear conclusions
- `compare` - Compare options side by side with tradeoffs
- `web` - Inspect pages deeply after initial retrieval
- `in-depth-research` - Expand into long-form investigations
- `elasticsearch` - Build custom search backends when needed

## Feedback

- If useful: `clawhub star multi-engine-web-search`
- Stay updated: `clawhub sync`
