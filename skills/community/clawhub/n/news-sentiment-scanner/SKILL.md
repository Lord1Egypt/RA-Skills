---
name: news-sentiment-scanner
description: "Scan news sources and RSS feeds for events that could move prediction market prices. Score headlines for market impact, flag urgent stories, and cross-reference with active markets. Use when asked about breaking news, market-moving events, or news sentiment."
metadata:
  openclaw:
    emoji: "📰"
    requires:
      bins: ["curl", "jq", "python3"]
---

# News Sentiment Scanner

Scan news and RSS feeds for market-moving events, score headline sentiment, and flag prediction market trading opportunities.

## When to Use

Use this skill when the user asks about:
- Breaking news that could affect prediction markets
- Scanning news for trading opportunities
- Sentiment analysis of current headlines
- Market-moving events in sports, politics, or economics
- News-driven trading signals
- Whether any recent news affects open positions

## RSS Feed Sources

Default feeds covering key prediction market verticals:

| Vertical | Feed URL |
|----------|----------|
| General Breaking | https://feeds.apnews.com/rss/apf-topnews |
| World News | https://feeds.reuters.com/reuters/topNews |
| US Politics | https://feeds.apnews.com/rss/apf-politics |
| Sports | https://www.espn.com/espn/rss/news |
| Economics | https://feeds.reuters.com/reuters/businessNews |
| Crypto | https://cointelegraph.com/rss |

The agent may add or substitute feeds based on context (e.g., if the user trades sports markets, prioritize ESPN).

## Operations

### 1. Scan RSS Feeds for Headlines

Fetch the latest headlines from all configured feeds:

```bash
for FEED_URL in \
  "https://feeds.apnews.com/rss/apf-topnews" \
  "https://feeds.reuters.com/reuters/topNews" \
  "https://feeds.apnews.com/rss/apf-politics" \
  "https://www.espn.com/espn/rss/news" \
  "https://feeds.reuters.com/reuters/businessNews" \
  "https://cointelegraph.com/rss"; do
  curl -s "$FEED_URL" | python3 -c "
import sys, xml.etree.ElementTree as ET
from datetime import datetime, timezone
try:
    tree = ET.parse(sys.stdin)
    root = tree.getroot()
    source = root.find('.//channel/title')
    src = source.text if source is not None else 'Unknown'
    for item in root.findall('.//item')[:10]:
        title = item.find('title')
        link = item.find('link')
        pub = item.find('pubDate')
        t = title.text if title is not None else ''
        l = link.text if link is not None else ''
        p = pub.text if pub is not None else ''
        print(f'{src}|{t}|{l}|{p}')
except: pass
"
done

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-news-sentiment-scanner-skill/](https://agentbets.ai/guides/openclaw-news-sentiment-scanner-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
