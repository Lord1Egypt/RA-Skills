---
name: daily-news-discord
description: >
  Delivers a daily news digest to a Discord channel via webhook. Use this skill
  whenever the user wants to: send today's news to Discord, set up an automated
  daily news briefing, post AI/tech headlines to a Discord server, configure a
  news bot for Discord, or get a morning digest of top stories. Trigger even if
  the user says things like "news to discord", "daily briefing", "morning headlines",
  or "news bot". This skill handles both one-off sends and recurring scheduled deliveries.
---

# Daily News → Discord

This skill fetches the top news stories for the day and delivers them to a Discord
channel via webhook as a clean, readable embed.

## Configuration

These values are baked into the scheduled task but can be overridden at runtime:

| Setting | Default |
|---|---|
| **Webhook URL** | Set in scheduled task |
| **Topics** | AI & Tech |
| **Stories** | 5 headlines |
| **Schedule** | 8:00 AM daily |

---

## Execution Steps

### 1. Get today's date
Run a quick bash command to get the current date in a friendly format:
```bash
date "+%A, %B %-d, %Y"
```

### 2. Search for news
Perform 2–3 targeted web searches to find today's top stories on the configured topics.
Use searches like:
- `"AI news today [current month year]"`
- `"tech news [current date]"`
- `"[specific topic] latest developments [month year]"`

Pick the **5 most newsworthy, distinct, and recent** stories. Prefer stories from the
last 24–48 hours. Skip duplicate coverage of the same event.

### 3. Build the stories JSON
Format the 5 stories as a JSON array. Each story needs:
```json
[
  {
    "headline": "Short, clear headline (max 80 chars)",
    "summary": "One to two sentence summary of what happened and why it matters. (max 250 chars)",
    "url": "https://source-article-url.com"
  }
]
```

Keep summaries punchy and informative — no filler phrases like "In a world where...".

### 4. Send to Discord
Call the bundled send script with the stories JSON, date, and topics:

```bash
python3 "$(dirname "$0")/scripts/send_to_discord.py" \
  --webhook "WEBHOOK_URL_HERE" \
  --date "DATE_STRING" \
  --topics "AI & Tech" \
  --stories 'STORIES_JSON_HERE'
```

Replace placeholders with actual values. Pass the stories JSON as a single-quoted
string. If the JSON contains single quotes, use a temp file instead:

```bash
echo 'STORIES_JSON' > /tmp/stories.json
python3 scripts/send_to_discord.py --webhook "..." --date "..." --topics "..." --stories-file /tmp/stories.json
```

### 5. Confirm delivery
The script prints the HTTP status code. A `204` means success. If it fails, inspect
the error output and retry once (Discord webhooks occasionally return 429 rate limits —
wait 2 seconds and retry).

---

## Discord Message Format

The message is sent as a rich embed:

```
📰 Daily News Digest — Monday, March 6, 2026
Today's top stories in AI & Tech

1. OpenAI Releases New Reasoning Model
   GPT-5 now available to all users with improved reasoning...
   [Read more]

2. ...
...
──────────────────────────────
OpenClaw Daily News • Powered by Claude
```

---

## Customization

To change topics, edit the `--topics` argument in the scheduled task prompt and adjust
the search queries in Step 2. Topics can be comma-separated: `"AI, Finance, Science"`.
