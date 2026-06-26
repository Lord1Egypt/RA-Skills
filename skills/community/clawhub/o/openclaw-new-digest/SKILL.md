---
name: news-digest
description: "User-configurable multi-slot news aggregation and push system. Schedule, topics, and keywords are defined by the user via config.json. Aggregates from Twitter, Hacker News, Tavily, filters by influence, summarizes, stores locally, supports feedback iteration."
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":["node"],"env":["TAVILY_API_KEY","XPOZ_API_KEY"]},"primaryEnv":"TAVILY_API_KEY"}}
---

# News Digest

AI-assisted news aggregation and push system with **user-defined schedule and topics**. The agent fetches content from Twitter (Xpoz MCP), Hacker News, and Tavily Search, then filters, summarizes, and delivers via Feishu/Telegram. This is an **agent-driven workflow** — the agent is the executor, triggered manually or by cron.

## First-Time Setup (IMPORTANT)

Before executing any push, **check if a configuration exists**:

```bash
node {baseDir}/scripts/manage-config.mjs show
```

If the output says "No Configuration Found", you **MUST** ask the user to set up their schedule before proceeding. Do NOT use hardcoded defaults without user consent.

### Setup Conversation Flow

Ask the user these questions one by one:

1. **"你希望每天推送几次？"** — Determine the number of daily push slots (typical: 2-4).
2. **For each slot, ask:**
   - **"第 N 个推送的时间是？"** (e.g. 08:00, 12:00, 18:00)
   - **"这个时段的主题/方向是什么？"** (e.g. 金融, AI/Agent, 综合热点)
   - **"这个主题的标签名称？"** (e.g. 金融早报, AI午报, 晚间热点)
   - **"关键词有哪些？"** (comma-separated)
   - **"优先级规则？"** (e.g. crypto > 金融事件 > 美股)
3. **"需要调整默认设置吗？"** — Summary length (default: 100-300 chars), language (default: zh-CN), items per push (default: 3-10), time window (default: 24h).

### Save Each Slot

After collecting user preferences, save each slot:

```bash
node {baseDir}/scripts/manage-config.mjs set-slot \
  --name <slot_name> \
  --time <HH:MM> \
  --topic "<topic>" \
  --label "<display_label>" \
  --keywords "<kw1,kw2,kw3>" \
  --priority "<priority_rules>" \
  --sources "twitter,tavily,hackernews"
```

Example:
```bash
node {baseDir}/scripts/manage-config.mjs set-slot --name morning --time 08:00 --topic "Finance" --label "金融早报" --keywords "crypto,bitcoin,ethereum,finance,stock" --priority "crypto > financial events > US stocks" --sources "twitter,tavily,hackernews"
```

### Update Defaults (Optional)

```bash
node {baseDir}/scripts/manage-config.mjs set-defaults --summary-language en --items-per-push "5-15"
```

### Quick-Init with Defaults

If the user is okay with the standard 3-slot setup (08:00 Finance, 12:00 AI, 18:00 General):
```bash
node {baseDir}/scripts/manage-config.mjs init
```

### Verify

```bash
node {baseDir}/scripts/manage-config.mjs show
```

## Quick Start (After Config Exists)

**Manual push** — just tell the agent:
> "Execute the news digest push for [slot_name]"

**Scheduled push** — set up cron entries matching your config (see `references/setup-guide.md`):
```bash
# Example — adjust times and slot names to match YOUR config
0 8 * * *  /path/to/news-digest-1.0.0/scripts/cron-trigger.sh --slot morning
0 12 * * * /path/to/news-digest-1.0.0/scripts/cron-trigger.sh --slot noon
0 18 * * * /path/to/news-digest-1.0.0/scripts/cron-trigger.sh --slot evening
```

The `cron-trigger.sh` script reads `config.json` for slot definitions, loads `.env`, and spawns an OpenClaw session.

**Check environment**:
```bash
node {baseDir}/scripts/env-check.mjs
```

## Configuration Management

