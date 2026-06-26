---
name: japan-news-mcp
description: "Get Japanese financial and business news from Yahoo News Japan, NHK, Reuters Japan, and Toyo Keizai (東洋経済) — search headlines by keyword, get article summaries. Japan stock market news, economic news, corporate news. No API key required."
metadata: {"openclaw":{"emoji":"📰","requires":{"bins":["japan-news-mcp"]},"install":[{"id":"uv","kind":"uv","package":"japan-news-mcp","bins":["japan-news-mcp"],"label":"Install japan-news-mcp (uv)"}],"tags":["japan","news","finance","rss","mcp","business","economy","japanese"]}}
---

# Japan News: Japanese Financial & Business News

Get the latest Japanese financial and business news from 4 major RSS sources. No API key required — all sources are public RSS feeds.

## Use Cases

- Get latest business/financial headlines from major Japanese news sources
- Search for news about specific companies (トヨタ, ソニー, etc.)
- Monitor breaking financial news for investment research
- Summarize recent economic/business trends in Japan
- Send periodic news digests via Telegram

## Commands

### Get headlines
```bash
# Get latest headlines from all sources
japan-news-mcp headlines

# From a specific source
japan-news-mcp headlines --source yahoo
japan-news-mcp headlines --source nhk
japan-news-mcp headlines --source reuters
japan-news-mcp headlines --source toyokeizai

# Limit results
japan-news-mcp headlines --limit 10 --format json
```

### Search news
```bash
# Search by keyword
japan-news-mcp search トヨタ
japan-news-mcp search "日銀 金利"
japan-news-mcp search inflation --format json
```

### List sources
```bash
japan-news-mcp sources
```

### Test connectivity
```bash
japan-news-mcp test
```

## News Sources

| Source | Language | Coverage |
|---|---|---|
| Yahoo News Japan (ビジネス) | Japanese | Broad business/economy |
| NHK (経済) | Japanese | Public broadcaster, policy focus |
| Reuters Japan (ビジネス) | Japanese | International perspective |
| Toyo Keizai Online (東洋経済) | Japanese | Deep analysis, corporate |

## Workflow

1. `japan-news-mcp headlines` → browse latest news
2. `japan-news-mcp search <keyword>` → find specific company/topic news
3. Summarize and report findings

## Important

- No API key required — uses public RSS feeds
- Rate limited to avoid overloading news sources
- News content is copyrighted — summarize, don't reproduce full articles
- Python package: `pip install japan-news-mcp` or `uv tool install japan-news-mcp`
