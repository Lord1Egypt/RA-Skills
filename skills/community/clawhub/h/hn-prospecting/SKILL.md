---
name: hn-prospecting
description: Find high-intent leads on Hacker News via the free Algolia API — no API key needed. Score posts, surface Ask HN threads, and identify technical founders actively seeking tools.
version: 1.0.0
author: ModelFitAI <skills@modelfitai.com>
license: MIT
keywords: [openclaw, skill, hackernews, hn, lead-gen, prospecting, sales, founders]
requires: {}
---

# Hacker News Prospecting Skill

Find warm leads in Hacker News threads — technical founders and buyers actively seeking tools. Uses the **free Algolia HN Search API** — no API key, no credentials, no rate limits worth worrying about.

## How It Works

The HN Algolia API (`hn.algolia.com`) provides full-text search over all HN content — stories, Ask HN threads, and comments — completely free with no auth. This skill searches for buying-intent posts and scores them by lead quality.

## Commands

Run with Node.js: `node {baseDir}/hn-prospecting.js <command> [args]`

- **search `<keyword>`** — Find high-intent HN posts mentioning your keyword
- **ask** — Find recent "Ask HN" threads (best for tool discovery opportunities)
- **front** — Get current front page stories (trending technical discussions)
- **score** — Score an HN post for lead quality

## Usage

```bash
node {baseDir}/hn-prospecting.js search "looking for AI agent tool"
node {baseDir}/hn-prospecting.js search "alternative to Zapier"
node {baseDir}/hn-prospecting.js ask "lead generation"
node {baseDir}/hn-prospecting.js front
node {baseDir}/hn-prospecting.js score --title "Ask HN: What do you use for outreach?" --points 45 --comments 32
```

## Environment Variables

None required. The HN Algolia API is fully public.

## Why HN?

HN readers are disproportionately technical founders, early adopters, and decision-makers — the exact ICP for most B2B SaaS tools. "Ask HN: What tools do you use for X?" threads are goldmines for qualified lead discovery.