```bash
# View current config
node {baseDir}/scripts/manage-config.mjs show

# Add or update a slot
node {baseDir}/scripts/manage-config.mjs set-slot --name <name> --time <HH:MM> --topic <topic> --label <label> --keywords <kw>

# Remove a slot
node {baseDir}/scripts/manage-config.mjs remove-slot --name <name>

# Update defaults
node {baseDir}/scripts/manage-config.mjs set-defaults --summary-length "100-300"

# Reset to factory defaults
node {baseDir}/scripts/manage-config.mjs reset
```

The user can change their schedule at any time. Just re-run `set-slot` or `remove-slot` and update cron accordingly.

## Workflow

For each push slot, follow these steps **in order**. Read the slot's configuration first.

### Step 0: Load Slot Configuration

```bash
node {baseDir}/scripts/manage-config.mjs show
```

Identify the target slot from the output: its `topic`, `keywords`, `priority`, `sources`, and `influence_thresholds`. All subsequent steps use these values — do NOT use hardcoded topics or keywords.

### Step 1: Check Previous Feedback

```bash
node {baseDir}/scripts/query.mjs feedback --days 3
```

Review recent feedback and adjust your filtering/summarization strategy accordingly.

### Step 2: Fetch Data from All Sources

Use the slot's **keywords** and **sources** from config. Run in parallel:

**Hacker News** (if `hackernews` in sources):
```bash
node {baseDir}/scripts/fetch-hackernews.mjs "<keywords joined with OR>" --min-score <hackernews_score from config> --hours <time_window_hours from defaults> -n 20
```

**Tavily Search** (if `tavily` in sources):
```bash
node {baseDir}/scripts/fetch-tavily.mjs "<keywords as search query>" --topic news --days 1 -n 10
```

Run multiple Tavily queries if the slot has diverse keywords — e.g. one for high-priority keywords, one for secondary.

**Twitter** via Xpoz MCP (if `twitter` in sources and `XPOZ_API_KEY` is set):

Use the Xpoz MCP tool `xpoz_search_tweets` with the slot's keywords. Filter by `min_likes > <twitter_likes from config>`. If `XPOZ_API_KEY` is not configured, skip and rely on other sources.

### Step 3: Deep-Read Key Articles (Optional)

For articles with thin summaries, extract full content:

```bash
node {baseDir}/scripts/extract-tavily.mjs "https://example.com/article1" "https://example.com/article2"
```

### Step 4: Filter & Select

Apply these rules, using thresholds from the slot's config:

1. **Time window**: Only content within the configured `time_window_hours` (default: 24h).
2. **Influence threshold**: Use `influence_thresholds` from the slot config.
3. **Topic match**: Content must match the slot's topic and keywords. Use `priority` to rank.
4. **Deduplication**: Same event from different outlets counts as one.
5. **Count**: Select items within the `items_per_push` range from config defaults.

### Step 5: Summarize Each Item

For each selected item:

- **Do NOT copy the original text verbatim.** Read and distill.
- **Length**: Use `summary_length` from config defaults (default: 100-300 chars).
- **Language**: Use `summary_language` from config defaults (default: zh-CN).
- **Structure**: Event overview → Key data/viewpoints → Potential impact.

### Step 6: Format the Push

```markdown
【{slot.label}】{time} 推送

1. [{category}] {title}（来源：{source}）
   {summary}
   🔗 {url}

2. [{category}] {title}（来源：{source}）
   {summary}
   🔗 {url}

...

---
📊 本次用量：Tavily Search ×{n} | Tavily Extract ×{n} | HN ×{n} | Xpoz ×{n}
💬 如有反馈，请直接回复。
```

Use the `label` field from the slot config as the topic label.

**Last slot of the day extra**: For the last scheduled slot in the config, append a monthly API usage forecast:
```bash
node {baseDir}/scripts/track-usage.mjs forecast
```

### Step 7: Track Usage & Store the Push

**Count your API calls** during steps 2-3:
- `fetch-tavily.mjs` = +1 `tavily_search`
- `extract-tavily.mjs` = +1 `tavily_extract` per URL batch
- `fetch-hackernews.mjs` = +1 `hackernews`
- Xpoz MCP tool call = +1 `xpoz`

Include the counts in the `usage` field when storing:

