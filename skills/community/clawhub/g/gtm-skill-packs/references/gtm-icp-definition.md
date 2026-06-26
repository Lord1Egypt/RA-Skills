---
name: gtm-icp-definition
description: >
  Run an ICP definition or refinement workshop. Use when a team needs to define
  who their best customers are, align sales and marketing on targeting, identify
  negative ICP criteria, or build a segment-and-persona framework from scratch.
  Triggers: "help me define our ICP," "who are our best customers," "refine our
  ICP," "sales and marketing disagree on who to target," "our pipeline quality
  is low."
license: MIT
compatibility: No code execution required.
metadata:
  author: iCustomer
  version: "1.0.0"
  website: https://icustomer.ai
---

# GTM ICP Definition

Facilitate a structured ICP workshop. Output is a versioned ICP document teams
can act on across sales, marketing, and growth.

## Steps

1. **Best customer analysis** — ask for 3–5 best customers. Extract: what they share
   (industry, size, stack, GTM model), what made them buy (trigger, champion, pain),
   what outcome they got, why they stay.

2. **Loss/churn analysis** — ask about lost deals and churned accounts. Identify
   recurring patterns → defines Negative ICP.

3. **Segment the market** — group into 2–5 segments by: vertical, business model,
   size band, data/tech maturity, GTM motion fit (PLG vs sales-led).

4. **Map the buying committee** — per segment: Economic Buyer (approves budget),
   Technical Champion (evaluates), End User (daily use), Blocker (can kill deal).

5. **Define FIRE criteria** — translate each segment into measurable scoring signals.
   What firmographic attributes = high Fit? What behavioral signals = high Intent?
   Use the `gtm-qualification-scoring` skill for the full FIRE rubric.

6. **Write the ICP document** — use the template below.

## Output (inline version)

```
ICP v[X] · [Company] · [Date]

Segment [#]: [Name]
Who: [1–2 sentences]
Firmographics: industry · size · geography · business model
Stack signals: [tools or tech patterns indicating fit]
Trigger events: [what makes them enter the market]
Buying committee: Economic Buyer / Champion / End User / Blocker
Why they buy: [pain + outcome]
ACV range / sales cycle: [estimate]

Negative ICP:
- [Characteristic] → [why it's a bad fit]

FIRE scoring criteria for this segment:
- Fit: [high-signal markers]
- Intent: [specific triggers]
- Recency: [timeframe threshold]
- Engagement: [interaction types that count]
```

**Flag any segment not grounded in real customers** as `[Hypothesis — validate with
first 10 customers]`. Version the document and recommend revisiting every 6 months.
