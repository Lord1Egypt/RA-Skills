# Multi-Source Feed — Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        OpenClaw Gateway                             │
│  Model: configurable    │  Fallback: configurable                   │
│  Retry: exponential backoff (30s → 60m cap)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────────────────────┐   ┌───────────────────────────┐     │
│  │   Daily Brief (main)      │   │   X-Push (optional)       │     │
│  │                            │   │                           │     │
│  │  Cron 1: Scrape  09:00    │   │  Cron: every 2h           │     │
│  │  Cron 2: Memo    09:20    │   │  X/Twitter only           │     │
│  └────────────────────────────┘   └───────────────────────────┘     │
│                                                                     │
│              * Both share config/user_profile.md                    │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
                     User's configured channel
```

## Daily Brief Pipeline

```
09:00 — crontab triggers python -m src.pipeline
     │
     ├── X/Twitter (Playwright)           ──┐
     ├── Hacker News (Algolia API)          │
     ├── GitHub Trending (BeautifulSoup)    │
     ├── AI blogs & tech media (RSS)        ├── raw items
     ├── Indie blogs & VC blogs (RSS)       │
     ├── arXiv (RSS)                        │
     ├── Reddit subs (API)                  │
     ├── Product Hunt (GraphQL)             │
     └── Tavily web searches (API)        ──┘
     │
     ▼
  Dedup
     ├── Intra-day: URL exact + title similarity (≥0.65)
     └── Cross-day: URLs from last 7 days of memo/*.md
     │
     ▼  deduplicated candidates
  Write feed_merged.json + feed_slim.json + data/YYYY-MM-DD.json
     │
─ ─ ─ ─ ─ ─ 20 min gap ─ ─ ─ ─ ─ ─
     │
09:20 — OpenClaw cron triggers memo generation
     │
     ▼
  Check feed_slim.json exists and is from today
     ├── Missing → notify user → abort
     └── Exists → continue
     │
     ▼
  LLM generates memo
     Reads: config/user_profile.md → config/preferences.md
            → feed_slim.json → yesterday's memo
     │
     ▼
  Output
     ├── Save to memo/YYYY-MM-DD.md
     └── Send to user via configured channel
```

## X-Push Pipeline (Optional)

```
Every 2h — OpenClaw cron triggers push/run.sh
     │
     ├── Scrape X/Twitter (quick mode: 15 posts/tab, 2min timeout)
     ├── Dedup against seen_posts.json (24h TTL)
     ├── Write new_posts.json
     │
     ▼
  LLM filters noteworthy posts
     Reads: config/user_profile.md → push/preferences.md → new_posts.json
     │
     ▼
  Send selected posts to user
```

## Source Types

All sources are configured in `config/sources.yaml`. The starter list covers these categories:

| Category | Type | Notes |
|----------|------|-------|
| X/Twitter | `x_feed` | For You + Following + Trending (Playwright) |
| Hacker News | `hn` | Algolia API, configurable min score |
| GitHub Trending | `github_trending` | Daily trending repos (BeautifulSoup) |
| AI Company Blogs | `rss` | OpenAI, Google AI, DeepMind, Meta, Microsoft, NVIDIA, HuggingFace, etc. |
| Tech Media | `rss` | TechCrunch, The Verge, MIT Tech Review, Wired, Ars Technica, Platformer, etc. |
| Independent Blogs | `rss` | Simon Willison, Lilian Weng, Chip Huyen, Stratechery, etc. |
| VC / Ecosystem | `rss` | YC Blog, a16z, Sequoia Capital, etc. |
| AI Research | `rss` | arXiv CS.AI, arXiv CS.LG |
| Reddit | `reddit` | Configurable subreddits (JSON API) |
| Product Hunt | `producthunt` | Daily top products (GraphQL API) |
| Web Search | `web_search` | Tavily API (configurable queries) |
| Anthropic News | `anthropic_news` | Custom scraper (no public RSS) |

Add your own sources with 4 lines of YAML — see README for details.

## Storage

| File | Purpose | Lifecycle |
|------|---------|-----------|
| `feed_raw.json` | Raw X/Twitter scrape | Overwritten each run |
| `feed_merged.json` | Full deduplicated feed | Overwritten each run |
| `feed_slim.json` | Slim feed for LLM (source/title/url/author/metrics only) | Overwritten each run |
| `data/YYYY-MM-DD.json` | Daily archive | Append per day |
| `memo/YYYY-MM-DD.md` | Daily memo (used for cross-day dedup) | Append per day |

## Configuration

| What | How |
|------|-----|
| Add RSS source | 4 lines in `config/sources.yaml` |
| Change interests | Edit `config/user_profile.md` |
| Change memo format | Edit `config/preferences.md` |
| Adjust dedup window | `XFEED_SHOWN_LOOKBACK_DAYS=N` in `.env` |
| Tune X scraper | `X_TARGET_POSTS`, `X_MAX_SCROLLS`, etc. in `.env` |
