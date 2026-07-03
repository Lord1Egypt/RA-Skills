---
name: news-curator
version: 2.0.0
description: "Fetch RSS feeds via curl, curate, and deliver news briefings to Telegram. MiniMax M3, isolated cron sessions, curl-not-fetch."
allowed-tools: [cron, exec]
---

# News Curator

Three daily briefings: morning (7:30am), afternoon (3pm), evening (10pm). Each uses a direct isolated cron session — no sub-agents, no sessions_yield, no spawn.

## Architecture — Critical

**DO NOT use sessions_spawn + sessions_yield.** The yield causes the parent session file to change during the wait, triggering `EmbeddedAttemptSessionTakeoverError`. Instead:

- Cron fires `sessionTarget: "isolated"` with `kind: "agentTurn"`
- Agent does ALL work in one shot: curl feeds → parse XML → curate → output briefing
- Final response auto-delivers to Telegram via `delivery.mode: "announce"`
- No `sessions_spawn`, no `sessions_yield`, no `send_message`
- Explicitly tell the agent: "Use exec tool with curl. Do NOT use fetch tool." MiniMax defaults to `fetch` which returns HTML blocks on some RSS endpoints.

## Prompt Essentials

Every news cron prompt MUST include:

1. **"Use exec tool with curl. Do NOT use fetch tool."** — MiniMax M3 prefers its built-in `fetch` tool which gets blocked by many RSS endpoints. `curl -sL` works. Without this line, the model will use `fetch` and fail.

2. **"Final response = the briefing. Nothing else. No meta, no talk about what you did."** — Without this, MiniMax often outputs a description of its process ("Gus fetched the feeds and curated 5 stories...") instead of the actual briefing.

3. **Do NOT use "send_message"** — The final reply auto-delivers. Using `message` tool causes duplicate delivery or errors.

4. **"Real URLs from feeds only. No fake links."** — The model may fabricate headlines.

5. List each curl command on its own line. The model will run them sequentially via `exec` tool.

## Sources (verified working with curl -sL --max-time 25)

| Type | Source | URL |
|------|--------|-----|
| AI | AI News | https://artificialintelligence-news.com/feed/ |
| AI | TechCrunch AI | https://techcrunch.com/category/artificial-intelligence/feed/ |
| AI | Wired | https://www.wired.com/feed/rss |
| AI | Ars Technica | https://arstechnica.com/feed/ |
| AI | MIT Tech Review | https://www.technologyreview.com/topic/artificial-intelligence/feed/ |
| Finance | Benzinga Markets | https://www.benzinga.com/markets/feed |
| Finance | Bloomberg Markets | https://feeds.bloomberg.com/markets/news.rss |
| Finance | Financial Times | https://www.ft.com/markets?format=rss |
| Finance | MarketWatch/Dow Jones | https://feeds.content.dowjones.io/public/rss/mw_topstories |
| Finance | Investing.com | https://www.investing.com/rss/news.rss |
| Finance | Seeking Alpha | https://seekingalpha.com/market_currents.xml |

**DO NOT use** The Verge RSS (`https://www.theverge.com/rss/ai-artificial-intelligence/index.xml`) — returns HTML captcha, always blocked.

**DO NOT use** Google News RSS — 400 error.

**DO NOT use** Nasdaq RSS — returns empty/000.

Reuters, CNBC, Yahoo Finance RSS feeds also unreliable (block flakily). Stick to the verified list above.

## Filtering rules

Skip: crypto, forex, personal finance ("I have $X saved what do I do"), NFT, price predictions, spam, earnings transcript full text, obituaries, press releases.

Prefer: major AI lab/product/policy news, big market swings, Fed/rates signals, tech positioning, AI capex reality checks, Nasdaq-moving events. Hobo likes knowing when to buy the dip.

Target 5-7 stories per briefing, split roughly half AI and half markets. 1500-3000 chars total.

## Delivery format

