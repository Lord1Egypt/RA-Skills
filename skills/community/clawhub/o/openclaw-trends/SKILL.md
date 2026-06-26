---
name: openclaw-trends
description: Fetch and aggregate OpenClaw-related content from across the internet. Use when the user asks about OpenClaw trends, news, tutorials, videos, community discussions, or what people are saying about OpenClaw. Triggers on phrases like "what's new with OpenClaw", "find OpenClaw tutorials", "OpenClaw news", "OpenClaw YouTube videos", or checking for OpenClaw mentions online.
---

# OpenClaw Trends

Fetch trending content about OpenClaw from multiple sources and deliver a summary.

## Quick Start

```bash
python3 scripts/fetch_trends.py [--days 3] [--output json|text]
```

## Workflow

1. **Fetch from sources**:
   - **YouTube** - Videos (Data API v3)
   - **GitHub** - Repos, discussions, releases
   - **X/Twitter** - Posts (web search)
   - **Reddit** - Discussions (web search)
   - **Hacker News** - Tech discussions (web search)

2. **Filter by freshness**: Default 2-3 days

3. **Deduplicate & rank**: Remove duplicates, sort by date

4. **Output**: Structured summary with links

## Notes

- **YouTube** uses Data API v3 (key embedded for convenience)
- **X/Twitter, Reddit, HN** use DuckDuckGo web search (no API needed)
- **GitHub** uses `gh` CLI (auto-detected)
- For agent-triggered runs, the `web_search` tool provides richer results

## Output Format

Returns a structured summary:
- **Source** (YouTube, X, Blog, etc.)
- **Title**
- **Description** (truncated)
- **URL**
- **Date**

## Scheduled Checks

For daily updates, add to cron:

```bash
# Daily OpenClaw trends at 9 AM
0 9 * * * cd ~/.openclaw/workspace/skills/openclaw-trends && python3 scripts/fetch_trends.py --days 3 --notify
```

## Notes

- YouTube uses Data API v3 (requires key)
- X/Twitter uses web search (no API needed)
- GitHub uses `gh` CLI or REST API
- All other sources use web search
