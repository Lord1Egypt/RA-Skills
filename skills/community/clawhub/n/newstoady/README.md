# NewsToday

> 私人新闻助手 — 早报 · 晚报 · AI早报 · RSS聚合 · 突发提醒 · 热榜聚合 · 话题追踪 · 军事新闻 · 个性化推送

An [OpenClaw](https://openclaw.ai) skill that aggregates, deduplicates, and summarizes the most important news stories into a single readable briefing — delivered at the right time, via your preferred channel.

## Features

- **Morning Briefing** — 10 top stories across politics, finance, tech, international, and society; pulled from RSS feeds (Sina News, The Paper, 36Kr, BBC Chinese, Reuters Chinese) + real-time WebSearch
- **Evening Recap** — 3–5 key developments of the day + preview of tomorrow's events
- **Breaking News Alerts** — auto-fires every 2 hours (08:00–22:00) when a major story breaks (earthquakes, market crashes, political announcements)
- **Hot List Aggregation** — merges Weibo, Zhihu, Baidu, and X (Twitter) trending lists with deduplication; X falls back silently if unavailable
- **AI Briefing** — dedicated mode for AI/LLM news (trigger: "AI早报", "AI最新", "人工智能动态"); 5 focused stories from AI-specific sources
- **Topic Tracking** — follows a keyword over time with timeline, official responses, and multiple perspectives
- **Personalized Topics** — weight finance over entertainment, boost international coverage, etc.
- **Military News** — dedicated category covering regional conflicts, defense policy, and military exercises
- **Bilingual** — Chinese and English output supported

## Supported Channels

`telegram` / `feishu` / `slack` / `discord`

## Quick Start

```bash
# Optional: register to unlock personalized push & breaking alerts
node scripts/register.js <userId> [language] [topics] [channel]
# e.g.
node scripts/register.js alice zh 科技,财经,国际 telegram
node scripts/register.js bob en tech,finance telegram

# Manual trigger (no registration needed)
node scripts/morning-push.js [userId]
node scripts/evening-push.js [userId]
node scripts/rss-fetch.js [--lang zh|en] [--topics 科技,财经]
node scripts/breaking-alert.js <userId>

# Topic preferences
node scripts/preference.js show <userId>
node scripts/preference.js set <userId> <topic> <weight 0-1>
node scripts/preference.js reset <userId>

# Push management
node scripts/push-toggle.js on <userId> [--morning 08:00] [--evening 20:00] [--channel telegram]
node scripts/push-toggle.js off <userId>
node scripts/push-toggle.js status <userId>
```

## Notes

- No registration required for on-demand morning/evening briefings
- Each story includes source attribution and a 2-sentence summary
- Controversial topics present multiple perspectives without editorial stance
- If RSS feeds are unavailable, the skill automatically falls back to WebSearch
- User data stored in `data/users/<userId>.json` contains only preferences and topic weights — no news content