```bash
echo '{
  "slot": "<slot_name>",
  "topic": "<slot_topic>",
  "keywords": ["<from config>"],
  "items": [
    {
      "source": "twitter",
      "category": "crypto",
      "title": "Bitcoin hits new high",
      "url": "https://...",
      "author": "@example",
      "influence_score": 1520,
      "raw_excerpt": "Original excerpt...",
      "summary": "Your summary...",
      "metadata": {"likes": 1520, "retweets": 340}
    }
  ],
  "usage": {
    "tavily_search": 2,
    "tavily_extract": 1,
    "hackernews": 1,
    "xpoz": 1
  }
}' | node {baseDir}/scripts/store-push.mjs
```

This automatically persists usage data to `data/usage/YYYY-MM.json`.

You can also record usage separately:
```bash
node {baseDir}/scripts/track-usage.mjs record --slot <name> --tavily-search 2 --tavily-extract 1 --hackernews 1 --xpoz 1
```

### Step 8: Deliver the Push

Send the formatted push content through OpenClaw's built-in messaging (Feishu or Telegram, as configured by the user).

### Step 9: Handle Feedback

When a user provides feedback (free text), record it:

```bash
node {baseDir}/scripts/add-feedback.mjs --date 2026-03-06 --slot <name> "feedback text"

# Feedback on a specific item
node {baseDir}/scripts/add-feedback.mjs --date 2026-03-06 --slot <name> --item-id item-001 "this summary is too brief"
```

When a user asks to **modify the schedule or topics**, use `manage-config.mjs`:
```bash
# Change a slot's time
node {baseDir}/scripts/manage-config.mjs set-slot --name morning --time 07:30

# Change keywords
node {baseDir}/scripts/manage-config.mjs set-slot --name morning --keywords "crypto,defi,bitcoin,ethereum"

# Add a new slot
node {baseDir}/scripts/manage-config.mjs set-slot --name afternoon --time 15:00 --topic "Markets" --label "盘后速递" --keywords "stocks,earnings,markets"

# Remove a slot
node {baseDir}/scripts/manage-config.mjs remove-slot --name evening
```

## Query History

```bash
# View a specific push
node {baseDir}/scripts/query.mjs pushes --date 2026-03-06 --slot <name>

# View all pushes for a date
node {baseDir}/scripts/query.mjs pushes --date 2026-03-06

# View feedback
node {baseDir}/scripts/query.mjs feedback --date 2026-03-06 --slot <name>

# Search by keyword across recent pushes
node {baseDir}/scripts/query.mjs search --keyword "bitcoin" --days 7
```

## API Usage Tracking

```bash
# Today's usage breakdown by slot
node {baseDir}/scripts/track-usage.mjs today

# Current month's total usage
node {baseDir}/scripts/track-usage.mjs monthly

# Monthly forecast
node {baseDir}/scripts/track-usage.mjs forecast
```

Usage is recorded automatically when `store-push.mjs` receives a `usage` field.

## Feedback Iteration Strategy

Before each push, review feedback from the past 3 days. Adjust behavior based on patterns:

| Feedback Pattern | Adjustment |
|------------------|------------|
| "Too brief" on summaries | Increase summary detail, aim for upper end of summary_length |
| "More about X topic" | Add X-related keywords via `manage-config.mjs set-slot` |
| "Less about Y" | Remove or deprioritize Y keywords |
| "Timing too early/late" | Update slot time via `manage-config.mjs set-slot --name <name> --time <HH:MM>` |
| "Wrong category" | Refine topic matching rules |
| "Liked this item" | Boost similar content sources/authors |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TAVILY_API_KEY` | Yes | Tavily Search API key. Get from https://tavily.com |
| `XPOZ_API_KEY` | Recommended | Xpoz MCP service key. If missing, Twitter source is skipped gracefully. |
| `NEWS_DIGEST_DATA_DIR` | No | Data storage directory. Default: `{baseDir}/data/` |

## Notes

- All scripts output Markdown for easy parsing.
- Scripts use only Node.js built-in APIs (no npm dependencies).
- Tavily search and extract are built into this skill — no need to install `tavily-search` separately.
- If Xpoz MCP is unavailable, degrade gracefully by relying on Tavily + HN.
- Store every push for traceability. Never skip the storage step.
- Feedback is the primary mechanism for quality improvement. Always check before pushing.
- **Schedule and topics are user-defined.** Always read config before pushing. Never assume slots exist.
