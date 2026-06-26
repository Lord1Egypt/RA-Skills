---
name: local-lead-outreach-engine
description: Build qualified B2B lead shortlists and practical cold outreach sequences for agencies, consultants, freelancers, SaaS founders, and service businesses. Use when the user wants to find prospects, qualify leads, prioritize outreach targets, write cold emails, create follow-up sequences, prepare a send batch, or turn a rough offer into prospect-specific outreach.
---

# Local Lead Outreach Engine

Use this skill to turn a seller's offer into a small, qualified outreach batch with clear reasoning and ready-to-review emails.

## Core Principles

Prefer quality over volume. Produce 10 strong leads before 100 weak ones.

Ground every recommendation in observable evidence. Never invent revenue, headcount, budget, pain, technology, intent, or contact details.

Write like a useful human, not a sales automation tool. Keep copy specific, short, plain, and low-pressure.

Do not send, schedule, upload, or automate outreach unless the user explicitly asks and approves the exact recipients and copy.

## First Step

If the user's offer or target market is unclear, ask only for the missing essentials:

- what they sell
- who they want to sell to
- geography or niche
- minimum deal size or target monthly value
- any exclusions

If the user already provides enough context, proceed.

## Workflow

1. Clarify the offer in one sentence.
2. Define the best-fit ICP and disqualifiers.
3. Build or clean a lead list using the user's data, web research, CRM export, spreadsheet, or pasted prospects.
4. Score each prospect using fit, urgency signals, reachable contact route, likely budget, and relevance to the offer.
5. Select a small send batch.
6. Create a first email plus 2-4 follow-ups.
7. Provide a send-readiness check before any outreach action.

## Lead Qualification

Score leads from 1-5:

- 5 = strong fit, clear pain signal, reachable decision-maker or official contact, likely budget
- 4 = good fit with one missing signal
- 3 = plausible but needs more research or weaker timing
- 2 = weak fit, unclear buyer, low urgency, or poor contact route
- 1 = exclude

Prioritize leads with:

- clear recurring need for the user's service
- outdated, broken, inconsistent, or underperforming public assets
- recent launches, hiring, expansion, events, funding, new locations, or active campaigns
- visible owner, founder, marketing lead, operations lead, or department contact
- evidence they already spend money on the problem area

Disqualify leads with:

- no realistic ability to buy
- no clean contact route
- unrelated niche
- obvious legal, ethical, or brand risk
- prior opt-out, bounce, complaint, or "not interested" status when known

For more detailed scoring rules, read `references/icp-scoring.md`.

## Outreach Copy

Write emails with:

- subject line under 7 words
- 80-140 words for the first email
- one clear reason for contacting them
- one specific observed signal
- one simple offer
- one low-friction CTA
- no hype, false urgency, fake familiarity, or exaggerated claims

Default CTA examples:

- "Worth me sending over a quick idea?"
- "Should I send the 3 things I noticed?"
- "Would a short example be useful?"
- "Is this worth a quick look?"

For copy patterns, follow-up rules, and anti-spam checks, read `references/outreach-copy.md`.

## Compliance And Safety

Use publicly available business contact information only unless the user provides a lawful first-party list.

Always include opt-out language when preparing production-ready cold email.

Do not help bypass consent, hide sender identity, evade spam filters, scrape behind logins, or target private individuals at home.

For practical compliance guardrails, read `references/safety-and-compliance.md`.

## Output Formats

For lead lists, output a table with:

- company
- website
- location
- segment
- contact route
- evidence observed
- fit score
- recommended angle
- risk or missing info

For a send batch, output:

- chosen recipients
- why each was selected
- first email
- follow-up sequence
- personalization notes
- send-readiness checklist

## Quality Bar

Before finishing, check:

- every lead has a reason tied to the offer
- every email could only plausibly be for that recipient or segment
- no claim appears without evidence
- weak leads are marked as research-only or excluded
- the user can copy the output into their sending workflow without rewriting everything
