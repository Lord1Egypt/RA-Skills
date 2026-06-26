---
name: gtm-inbound-strategy
description: >
  Design inbound GTM systems — lead routing logic, PLG activation flows, nurture
  tracks, and ICP-based triage. Use when leads aren't converting, building or
  optimizing a PLG trial funnel, or when marketing and sales disagree on lead
  quality. Triggers: "design our inbound motion," "build a lead routing model,"
  "create a nurture sequence," "our trial signups aren't activating," "triage
  these inbound leads," "optimize our PLG funnel."
license: MIT
compatibility: No code execution required.
metadata:
  author: iCustomer
  version: "1.0.0"
  website: https://icustomer.ai
---

# GTM Inbound Strategy

Design or optimize the inbound GTM system from lead capture through conversion.
Output is a routing model + activation/nurture sequences with explicit SLAs.

## Steps

1. **Classify lead sources** — assign signal strength and routing priority:
   - Demo request → 🔴 High: route to AE (SLA: 4 hours)
   - Trial/PLG signup → 🟡 Medium: PLG activation flow
   - Gated content / event → 🟡 Medium: nurture + intent watch
   - Newsletter / organic → ⚪ Low: long-play nurture

2. **ICP triage** — FIRE quick-score every inbound lead within 24 hours
   (see `gtm-qualification-scoring` for the full rubric):
   - F ≥ 7 AND I ≥ 7 → sales-qualified, route to AE now
   - F ≥ 6, I < 6 → marketing-qualified, enter nurture + intent watch
   - F < 6 → self-serve or long-play nurture — no SDR time

3. **PLG activation flow** (if applicable) — define the "aha moment" first: the
   single action that predicts retention. Build the sequence to reach it in ≤ 3 steps.
   Default cadence: Day 0 confirm → Day 1 first-value prompt → Day 3 usage check →
   Day 7 case study → Day 14 sales touch (if ICP match) → Day 21 re-engagement.

4. **Nurture tracks** — assign to one of three tracks:
   - Track A (High-Fit, Low-Intent): educate, 1x/week for 6 weeks
   - Track B (High-Intent, Unknown-Fit): qualify fast, 2x/week for 2 weeks
   - Track C (Low-Fit, Low-Intent): brand affinity, 2x/month

5. **Define SLAs** — every routing rule needs a time window and an owner.
   "Route to sales" without an SLA is not a system.

## Output

```
# Inbound GTM Motion: [Product / Segment] | [Date]

Lead Source Map: [Source · Signal strength · Routing priority]
FIRE Triage Thresholds: [Specific F/I thresholds for this ICP]

Routing Logic:
IF [source + FIRE condition] → [action] (SLA: [time], Owner: [role])
[repeat for each routing rule]

PLG Activation Flow: [Day-by-day: channel · content · goal · aha moment]
Nurture Tracks: [Track A / B / C — cadence, content type, goal]
Handoff SLAs: [Lead tier → response time → who owns it]
```
