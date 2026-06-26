---
name: news-express
description: Use this skill when users ask for news updates, daily briefings, or what's happening in the world.
---

# News Express

## Overview

Use this skill when users ask for news updates, daily briefings, or what's happening in the world. Fetches news from reliable international and Chinese RSS feeds, **requiring no API keys**. Simply use the `web_fetch` tool to read RSS XML directly.

## Trigger Scenarios

- User asks "what's the news today", "latest updates", "daily briefing"
- User asks "what's happening domestically/internationally"
- User requests categorized news such as technology, finance, sports
- User asks for "morning briefing", "evening briefing", "news summary"

## RSS Feeds

### 🇨🇳 Domestic Sources

| Source | Category | URL |
|------|------|-----|
| 36Kr | Latest Flash News | `https://36kr.com/feed-newsflash` |
| Solidot | Technology | `https://www.solidot.org/index.rss` |
| SSPAI | Technology/Digital | `https://sspai.com/feed` |
| IThome | AI/Technology/Digital | `https://www.ithome.com/rss/` |
| Zhidx | Flash News/Headlines/AI/Robotics | `https://zhidx.com/rss` |
| ITJuzi | Finance | `https://www.itjuzi.com/api/telegraph.xml` |
| cnBeta | AI/Technology/Digital | `https://plink.anyfeeder.com/cnbeta` |
| Odaily | Flash News | `https://rss.odaily.news/rss/newsflash` |
| People's Daily | Headlines | `http://www.people.com.cn/rss/politics.xml` |

### 🌍 International Sources

| Source | Category | URL |
|------|------|-----|
| OpenAI | AI | `https://openai.com/news/rss.xml` |
| NPR | United States | `https://feeds.npr.org/1001/rss.xml` |
| Hacker News | Technology | `https://hnrss.org/frontpage` |
| PANews | Flash News | `https://www.panewslab.com/rss.xml?lang=en&type=NEWS&featured=true` |
| ArXiv | AI | `https://rss.arxiv.org/rss/cs.AI` |
| China Daily | English/International | `https://www.chinadaily.com.cn/rss/china_rss.xml` |
| TechCrunch | Technology | `https://techcrunch.com/feed/` |

## Workflow

### Step 1: Fetch RSS Content

Use the `web_fetch` tool to read RSS XML directly:

```
web_fetch(url="https://openai.com/news/rss.xml")
```

### Step 2: Parse Headlines

In the RSS XML structure, news headlines are within `<title>` tags, summaries within `<description>` tags, and links within `<link>` tags. Simply extract them from the markdown text returned by `web_fetch`.

### Step 3: Compile and Output

Organize by domestic and international categories, taking 6-8 items each, outputting each headline with a concise summary.

## Output Format

```
📰 [Latest News]
🗓️ [Date] · [Day of Week]

---

## 🇨🇳 Domestic

• [Headline 1] 
[Summary 1]
• [Headline 2] 
[Summary 2]
• [Headline 3] 
[Summary 3]
...

---

## 🌍 International

• [Headline 1] 
[Summary 1]
• [Headline 2] 
[Summary 2]
• [Headline 3] 
[Summary 3]
...

---
Data Source: RSS Feeds
```

## Important Notes

- **No API Key Required**: All data is obtained through public RSS feeds
- **Some domestic sources may require proper network access**: If access fails, automatically switch to backup sources
- **Content Timeliness**: RSS typically updates every 15-60 minutes
- **Language**: Domestic sources output in Chinese, international sources can be bilingual (Chinese/English)