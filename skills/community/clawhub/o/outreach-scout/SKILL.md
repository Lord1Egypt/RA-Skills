---
name: outreach-scout
description: Find and engage warm leads on Reddit, X/Twitter, and forums. Monitors platforms for people asking questions your product solves, drafts helpful replies that naturally mention your offering, and tracks all activity. Use when you need marketing, lead generation, audience building, finding potential customers, or growing product awareness. Works with heartbeats for automated daily scouting.
---

# Outreach Scout

Find people who already need what you're selling. Draft replies that help first, sell second.

## Quick Start

1. Create a scout config file at `life/areas/outreach/scout-config.md` using the template in `{baseDir}/assets/scout-config-template.md`
2. Create the tracking log at `life/areas/outreach/scout-log.md` using `{baseDir}/assets/scout-log-template.md`
3. Run a scout session (see workflow below)

## Core Workflow

### Manual Scout (on-demand)

When asked to scout, find leads, or do outreach:

1. **Read config** — load `life/areas/outreach/scout-config.md` for targets, keywords, and products
2. **Search** — run platform searches (see Search Patterns below)
3. **Filter** — check `life/areas/outreach/scout-log.md` to skip already-seen threads
4. **Analyze** — for each promising result, fetch the thread and assess:
   - Is someone asking a question your product answers?
   - Is the thread recent enough to engage? (< 48 hours ideal, < 7 days acceptable)
   - Is there already a good answer? (if yes, skip unless you can add genuine value)
5. **Draft replies** — write helpful responses following the Reply Guidelines below
6. **Present to user** — show the leads and draft replies for approval
7. **Log** — record all found threads in the scout log (whether engaged or skipped)

### Heartbeat Scout (automated)

Add to your HEARTBEAT.md:
```
## Outreach Scout
- Run a scout sweep during daytime heartbeats (max 1x per 4 hours)
- Present any new leads found
- Skip if last scout was < 4 hours ago (check scout-log.md timestamps)
```

During heartbeat: run the scout workflow, but only present results if you find something worth engaging. Don't message the user just to say "no leads found."

## Search Patterns

### Reddit
Use `web_search` with these query patterns:
```
site:reddit.com "[keyword]" after:[date]
site:reddit.com/r/[subreddit] "[keyword]"
```

Search for:
- Direct questions: "how do I [thing your product does]"
- Frustration signals: "struggling with", "can't figure out", "anyone know how to"
- Recommendation requests: "best way to", "what do you use for", "recommendations for"
- Comparison threads: "[competitor] vs", "alternative to"

### X/Twitter
Use `web_search` with:
```
site:x.com "[keyword]" OR site:twitter.com "[keyword]"
```

Search for:
- Questions and complaints about problems you solve
- "Anyone know a good..." requests
- Build-in-public threads in your niche

### Forums & Communities
Use `web_search` with:
```
"[keyword]" site:discord.com OR site:community.[domain] OR site:forum.[domain]
```

### General Web
```
"[keyword]" "[problem phrase]" -site:youtube.com
```

## Reply Guidelines

**The golden rule: Be genuinely helpful. The mention of your product is the side dish, not the main course.**

### Structure of a good reply
1. **Acknowledge their problem** — show you understand what they're dealing with
2. **Give real help** — answer their question or share useful info (this is the bulk of the reply)
3. **Natural mention** — if relevant, mention your product/skill as one option among several
4. **No hard sell** — no "BUY NOW", no affiliate links, no pressure

### What makes a reply feel genuine vs spammy

**Genuine:**
> "I ran into the same issue setting up memory persistence. What worked for me was a 3-layer system — daily notes for raw logs, a knowledge graph for durable stuff, and a tacit knowledge file for preferences/lessons. I actually packaged this as a free skill on ClawHub (para-memory) if you want to skip the setup."

**Spammy:**
> "Check out para-memory on ClawHub! It solves exactly this problem! 🚀🔥"

### Platform-specific guidelines
See `{baseDir}/references/platform-tips.md` for Reddit, X, and Discord etiquette.

### Reply tone
- Match the platform's culture (Reddit is more technical, X is more casual)
- Be concise — long replies get skipped
- Include specific details that show you actually know what you're talking about
- If you can't add genuine value, don't reply

## Tracking

The scout log (`life/areas/outreach/scout-log.md`) tracks:
- Date and time of each scout session
- Threads found (URL, platform, relevance score)
- Action taken (replied, skipped, saved for later)
- Results (if known — upvotes, replies, clicks)

This prevents double-engaging threads and helps identify which platforms/keywords produce the best leads.

## Metrics

Track weekly in the scout log:
- **Threads found** — total leads discovered
- **Threads engaged** — replies posted
- **Response rate** — replies that got positive engagement
- **Conversions** — any clicks/sales that traced back to outreach

## Advanced: Multi-Product Scouting

If you have multiple products, the config supports listing several. The scout will match threads to the most relevant product and tailor the reply accordingly.

## Credits

Built by Kai @ KaiShips — kaiships.com
