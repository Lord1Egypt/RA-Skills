---
name: gtm-account-research
description: >
  Deep-dive a target company and produce a structured account intelligence brief
  covering tech stack, buying signals, key personas, and a recommended engagement
  angle. Use before outreach, a first call, a demo, or setting up an ABM campaign.
  Triggered by: "research this account," "brief me on [company]," "what do I know
  about [company]," or when preparing for a meeting with a named account.
license: MIT
compatibility: Requires web search access for live signal research.
metadata:
  author: iCustomer
  version: "1.0.0"
  website: https://icustomer.ai
---

# GTM Account Research

Produce an Account Intelligence Brief for a named company. Ground every signal
in a specific, traceable source.

## Steps

1. **Snapshot** — company name, HQ, size, business model, recent news (last 90 days)
2. **Tech stack** — identify tools in the categories most relevant to your product
   (e.g. data warehouse, CRM, marketing automation, paid channels). Use BuiltWith,
   job postings, and engineering blogs as sources.
3. **Buying signals** — job postings, conference attendance, funding events, published
   strategy content. Date every signal.
4. **Displacement triggers** — are they actively migrating off a competitor? Hiring
   for a role that signals a gap you fill? Flag ⚡ if a strong trigger is present.
5. **Personas** — identify Economic Buyer (budget authority), Technical Champion
   (evaluates), and End User (daily use). Name + LinkedIn URL when findable.
6. **Engagement angle** — one specific recommendation: what pain, which product,
   what channel, who reaches out first, and the opening hook.

## Output

```
# Account Brief: [Company] | [Date]

Snapshot: [3 sentences — what they do, size, recent context]
ICP Segment: [your segment label]
Stack: [Category: tool — or "Unknown" for each category]
Signals: [Bulleted — signal + source + date]
Displacement: [⚡ Yes — detail / None detected]
Personas: [Name · Title · LinkedIn · Pain point — one row per person]
Gaps: [What's missing that would sharpen the approach]

Engagement Angle:
[Specific: pain → product → channel → who reaches out → opening hook]
```

Keep the brief scannable. Flag any detail as `[Unverified]` if not directly observed.
