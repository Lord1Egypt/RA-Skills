---
name: ai-news-oracle
description: Fetch real-time AI news briefings powered by SkillBoss API Hub (Hacker News, TechCrunch, The Verge). Uses SkillBoss search and chat capabilities for news aggregation and summarization.
author: swimmingkiim
version: 1.0.0
requires.env: [SKILLBOSS_API_KEY]
---

> 📖 **Complete setup guide**: https://skillboss.co/skill.md


# AI News Oracle Skill

> **"The fastest way for autonomous agents to stay updated on AI trends without browsing the web."**

This skill connects your agent to the **AI News Oracle**, powered by **SkillBoss API Hub**. It monitors top AI news sources (Hacker News, TechCrunch, The Verge), summarizes them using SkillBoss's chat capability, and delivers a concise, hallucination-free briefing JSON.

## Features

- **Real-time Monitoring**: Aggregates news from trusted tech sources via SkillBoss search API.
- **AI-Powered Summary**: Uses SkillBoss API Hub's chat capability to generate consistent, agent-friendly summaries.
- **Unified API**: Single `SKILLBOSS_API_KEY` for all capabilities via `https://api.skillboss.co/v1/pilot`.

## Tools

### `ai_news_briefing`

Fetches the latest AI news briefing. Returns a structured summary with timestamps and source links.

**Parameters:**
- (None) - Just call the tool to get the latest briefing.

**Example Output:**
```text
AI News Briefing (2026-02-10 06:46:22)

- Open source AI is the path forward (Meta)
- Anthropic closes in on $20B round
- ChatGPT rolls out ads in free tier

Source: AI News Oracle via SkillBoss API Hub
```

## Installation

Using OpenClaw CLI:
```bash
openclaw install skill https://github.com/swimmingkiim/openclaw-skill-ai-news-oracle
```

## Usage

```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.skillboss.co/v1"

def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()

# Step 1: Search for latest AI news
search_result = pilot({
    "type": "search",
    "inputs": {"query": "latest AI news today"},
    "prefer": "balanced"
})
news_raw = search_result["result"]

# Step 2: Summarize with LLM via SkillBoss chat
summary_result = pilot({
    "type": "chat",
    "inputs": {
        "messages": [
            {"role": "system", "content": "You are an AI news summarizer. Return a concise bullet-point briefing."},
            {"role": "user", "content": f"Summarize these AI news results:\n{news_raw}"}
        ]
    },
    "prefer": "balanced"
})
briefing = summary_result["result"]["choices"][0]["message"]["content"]
print(briefing)
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SKILLBOSS_API_KEY` | SkillBoss API Hub authentication key |

## Links
- **API Hub**: `https://api.skillboss.co/v1/pilot`
- **Developer**: [swimmingkiim](https://github.com/swimmingkiim)
