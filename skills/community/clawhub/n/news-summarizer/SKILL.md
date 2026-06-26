---
name: news-summary
description: >
  Fetch and summarize world news from BBC, Reuters, NPR RSS feeds. Can create voice summaries.
  USE WHEN: "What's happening in the world?", daily briefings, general news updates, current events.
  DON'T USE: Stock/market news (use stock-analysis), weather (use weather skill), sports scores, stock-specific company news.
---

# News Summary

## Overview

Fetch and summarize news from trusted international sources via RSS feeds.

## When NOT to Use This Skill

❌ "What's happening with NVDA stock?" → Use **stock-analysis** skill
❌ "What's the weather in Warren NJ?" → Use **weather** skill  
❌ "Summarize this YouTube video" → Use **summarize** skill
❌ "What are people saying on Twitter about X?" → Use **bird** skill
❌ "Give me sports scores" → Use web_search directly

## RSS Feeds

### BBC (Primary)
```bash
# World news
curl -s "https://feeds.bbci.co.uk/news/world/rss.xml"

# Top stories
curl -s "https://feeds.bbci.co.uk/news/rss.xml"

# Business
curl -s "https://feeds.bbci.co.uk/news/business/rss.xml"

# Technology
curl -s "https://feeds.bbci.co.uk/news/technology/rss.xml"

# Asia (good for India/South Asia coverage)
curl -s "https://feeds.bbci.co.uk/news/world/asia/rss.xml"
```

### Reuters
```bash
# World news
curl -s "https://www.reutersagency.com/feed/?best-regions=world&post_type=best"
```

### NPR (US perspective)
```bash
curl -s "https://feeds.npr.org/1001/rss.xml"
```

### The Hindu (India)
```bash
curl -s "https://www.thehindu.com/news/national/feeder/default.rss"
```

## Parse RSS

Extract titles and descriptions:
```bash
curl -s "https://feeds.bbci.co.uk/news/world/rss.xml" | \
  grep -E "<title>|<description>" | \
  sed 's/<[^>]*>//g' | \
  sed 's/^[ \t]*//' | \
  head -30
```

## Workflow

### Text summary
1. Fetch BBC world headlines
2. Optionally supplement with Reuters/NPR
3. Summarize key stories
4. Group by region or topic

### Voice summary
1. Create text summary
2. Generate voice with OpenAI TTS
3. Send as audio message

```bash
curl -s https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1-hd",
    "input": "<news summary text>",
    "voice": "onyx",
    "speed": 0.95
  }' \
  --output /tmp/news.mp3
```

## Example Output Format

```
📰 News Summary [date]

🌍 WORLD
- [headline 1]
- [headline 2]

💼 BUSINESS
- [headline 1]

💻 TECH
- [headline 1]
```

## Best Practices

- Keep summaries concise (5-8 top stories)
- Prioritize breaking news and major events
- For voice: ~2 minutes max
- Balance perspectives (Western + Indian/Asia)
- Cite source if asked
