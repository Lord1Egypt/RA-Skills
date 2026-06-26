---
name: lead-nurture
description: Adaptive email and SMS nurture sequences that adjust based on engagement signals. Input your lead scenario — get a sequence with A/B subject lines, re-send logic, timing rules, and engagement scoring. Not a template generator — a behavioral system.
version: 2.0.0
author: drivenautoplex1
---

# Lead Nurture Sequence Generator — Adaptive v2

Turn cold or stalled leads into warm pipeline with sequences that adapt to behavior, not just time.

## What Makes v2 Different From Template Generators

Most nurture tools send the same emails on the same schedule regardless of what the lead does. That's why most sequences underperform.

v2 introduces **behavioral branching** — each touch has three variants depending on the lead's prior engagement:

- **Branch A (Engaged):** Lead opened and/or replied → deepen the conversation
- **Branch B (Passive):** Lead opened but didn't reply → reframe and re-approach
- **Branch C (Dark):** Lead didn't open → re-send with different subject + format change

The system also outputs an **engagement score** (0–100) that updates after each touch based on behavior, letting your CRM or agent know when to escalate to human outreach.

---

## Inputs

```json
{
  "industry": "mortgage|real_estate|coaching|saas|services|custom",
  "lead_type": "credit_repair|browsing|not_ready|abandoned_cart|cold|warm|referral",
  "sequence_length": 5,
  "timeline_days": 75,
  "goal": "book_call|close_sale|reactivate|warm_referral",
  "brand_voice": "professional|casual|authoritative|empathetic",
  "include_sms": true,
  "behavioral_branching": true,
  "ab_subjects": true,
  "engagement_scoring": true,
  "crm_export_format": "json|csv|gohighlevel|followupboss|mailchimp"
}
```

---

## Outputs

```json
{
  "sequence": [
    {
      "day": 0,
      "touch_number": 1,
      "type": "email",
      "subject_a": "Your credit timeline (honest answer)",
      "subject_b": "Something most people in your situation get wrong",
      "preview": "Most people think fixing credit takes years. It doesn't.",
      "body_engaged": "...",
      "body_passive": "...",
      "body_dark": "...",
      "cta": "Reply with your biggest concern",
      "sms": "Hey [Name] — sent you an email. Worth 2 min when you get a chance.",
      "send_rule": "Send immediately on trigger",
      "resend_rule": "If no open after 72h, send subject_b with body_dark variant",
      "pause_rule": "If reply received, pause sequence and flag for human follow-up"
    }
  ],
  "engagement_scoring": {
    "open_weight": 10,
    "reply_weight": 40,
    "click_weight": 20,
    "resend_trigger_threshold": 0,
    "human_escalation_threshold": 60,
    "archive_threshold": -20
  },
  "sequence_summary": "5-touch adaptive sequence over 75 days — credit repair leads",
  "psychology_map": {
    "touch_1": "Pacing + reality check — meet them where they are",
    "touch_2": "Quick win — build trust with immediate value",
    "touch_3": "Myth bust — reframe limiting beliefs, position as expert",
    "touch_4": "Market urgency — seeds the buying decision without pressure",
    "touch_5": "Soft close — assume the next step, remove friction"
  },
  "ab_test_guidance": "Run subject_a for 48h. If open rate <20%, switch to subject_b for remainder of send. Track by contact tag in your CRM.",
  "crm_export": "...formatted for selected CRM..."
}
```

---

## Behavioral Branching Logic

### How it works in practice (mortgage/credit repair example):

**Touch 1 sent → 72 hours pass:**

| What happened | Next action |
|---------------|-------------|
| Replied | Pause automation. Human follow-up within 4 hours. |
| Opened, no reply | Send Touch 2 (Branch B — reframe) |
| Didn't open | Re-send Touch 1 with subject_b variant, body_dark format |

**Engagement score threshold rules:**

| Score | Meaning | Trigger |
|-------|---------|---------|
| 60+ | Hot lead | Flag for immediate human outreach |
| 20–59 | Warm, nurturing | Continue sequence |
| 0–19 | Cool, passive | Switch to longer-interval, lighter touches |
| Below 0 | Unresponsive | Move to archive sequence (1 touch/month) |

---

## Tiers

**Free** — 3-email sequence, email only, no branching, no engagement scoring
**Standard ($12/mo)** — Up to 7 touches, all industries, email + SMS, A/B subjects, send/re-send rules
**Pro ($37/mo)** — Full behavioral branching, engagement scoring, CRM export (GHL/FUB/Mailchimp/CSV), psychology map, unlimited sequences, priority generation

---

## Pre-Tuned Lead Types (All Include Behavioral Branching in Standard+)

| Lead Type | Touches | Timeline | Core Psychology |
|-----------|---------|----------|-----------------|
| Credit repair (mortgage) | 5 | 75 days | Pacing → quick win → reframe → urgency → soft close |
| Abandoned cart (e-comm) | 4 | 7 days | Loss aversion → social proof → scarcity → final offer |
| Cold B2B outreach | 6 | 21 days | Value-first → problem framing → case study → objection → ask → breakup |
| Post-consultation (services) | 4 | 14 days | Recap → FAQ → comparison → decision frame |
| Gone-quiet reactivation | 3 | 30 days | Check-in → news hook → final reach |
| Referral re-engagement | 3 | 21 days | Gratitude → milestone update → soft ask |

---

## Example — Touch 2, Branch Variants (Mortgage / Credit Repair)

**Branch A (Engaged — replied to Touch 1):**
> Subject: Based on what you told me — here's where I'd start
>
> Since you mentioned [their concern], the fastest move is actually not what most people think.
> [Tailored advice based on their reply]
> Want me to run the exact math on what your score moving 40 points would do to your monthly payment?

**Branch B (Passive — opened, no reply):**
> Subject: The fastest thing you can do to move your score this month
>
> One thing, quick. The single fastest credit score move — faster than disputing anything — is reducing your utilization below 30% on every card.
> [Utilization explanation]
> Reply if you want help looking at your report together.

**Branch C (Dark — didn't open):**
> Subject: Quick question [First Name]
>
> Tried to reach you last week. No worries if the timing was off.
> One quick thing: do you know your current credit score? That's the only number that tells us what your options actually are right now.
> [Short. No links. Conversation-opener format.]

---

## Integration Notes

**GoHighLevel:** Use the JSON export → import as a Workflow. Each branch maps to a conditional trigger in GHL's workflow builder.

**Follow Up Boss:** Export as CSV → import as a Smart List action plan. Branch logic requires manual setup but the copy imports directly.

**Mailchimp:** Use Standard export → paste into an automation sequence. Branching requires Mailchimp's conditional content blocks (Standard plan+).

**Manual (any platform):** Create 3 versions of each email (A/B/C). Tag contacts by engagement level after each send. Send the appropriate version to each segment.

---

*v2.0.0 — Upgraded from template generator (depth 2) to behavioral system (depth 4). Added: behavioral branching, A/B subjects, re-send logic, engagement scoring, CRM export formats, psychology map.*
