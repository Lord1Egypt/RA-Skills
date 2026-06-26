---
name: linkedin-prospector
description: "Score LinkedIn prospects by signal strength (0-3). Detect high-intent leads: new job, funding, recent post, active hiring. Free skill - full outreach methodology pack at openclaw-courses-fawn.vercel.app"
homepage: https://openclaw-courses-fawn.vercel.app
author: "Romain Rabreau"
license: MIT-0
tags:
  - linkedin
  - prospecting
  - lead-generation
  - sales
  - outreach
version: 1.2.0
---

# LinkedIn Prospector

Score LinkedIn prospects by signal strength before reaching out.

This skill helps your OpenClaw agent evaluate whether a prospect is worth contacting right now - based on observable signals, not guessing.

## What this skill does

Your agent reads a prospect list and assigns each person a score:

**Score 3 - Contact now:**
- New job in last 90 days AND your offer is relevant to their role
- Company raised funding in last 6 months
- Published a post in last 7 days that relates to your offer
- Actively hiring for roles that indicate a problem you can solve

**Score 2 - Optional:**
- Weaker versions of the above (older signals, indirect relevance)

**Score 0-1 - Skip:**
- No detectable signal
- Skipping score 0-1 prospects is the main reason high-performing outreach works

## How to use

Load this skill into your OpenClaw agent:

```
SKILL signal-lead-finder.md
```

Then give your agent a prospect list (CSV or plain text with first name, LinkedIn URL, company, title).

Ask:
```
"Review this prospect list. Apply signal-lead-finder.md. 
Score each person 0-3. Sort by score descending. 
Show me the top 10 with their specific signals."
```

Your agent will then draft outreach messages only for score-3 prospects (if you use outreach-sequence.md from the full pack).

## What this skill does NOT do

This is a scoring and decision framework, not a browser automation tool. Your agent reads context (prospect info you provide) and applies the scoring rules. It does not log into LinkedIn or send messages automatically - any message sending uses your agent's normal capabilities and requires your review.

## Scoring rules

The agent applies this logic:

```
Signal check:
- New job (<90 days): +2 if role matches your ICP
- Funding (<6 months): +2 if company stage matches  
- Recent post (<7 days): +1 if topic overlaps with your offer
- Active hiring: +1 if roles indicate the problem you solve

Score 3: multiple strong signals, contact now
Score 2: single weak signal, optional
Score 0-1: no signal, skip
```

## Why signal scoring matters

Outreach without signal scoring gets 3-5% reply rate (industry average).
Outreach with signal scoring gets 25-35%+ reply rate.

The difference is not the message quality. It is whether the person has a reason to care right now.

## Full methodology pack

This is the free signal-scoring skill. The full pack includes:

1. signal-lead-finder.md (this file)
2. outreach-sequence.md - message structure and follow-up timing rules
3. message-quality-check.md - quality scoring (0-5) before sending
4. setup-course.md - ICP definition, list building, campaign setup
5. winning-examples.md - 10 annotated message examples with scores
6. sales-fundamentals.md - the 70/30 rule and forbidden words

Full pack: https://openclaw-courses-fawn.vercel.app - €14.99, delivered by email.

---

Built by Romain Rabreau, founder of Recon0x. Contact: romain@recon0x.com
