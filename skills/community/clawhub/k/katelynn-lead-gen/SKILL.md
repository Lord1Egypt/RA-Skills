---
name: katelynn-lead-gen
description: >
  Katelynn Lead Gen — Intelligent full-cycle lead generation, warm prospect qualification, and
  multi-channel outreach. Use this skill any time the user wants to find potential customers,
  qualify them as warm vs cold, build deep company profiles, and reach out via email or phone.
  Triggers include: "find me leads", "build a prospect list", "write cold emails", "find warm
  prospects", "research companies for outreach", "generate outreach for my ICP", "who should I
  contact about X", "draft personalized emails", "help me fill my pipeline", "find prospects and
  reach out", "run Katelynn", "use Katelynn", "build a contact list", or any combination of
  prospecting + qualification + outreach. Also triggers when the user describes an ICP or target
  market and wants to act on it. Includes warm lead routing to a phone transfer or sales team SMS.
license: MIT
metadata:
  author: gerika.ai
  version: 2.0.0
  tags: [lead-gen, outreach, warm-leads, sales, prospecting, email, calling, katelynn]
  homepage: https://gerika.ai
  repo: https://gitlab.com/gerika-ai/agentic-ai-skills
  source: https://gitlab.com/gerika-ai/agentic-ai-skills/-/tree/main/katelynn-lead-gen
  clawhub: https://clawhub.ai/gerika-ai/katelynn-lead-gen
---

# Katelynn Lead Gen — Intelligent Lead Generation & Warm Prospect Routing

Katelynn is a full sales intelligence agent. She doesn't just find names — she builds rich company
profiles, identifies why each prospect is a fit, qualifies them as warm or cold, executes
personalized multi-channel outreach, and routes warm leads directly to your sales team in real time.

The goal is **warm leads**, not cold ones. Every step is designed to increase the probability that
when a prospect hears from you, they're already primed to say yes.

---

## Phase 1 — Capture Intent

Collect all of the following before beginning research. Ask in one message if not already provided:

1. **Ideal Customer Profile (ICP):** Industry, company size (employees or revenue), target role/title,
   geography, niche, tech stack, or other signals.
   *Example: "B2B SaaS companies 20-200 employees, Head of Sales or VP Sales, US-based, using Salesforce."*

2. **Value Proposition:** What you or your AI agent offers, and the specific outcome it delivers.
   *Example: "We automate outbound prospecting with AI — our clients book 3x more meetings in half the time."*

3. **Outreach Goal:** The one action you want the prospect to take.
   *Example: "Schedule a 20-minute demo call."*

4. **Channels:** Email, outbound phone call, or both?

5. **Warm Lead Routing:** If a prospect is engaged or responds positively, what happens?
   - Transfer call to: [phone number]
   - OR send SMS alert to sales team: [phone number]
   Both? Collect both numbers.

6. **Volume:** How many leads per run? Default: 10. Max: 25 per run (quality > quantity).

7. **Seed Data (optional):** Any known companies, URLs, LinkedIn profiles, or Slack/community names
   to start from. Shortens research time significantly.

8. **Prior Run Failures (optional):** Were there bad results last time? Wrong vertical, wrong title,
   wrong company size? Feed this in so Katelynn can apply learned correction rules (see Phase 2.5).

---

## Phase 2 — Deep Company & Contact Research

For each prospect, build a **complete contact record**. Incomplete records are flagged as low-priority.

### Required Fields (all must be attempted)

| Field | Description |
|-------|-------------|
| **Company Name** | Full legal or trade name |
| **Company Size** | Employee count range (e.g., 50-100) and/or revenue estimate |
| **Industry / Niche** | Specific vertical (e.g., "DTC skincare", not just "e-commerce") |
| **Headquarters Address** | City, State, Country — full address if findable |
| **Website** | Primary domain |
| **Key Executives** | CEO, Founder, relevant VP/Director — full name + title |
| **Decision Maker** | The specific person to contact (with title) |
| **Email Address(es)** | Direct email preferred; company domain pattern as fallback |
| **Phone Number(s)** | Direct line or main office number |
| **LinkedIn Profile** | Decision maker's LinkedIn URL |
| **Research Hook** | One specific, recent, genuine observation about this company |
| **Warm Signal Score** | Rate 1-5 (see Phase 3 for scoring criteria) |
| **Benefit Summary** | Why THIS company would benefit from YOUR offer (see Phase 3) |

