---
name: project-ghost
version: 2.0.0
description: Web reading layer for AI agents. Convert any public URL into structured intelligence — entities, business intent, confidence score — in one API call.
tags: [web, scraping, research, intelligence, agents, api, data-extraction]
author: Sid890-cpu
homepage: https://project-ghost-lilac.vercel.app
repository: https://github.com/Sid890-cpu/project-ghost
license: MIT
runtime:
  env:
    - name: GHOST_API_KEY
      description: Your Ghost API key. Get one free at project-ghost-lilac.vercel.app
      required: true
      secret: true
---

# Project Ghost

Web reading layer for AI agents. Convert any public URL into structured, agent-ready intelligence in one API call.

## What it does

Feed Ghost any public URL and get back:
- **Business intent** — a 1-2 sentence summary of what the page is about
- **Named entities** — companies, people, products mentioned
- **Confidence score** — how reliable the extraction is (0-1)
- **Tokens saved** — how much token reduction vs raw HTML (avg 80%+)
- **Priority score** — relevance signal (1-10)

## Usage

```
Read this page and tell me what it's about: https://openai.com
```

```
Research Stripe's latest products using Ghost
```

```
What are the top stories on Hacker News right now?
```

## How to use in your agent

Set your `GHOST_API_KEY` environment variable, then call:

```bash
curl -X POST https://project-ghost-production.up.railway.app/distill \
  -H "Authorization: Bearer $GHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://apple.com"}'
```

## Response format

```json
{
  "title": "Apple",
  "tokens_saved": "80.7%",
  "signals_data": {
    "decision_signal": {
      "business_intent": "Apple promotes its latest hardware lineup...",
      "priority_score": 8,
      "category": "Technology"
    },
    "items": [
      {
        "title": "MacBook Pro with M5",
        "entities": ["Apple", "MacBook", "M5"],
        "impact_score": 9
      }
    ],
    "integrity_layer": {
      "confidence_score": 0.87,
      "is_high_integrity": true
    }
  }
}
```

## Works great with

- Research agents reading company websites
- News monitoring agents tracking topics
- Sales agents detecting buying signals
- Legal agents extracting policy terms
- Any agent that needs to understand web content

## Sites that work

Most public websites work — Wikipedia, GitHub, HackerNews, OpenAI, Stripe, Apple, Anthropic, and thousands more.

Sites with enterprise Cloudflare protection (WSJ, FT, Nike) may be blocked — the API returns a clear blocked message in that case.

## Get your free API key

Visit **project-ghost-lilac.vercel.app** → enter your email → get an instant `ghost_sk_...` key.

Free plan: 100 requests/month. No credit card needed.

## Links

- Homepage: https://project-ghost-lilac.vercel.app
- API Docs: https://project-ghost-production.up.railway.app
- GitHub: https://github.com/Sid890-cpu/project-ghost
- Integration Guide: https://project-ghost-lilac.vercel.app/integrate.html
