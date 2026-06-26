---
name: gtm-qualification-scoring
description: >
  Score and prioritize leads, accounts, or pipeline using the FIRE framework
  (Fit, Intent, Recency, Engagement). Use when asked to qualify a prospect,
  score a lead, rank accounts, triage pipeline, or decide who to call first.
license: MIT
compatibility: No code execution required. Works in claude.ai, Claude Code, and API.
metadata:
  author: iCustomer
  version: "1.0.0"
  website: https://icustomer.ai
---

# GTM Qualification Scoring

Score each account across FIRE (Fit · Intent · Recency · Engagement), assign a
priority tier, and recommend a next action. Every score needs traceable evidence.

## FIRE Scoring Rubric

**Formula:** FIRE Total = (F + I + R + E) / 4  [max 10.0]

**F — Fit** (ICP match: industry, size, stack, GTM model)
- 8–10: Exact ICP match — right vertical, size, tech stack, and buyer present
- 5–7: Partial match, 1–2 ICP criteria missing
- 1–4: Wrong industry, size, or insufficient data to assess

**I — Intent** (active buying behavior)
- 8–10: Active job posting for relevant role, RFP in market, or vendor comparison underway
- 5–7: Conference attendance, published strategy content, recent tech investment
- 1–4: No visible intent signals

**R — Recency** (freshness of intent signals)
- 8–10: Signal within 30 days
- 6–7: Signal 31–90 days ago
- 4–5: Signal 91–180 days ago
- 1–3: Older than 180 days or unknown

**E — Engagement** (prior contact with your brand or ecosystem)
- 8–10: Direct engagement (demo request, event attendance, reply to outreach)
- 6–7: Indirect (newsletter subscriber, mutual connection, partner network)
- 4–5: Warm ecosystem (social follower, 2nd-degree connection)
- 1–3: Cold — no prior contact

## Priority Tiers

| FIRE Total | Tier | Action |
|---|---|---|
| 8.0–10.0 | 🔴 P1 | Personalized outreach this week |
| 5.0–7.9 | 🟡 P2 | Sequence within 30 days |
| 1.0–4.9 | ⚪ P3 | Nurture only |

## Auto-Escalate to P1 (regardless of score) ⚡

Flag these signals immediately and override to P1:
- Actively migrating off or replacing a core platform you displace
- Job posting explicitly naming a problem you solve
- Funding event (Series B+) without the stack you provide
- Publicly described your category as "too expensive" or "too complex"
- Major infrastructure expansion directly relevant to your solution

## Steps

1. Identify the account(s) to score
2. Confirm the ICP segment — ask the user if not specified
3. Score each FIRE dimension 1–10 with specific evidence
4. Check auto-escalation triggers above
5. Calculate total: (F + I + R + E) / 4
6. Assign priority tier and write the recommended next action
7. Flag any intelligence gaps that would change the score

## Grounding Rules
- Every score needs traceable evidence — never assign a score without a reason
- Mark unverifiable signals as `[Unverified]`
- Score conservatively when evidence is thin

## Output

For a single account:
```
## [Company Name]
Segment: [ICP segment] | FIRE: F:[x] I:[x] R:[x] E:[x] → [x.x]/10 | Priority: [🔴/🟡/⚪] [P1/P2/P3]
Auto-Escalate: [⚡ Yes — reason / No]

Evidence: [One sentence per dimension — source + date]
Summary: [Why this account is or isn't worth pursuing right now]
Next Action: [Specific: who, channel, angle, when]
Gaps: [What info would change the score]
```

For 3+ accounts, lead with a ranked summary table, then individual entries sorted by score.