Each cron's prompt has its own formatted template. General structure:

```
{{emoji}} *Patch {{time}} briefing* [time SGT]

*AI & TECH*
1. [Headline](full url) — one punchy sentence

*MARKETS & MONEY*
1. [Headline](full url) — what moved, signal for tech

*NOTES*
Feeds that failed, if any.

~ Patch
```

Emojis: morning 🌅, afternoon 🌤️, evening 🌙.

## Cron schedule & collision avoidance

**CRITICAL:** With `maxConcurrentRuns: 2`, any two crons firing at the same minute will collide and trigger `EmbeddedAttemptSessionTakeoverError`. Every cron's minute must be unique.

| Time | Cron | Notes |
|------|------|-------|
| 07:30 | Morning news | ✅ unique |
| 09:00 | Transport check-in | ✅ |
| 09:03, 09:37 | Pi Dashboard | odd minutes avoid :00 |
| 09:34 | Expense Sync to Sheet | was 09:30, moved to avoid collision |
| 10:00 | Expense Check-in 10am | ✅ |
| ~:05 | Token Usage Tracker | `0 * * * *` + staggerMs 300000 |
| :07 | Regenerate Memory Dashboard | `7 * * * *` fixed minute |
| 13:30 | Expense Check-in 1:30pm | ✅ |
| 15:00 | Afternoon news | ✅ unique |
| 21:50 | Expense Check-in 10pm | ✅ |
| 22:00 | Evening news | ✅ unique |
| 23:50 | Daily Memory Log | ✅ unique |
| 00:00 | Backup workspace | ✅ unique (every 2 days) |
| Sat 10:00 | Investment Check-in | shares minute with Expense Check-in 10am — watch for collision |
| Sat 11:00 | Investment Sync | ✅ unique |
| Sun 05:00 | Weekly Security Audit | ✅ unique |

**Rule:** Never put two crons on the same minute. If unavoidable, shift one by 3-5 minutes.

## Model config

| Parameter | Value |
|-----------|-------|
| Model | `minimax/MiniMax-M3` |
| Fallbacks | `deepseek/deepseek-v4-flash`, `openrouter/auto` |
| Timeout | 300s (ample — typical run ~70s) |
| Thinking | Not explicitly set (cron session inherits default) |

MiniMax M3 is the primary. DeepSeek V4 Flash falls back cleanly if MiniMax times out. The `EmbeddedAttemptSessionTakeoverError` only happens when two crons share a minute, not from model issues.

## Session setup

- `sessionTarget: "isolated"` — fresh session per run, no memory of previous chats
- `sessionKey` — unique per cron (e.g. `session:cron:patch-news-morning-briefing`)
- `delivery.mode: "announce"` — agent's final response auto-sent to Telegram
- `delivery.to: "37134287"` — Hobo's chat ID

## What NOT to do (lessons from failures)

1. **No spawn + yield** — `sessions_spawn` + `sessions_yield` triggers session file fence check failure
2. **No sub-agents for this** — the isolated session already is a fresh session. Adding a sub-agent wrapper adds the yield problem and extra cost for no benefit
3. **No sending to the main Telegram session** — give each cron its own `sessionKey`. Main session key collisions cause lock contention
4. **Don't use the `fetch` tool** — MiniMax's built-in `fetch` blocks on many RSS endpoints. Force `exec` + `curl`
5. **Don't skip "no meta" instructions** — MiniMax defaults to verbose meta-commentary about what it did instead of outputting the briefing
6. **Don't put two crons on the same minute** — `maxConcurrentRuns: 2` still causes session file races when both fire simultaneously. Offset by at least 3 minutes

## Legacy

- `fetch-news.py` — old script for parallel RSS fetching (no longer used)
- `news-pending/` — directory for old 2-step flow (no longer used)
- `send-news.sh`, `deliver-news.sh` — legacy shell wrappers (deprecated)
- All replaced by direct isolated cron agentTurn with inline curl
