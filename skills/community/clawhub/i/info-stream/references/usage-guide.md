# Beginner Usage Guide

## What This Skill Does

Teaches your AI assistant to automatically collect, curate, and deliver a daily news digest for any topic/domain.

## Quick Start (4 Steps)

### Step 1: Get a Tavily API Key (Free)

1. Go to tavily.com and sign up with your email (1 minute)
2. Copy your API Key from the Dashboard
3. Free tier: 1000 searches/month — enough for daily use

### Step 2: Send the Skill to Your AI

Send `daily-news-collector.skill` to your AI assistant (OpenClaw, Claude, ChatGPT, etc.) and say:

> "Extract this skill and set up a daily [YOUR TOPIC] news digest for me."

Replace `[YOUR TOPIC]` with your domain:
- "frontend development" / "web development"
- "AI and machine learning"
- "blockchain and crypto"
- "gaming industry"
- "automotive tech"
- Any topic you're interested in

### Step 3: Your AI Will Configure Everything

The AI will:
1. Set up your Tavily API Key as an environment variable
2. Create two scheduled tasks (cron jobs):
   - **Morning collection**: Search news → Save to file
   - **Delivery**: Read file → Send to your chat
3. Customize keywords and sources for your domain

### Step 4: Receive Daily Digests ✅

That's it. Your AI will automatically deliver a daily digest every morning.

## For OpenClaw Users

Tell your AI:

> "Read daily-news-collector.skill, then create two cron jobs:
> 1. Collect [YOUR TOPIC] news daily at 7:00 AM
> 2. Push the digest to this chat at 8:00 AM"

The AI will:
- Read SKILL.md for the methodology
- Use scripts/tavily-search.js for searching
- Reference sources.md for information sources
- Set up cron jobs automatically

## FAQ

**Q: Can I skip Tavily and use something else?**
A: Yes. SKILL.md includes a pure web_fetch approach. It's slower but works without any API key.

**Q: Is the free tier enough?**
A: Yes. 7 search groups × 30 days = 210 searches/month. Free tier gives 1000.

**Q: Can I use this for non-tech topics?**
A: Absolutely. Just change the keywords. Works for parenting, fitness, investing, cooking, anything.

**Q: How good are the search results?**
A: Tavily returns relevance scores of 0.85-0.99, which is very high quality.

**Q: What if I already have another search API?**
A: You can replace Tavily with Brave Search, SerpAPI, or any search API. The methodology stays the same — just swap the search layer.

**Q: Can I get more than 10 stories per day?**
A: Yes. Change the selection count in the cron prompt. But we recommend quality over quantity.

## Core Design Principles

### Three-Layer Source Model (No Single Point of Failure)
- **AI Search (80%)** — Fast, broad coverage
- **Technical Blogs (20%)** — Deep, authoritative content
- **Community Aggregators** — Trend sensing

### Collection-Distribution Separation
- **Night/Morning**: Slow search → Save to file
- **Morning**: Read file → Instant push
- **User experience**: Immediate delivery

### Anti-Duplication
- Collection checks if today's report already exists before writing
- Distribution is read-only
- Two tasks have strict division of labor

## Customization Tips

### Changing Search Frequency
Edit the cron schedule in your AI's configuration:
- Every 12 hours: `0 7,19 * * *`
- Weekdays only: `0 7 * * 1-5`
- Three times daily: `0 7,12,18 * * *`

### Adding/Removing Sources
Edit `references/sources.md` to add or remove information sources for your domain.

### Adjusting Output Length
In the collection cron prompt, change:
- `精选最优质 10 条` → `精选最优质 15 条` (more stories)
- `2-3句详细描述` → `1-2句简短描述` (shorter descriptions)
