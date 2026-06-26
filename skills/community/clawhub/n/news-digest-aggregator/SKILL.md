---
name: news-digest-aggregator
description: Daily automated news digest that fetches RSS feeds, aggregates articles using LLM summarization, and delivers formatted digests to messaging channels (Discord/Slack/Feishu) on a schedule. Use when user wants daily news summaries, RSS aggregation, or scheduled content delivery.
---

# News Digest Aggregator

Automated daily news digest system that collects articles from RSS feeds, summarizes them using LLM, and delivers formatted digests to your preferred messaging channel.

## Quick Start

1. Configure RSS sources in `references/sources.json`
2. Set up channel credentials in environment variables
3. Run `scripts/fetch_and_digest.py` manually or schedule with cron

## Configuration

### RSS Sources

Edit `references/sources.json`:
```json
{
  "sources": [
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "category": "tech"},
    {"name": "Reuters", "url": "https://www.reutersagency.com/feed/?taxonomy=markets&post_type=reuters-best", "category": "finance"}
  ]
}
```

### Channel Settings

Set environment variables for your target channel:

**Discord:**
```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
```

**Slack:**
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

**Feishu:**
```bash
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/..."
```

## Usage

### Manual Run
```bash
python scripts/fetch_and_digest.py --config references/sources.json --channel discord
```

### Scheduled (Cron)
```bash
# Daily at 9 AM
0 9 * * * cd /path/to/skill && python scripts/fetch_and_digest.py --config references/sources.json --channel discord
```

## Output Format

The digest includes:
- 📅 Date header
- 📊 Summary statistics (total articles, sources)
- 🏷️ Categorized sections
- 🔗 Article links with brief summaries

## Customization

- **Max articles per source**: Edit `MAX_ARTICLES` in the script (default: 5)
- **Summary length**: Adjust `SUMMARY_MAX_TOKENS` (default: 150)
- **Categories**: Modify category tags in sources.json