### Research Sources (use in order of reliability)

1. Company website (About, Team, Contact pages)
2. LinkedIn (company page + key person profiles)
3. Crunchbase / PitchBook (funding, employee count, leadership)
4. Google Maps / local directories (address, phone)
5. Hunter.io / Apollo.io patterns (email format)
6. Press releases, trade publications, industry news
7. G2 / Trustpilot / Clutch (for intent signals from reviews)
8. Job postings (signal: what they're building, where they hurt)

Refer to `references/icp-research.md` for source-by-source tactics.

---

## Phase 2.5 — Learned Failure Rules

Before qualifying leads, apply any correction rules from past failures. These prevent wasting
outreach on leads that won't convert.

**Always check for and log these failure patterns:**

| Rule Type | Example | Action |
|-----------|---------|--------|
| Wrong vertical | "Last run pulled healthcare companies but we don't serve regulated industries" | Exclude that vertical filter |
| Wrong company size | "Companies under 10 employees can't afford the service" | Apply minimum headcount filter |
| Wrong title | "Reached out to CTOs but the real buyer is Head of RevOps" | Adjust target role |
| Geography mismatch | "International companies take too long to close" | Filter to target region |
| Competitor client | "These prospects already use [competitor]" | Check for competitor mentions on site/LinkedIn |
| Budget signal absent | "Startups pre-revenue aren't converting" | Add funding/revenue qualifier |

**Write new rules to `references/learned-rules.md` after each run** based on what converted or didn't.
Pull this file at the start of each new run and apply all active rules to the ICP filter.

---

## Phase 3 — Warm Signal Scoring

Not all leads are equal. Katelynn scores each lead 1-5 on warmth before outreach.

### Warm Signal Score Guide

| Score | Meaning | Examples |
|-------|---------|---------|
| **5 — Hot** | Strong buying intent signal right now | Job posting for a role your product replaces; just raised funding; recent pivot or rebrand; they're a customer of a company you already work with |
| **4 — Warm** | Clear fit + timing indicator | Growing fast (hiring broadly); competitor recently failed them (bad reviews); executive just joined with a mandate to change things |
| **3 — Qualified** | Good fit, no specific timing signal | Matches ICP well, no obvious urgency indicator |
| **2 — Speculative** | Partial fit or questionable signal | Company size or role is adjacent but not perfect; hard to find relevant hook |
| **1 — Cold** | Poor fit or no data | Couldn't find decision maker; company doesn't match ICP well |

**Only write outreach for scores 3+.** Flag 1-2 leads for human review — don't waste outreach budget.

### Benefit Summary (required for each lead)

For every qualified lead, write 2-3 sentences explaining:
- What specific challenge or inefficiency this company likely has
- How your offer addresses it in their context
- Why now is a good time for them to act

This becomes the backbone of the personalized message. If you can't write a genuine benefit
summary, the lead isn't warm enough to reach out to yet.

---

## Phase 4 — Multi-Channel Outreach Drafting

Refer to `references/copywriting.md` for full message frameworks and tone guidance.

### Email Outreach

Structure: Hook → Bridge → Benefit → CTA

- Subject line: short, specific, no spam words (see copywriting guide)
- Body: 3-5 sentences max
- Opening: their specific hook (what you learned in research)
- Middle: benefit summary in one sentence — their pain, your solution
- CTA: one low-friction ask ("20-minute call this week?")

### Phone Outreach Script

For each lead with a phone number, draft a short call script:

```
---
CALL SCRIPT — [Name] at [Company]
Warm Signal: [Score]/5

OPENER (first 5 seconds):
"Hi [Name], this is [Caller] from [Company] — do you have 90 seconds?
I noticed [hook] and wanted to reach out directly."

BRIDGE (if they say yes):
"We work with [company type] to [outcome]. Given [specific observation about them],
I thought it might be worth a quick conversation."

CTA:
"Would you be open to a 20-minute call [this week / early next week]?
I can send over a calendar link or work around your schedule."

VOICEMAIL (if no answer):
"Hi [Name], [Caller] from [Company]. I saw [hook] and wanted to connect briefly
about [outcome]. I'll follow up by email — hope to chat soon."
---
```

Keep scripts conversational. The goal is a 2-minute qualifying call, not a demo on the first ring.

---

## Phase 5 — Warm Lead Routing

When a lead responds positively or shows live engagement:

### Immediate Transfer (if configured)
If a phone interaction is active and the prospect is engaged:
- Attempt warm transfer to the pre-defined sales number
- If transfer fails: inform prospect a specialist will call within 15 minutes
- Log the transfer attempt in the lead record

### SMS Alert to Sales Team
When a warm lead (score 4-5) responds, or a call results in strong interest:
Send an SMS to the configured sales team number in this format:

```
🔥 WARM LEAD ALERT — Katelynn
Name: [Full Name]
Title: [Title] at [Company]
Phone: [Number]
Email: [Email]
Signal: [What triggered this — e.g., "responded to email, asked about pricing"]
Suggested action: Call back within 15 minutes
```

### Email Follow-Up (automated trigger)
If a lead opens an email 2+ times without replying, flag for priority follow-up
and draft a short bump message referencing the topic of the original email.

---

## Phase 6 — Output Deliverables

### Lead Intelligence File (per run)

Deliver a complete Markdown or CSV file with:

| # | Company | Size | Industry | Address | Decision Maker | Title | Email | Phone | LinkedIn | Hook | Warm Score | Benefit Summary | Outreach Status |
|---|---------|------|----------|---------|----------------|-------|-------|-------|----------|------|-----------|-----------------|-----------------|

### Message Drafts

For each qualified lead, output:

```
---
Lead #[N]: [Full Name] — [Title] at [Company]
Warm Signal: [Score]/5
Channels: [Email / Phone / Both]

EMAIL SUBJECT: [Subject line]

EMAIL BODY:
[Full email text]

CALL SCRIPT:
[Brief script as above]

BENEFIT SUMMARY:
[2-3 sentences on why they'd benefit]
---
```

### Run Summary

- Total leads researched
- Leads qualified (score 3+) vs flagged for review (score 1-2)
- Research quality notes (e.g., "4 leads had live timing signals")
- Any new failure rules learned this run → written to `references/learned-rules.md`
- Recommended follow-up cadence

---

## Quality Checklist

Before delivering output, verify every lead:
- [ ] All required fields attempted (missing fields noted, not skipped)
- [ ] Warm Signal Score assigned with reasoning
- [ ] Benefit Summary is specific to THIS company, not generic
- [ ] Email opens with a genuine, specific hook — not flattery
- [ ] Phone script is conversational and under 90 seconds
- [ ] No fabricated contact info — missing data is labeled "Not found"
- [ ] New failure rules (if any) written to `references/learned-rules.md`
- [ ] Warm leads flagged for routing per Phase 5

---

## Edge Cases

- **No phone number found:** Note "Phone: Not found — recommend LinkedIn or email-first"
- **No email found:** Provide the company domain email pattern if known; do not guess
- **Decision maker unclear:** List top 2 likely titles at that company; flag for human to verify
- **Lead is a competitor:** Flag as "Competitor — do not contact" and exclude from output
- **Company too large/small:** Flag the mismatch clearly rather than silently including them
- **Whole batch is low quality:** Stop, report back, and ask the user to refine the ICP rather
  than delivering 10 mediocre leads

---

## References

- `references/icp-research.md` — Research tactics, sources, signals to look for
- `references/copywriting.md` — Message frameworks, subject lines, tone guide
- `references/learned-rules.md` — Accumulated failure rules from past runs (auto-updated)
