---
name: no-news
description: Fetch and display international tech news from curated RSS feeds (TechCrunch, The Verge, Wired, Ars Technica, Engadget, Hacker News, MIT Technology Review, Gizmodo). Use when the user asks for tech news, latest technology headlines, international tech digest, or says "no-news", "tech news", "科技新闻". NOT for: AI-specific news aggregation (use ai-news or big-ai-news), Chinese tech news (use caixin), Hacker News only (use hn-news).
---

# No-News — 国际科技新闻

Fetch tech news from 8 curated RSS sources and display as a markdown table.

## Quick Start

Run the bundled script:

```
python scripts/tech_news.py --summary
```

This fetches all sources (with 30-min cache) and outputs a markdown table with title, source link, publish time, and summary.

## Options (resolve from user request when specified)

| Flag | Purpose |
|---|---|
| `--summary` | Include 摘要 column (recommended default) |
| `-s <source>` | Single source (techcrunch, theverge, wired, arstechnica, engadget, hackernews, mittech, gizmodo) |
| `-l <N>` | Items per source (default 10) |
| `--no-cache` | Skip cache, force fresh fetch |
| `--sources` | List available sources |

## Workflow

1. Run `scripts/tech_news.py --summary` (add `-s` or `-l` if user specified).
2. Present the markdown output directly to the user.
3. If user wants details on a specific article, provide the link from the table.

## Dependencies

Requires `feedparser`, `requests`, `rich` — install if missing:

```
pip install feedparser requests rich
```
