---
name: news-curator
version: 1.0.0
description: "Fetch, filter, dedup, and deliver curated news briefings to Telegram. Benzinga for finance, AI News RSS for tech."
allowed-tools: [cron, exec, web_fetch, web_search]
---

# News Curator

Three daily briefings: morning (7:30am), afternoon (3pm), night (10pm). Each fetches live web content, filters, curates, and delivers to Telegram.

## Sources

| Type | Source |
|------|--------|
| Finance | Benzinga Markets feed (`site:benzinga.com markets`) |
| AI/Tech | Artificial Intelligence News RSS + The Verge AI |
| Backup | Web search: "latest AI artificial intelligence news today" + "latest finance markets news today" |

**Filter OUT:** personal finance, crypto, forex, NFT, spam, low-quality content, price predictions, lifestyle junk.

## Delivery format (via Telegram)

```
📰 News Briefing — June 3

💰 Finance & Markets:
• Title — one-line summary (source) | link

🤖 AI & Tech:
• Title — one-line summary (source) | link

Curated by Patch
```

## Cron schedule

| Time | Description | Model |
|------|-------------|-------|
| 7:30am | Morning briefing | `deepseek/deepseek-v4-flash` |
| 3:00pm | Afternoon briefing | `deepseek/deepseek-v4-flash` |
| 10:00pm | Night briefing | `deepseek/deepseek-v4-flash` |

All pin model explicitly. Timeout: 600s (web search + curation in one turn).

## Flow

1. Cron fires isolated agentTurn
2. Agent searches web for news (4 searches: finance, AI, Benzinga, The Verge)
3. Filters out junk content
4. Selects 6-8 most important items (mix finance + AI)
5. Formats into briefing block
6. Agent's response auto-delivers to Telegram via announce delivery mode

## Dedup (within single run)

Built into agent prompt: "Filter OUT personal finance, crypto, forex, NFT, spam" — implicit dedup via web search result freshness.

## News pending (legacy)

Old flow used `news-pending/` directory with curated-news.py fetching RSS at 7:30am. Replaced by direct web search in agentTurn crons. No longer in use.

## Scripts

- `deliver-news.sh` — legacy shell wrapper (deprecated)
- `send-news-today.sh` — legacy delivery (deprecated)

Prefer direct cron agentTurn over shell scripts.
