---
name: google-alerts
description: "Monitor keywords via free web search. Use when: (1) Tracking brand or product mentions, (2) Monitoring industry keywords, (3) Researching competitors and market trends, (4) Daily competitive intel reports. Creates Hootsuite-style formatted output from search results."
metadata:
  openclaw:
    requires:
      env:
        - GOOGLE_ALERT_FEED_ID
      bins:
        - bash
        - curl
        - python3
---

# Google Alerts Monitor

Keyword monitoring with Hootsuite-style output. Free, no API keys required.

## What This Skill Does

- Fetches Google Alerts RSS feeds for your keywords
- Formats results into visual, social-media-style cards
- Prints clean JSON output and formatted text for use by agents or cron jobs

**What this skill does NOT do:** It does not save files, schedule cron jobs, or post to chat. Those integrations are handled by your agent prompt or external automation.

## Keywords

Edit `references/keywords.md` with your own keywords. One per line.

## Search Script

```bash
# Set your Google Alert feed ID (see setup-guide.md)
export GOOGLE_ALERT_FEED_ID="your_feed_id_here"

# Search a keyword
bash scripts/search.sh "your keyword" 10
```

Output: JSON array of results (title, link, description, published date)

## Formatter Script

Takes JSON results and formats them into Hootsuite-style cards:

```bash
bash scripts/search.sh "your keyword" 10 \
  | python3 scripts/format-results.py --term "your keyword" --source google --count 10
```

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 YOUR KEYWORD — GOOGLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Result Title · 3h ago
"Description text preview truncated to 280 chars..."
↗️ https://example.com/link
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Setup

1. Create Google Alerts at [google.com/alerts](https://www.google.com/alerts)
2. Get the RSS feed ID from each alert's feed URL
3. Set `GOOGLE_ALERT_FEED_ID` in your environment or edit `scripts/search.sh`
4. See `references/setup-guide.md` for details

## Scripts

- `scripts/search.sh` — Fetch Google Alerts RSS, output JSON
- `scripts/format-results.py` — Format JSON results as Hootsuite-style cards

## References

- `references/keywords.md` — Keyword definitions
- `references/setup-guide.md` — Detailed setup instructions
