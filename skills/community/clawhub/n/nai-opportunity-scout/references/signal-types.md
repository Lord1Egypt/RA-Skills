# Demand Signal Types

A taxonomy of signals that indicate real, actionable market demand. Use this when
scoring findings to distinguish genuine opportunity from noise.

## Table of Contents

1. [Direct Demand Signals](#direct-demand-signals)
2. [Indirect Demand Signals](#indirect-demand-signals)
3. [Noise Signals (Filter Out)](#noise-signals)
4. [Signal Strength Indicators](#signal-strength-indicators)
5. [Examples by Signal Type](#examples)

---

## Direct Demand Signals

These explicitly state an unmet need. Highest confidence.

### 1. Explicit Wish / Feature Request

Someone directly asks for something that doesn't exist or lacks key features.

**Keyword patterns**: "I wish", "if only", "someone should build", "is there a tool
that", "looking for a way to", "need something that", "does anyone know of"

**Example (Reddit r/smallbusiness)**:
> "I wish there was an invoicing tool that just let me send a PDF and get paid.
> Every tool I try wants me to sign up for a whole ecosystem. I just want simple invoicing."

**Example (HN)**:
> "Is there a self-hosted alternative to Notion that doesn't feel like it was
> designed by committee? I want something fast and local."

**Signal strength**: HIGH — direct expression of unmet need.

### 2. Frustration / Pain Expression

Someone describes a painful experience with existing solutions.

**Keyword patterns**: "frustrated", "annoyed", "hate that", "terrible experience",
"why does every", "so tired of", "fed up with", "drives me crazy"

**Example (Reddit r/SaaS)**:
> "I'm so frustrated with Zapier pricing. I have 5 simple automations and they
> want $50/month. There has to be a better way for small operations."

**Example (Reddit r/selfhosted)**:
> "Why does every self-hosted dashboard assume you're running Kubernetes?
> I have 3 Docker containers on a Pi. I don't need Grafana."

**Signal strength**: HIGH — pain + specific problem = clear opportunity.

### 3. "Shut Up and Take My Money"

Someone explicitly states willingness to pay for a solution.

**Keyword patterns**: "I'd pay for", "shut up and take my money", "worth paying for",
"I'd switch to", "instant buy if", "take my money"

**Example (HN)**:
> "If someone built a Gmail client that was actually fast and didn't spy on me,
> I'd pay $10/month tomorrow. Fastmail is close but the UI is 2010."

**Signal strength**: VERY HIGH — validated willingness to pay. Rare but golden.

### 4. Solution Seeking

Someone actively searching for a solution, hasn't found one.

**Keyword patterns**: "has anyone solved", "how do you handle", "what do you use for",
"best way to", "anyone found a good", "recommendations for"

**Example (Reddit r/LocalLLaMA)**:
> "Has anyone found a good way to do RAG over a large codebase locally?
> Everything I've tried either chokes on context or needs cloud APIs."

**Signal strength**: MEDIUM-HIGH — demand is clear, but might have existing solutions
the poster hasn't found. Check replies for competition signals.

---

## Indirect Demand Signals

These don't directly ask for something but reveal gaps through behavior.

### 5. Workaround Description

Someone describes a hacky, manual, or fragile solution they built. This means:
the need exists, no good solution exists, they're invested enough to build something ugly.

**Keyword patterns**: "workaround", "hack", "duct tape", "jerry-rigged", "I wrote a
script that", "my current workflow is", "cobbled together", "ugly but works"

**Example (Reddit r/selfhosted)**:
> "I cobbled together a bash script that scrapes my ISP's usage page, logs it to
> a CSV, and sends me a Telegram alert when I hit 80%. Ugly but it works."

**Signal strength**: HIGH — someone invested real effort = strong unmet need.
The uglier the workaround, the bigger the opportunity.

### 6. Comparison Shopping / "Alternative To"

Someone comparing existing options and finding all lacking.

**Keyword patterns**: "alternative to", "compared to", "vs", "switching from",
"looking to replace", "moved away from", "outgrown"

**Example (Reddit r/SaaS)**:
> "I've tried Airtable, Notion, and Coda for project management and they all
> feel like Swiss Army knives when I need a screwdriver. Is there anything
> that just does task tracking without the bloat?"

**Signal strength**: MEDIUM-HIGH — dissatisfaction with existing options = opportunity
for a focused competitor.

### 7. Scaling Pain

Someone hit limits of their current solution as they grew.

**Keyword patterns**: "outgrew", "doesn't scale", "worked fine until", "now that we
have more", "hit the limits", "breaking at scale"

**Example (Reddit r/smallbusiness)**:
> "Google Sheets worked fine for inventory when we had 50 SKUs. Now we have 500
> and it's a nightmare. Everything is slow and formulas break constantly."

**Signal strength**: MEDIUM — indicates a market segment (growing businesses) that
existing tools under-serve.

### 8. Migration / Escape

Someone trying to leave a platform, blocked by lock-in or lack of alternatives.

**Keyword patterns**: "migrate from", "escape", "leave", "export my data",
"locked in", "held hostage", "can't switch because"

**Example (HN)**:
> "I want to leave Heroku but every alternative either costs 3x more or requires
> a DevOps hire. There's a massive gap for 'Heroku but cheaper and not dead.'"

**Signal strength**: MEDIUM-HIGH — lock-in frustration often comes with willingness
to pay for escape routes.

---

## Noise Signals

Filter these OUT — they look like demand but aren't actionable.

### Vague Complaints

> "Everything sucks these days" / "Software quality is declining"

No specific problem, no specific need. Skip.

### Already Solved (Check Replies)

If the top replies provide 3+ solid solutions with upvotes, the need is likely met.
Lower the opportunity score significantly.

### One Person's Edge Case

> "I need a tool that converts Esperanto PDFs to Braille-compatible HTML"

Real need, market of one. Not an opportunity unless you see it recurring.

### Hype / Trend Chasing

> "Someone should build an AI agent that does everything with blockchain"

Buzzword soup without specific pain. Usually noise.

### Self-Promotion Disguised as Demand

> "Has anyone tried [specific product with affiliate link]?"

Not a demand signal — it's marketing.

---

## Signal Strength Indicators

Beyond the signal type, these factors amplify or dampen strength:

| Factor | Amplifies | Dampens |
|--------|-----------|---------|
| **Engagement** | 50+ upvotes, 20+ comments | 0-2 upvotes, no discussion |
| **Specificity** | Named tools, dollar amounts, metrics | Vague desires |
| **Recurrence** | Same signal across 3+ posts/weeks | One-off mention |
| **Recency** | Posted within last 30 days | 6+ months old |
| **Author profile** | Active community member, domain expert | New/throwaway account |
| **Reply quality** | "I have this problem too" replies | "Just use X" with solutions |
| **Community fit** | Posted in relevant, active subreddit | Cross-posted spam |

## Quick Scoring Guide

- **9-10**: "Shut up and take my money" + high engagement + recurring + no solution in replies
- **7-8**: Clear demand expression + decent engagement + partial or no solutions available
- **5-6**: Indirect signal (workaround, comparison) + some engagement + solutions exist but are imperfect
- **3-4**: Vague demand + low engagement OR demand is clear but well-served by existing tools
- **1-2**: Noise, one-person edge case, or fully solved problem
