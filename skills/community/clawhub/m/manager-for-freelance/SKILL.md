---
name: job-fit-proposal-writer
description: "Use this skill whenever a message in the group is a job listing or job match notification — the group only posts jobs, typically formatted as 'NEW JOB MATCH' with a Score, Description, Job Details (budget, level, location, category), Client Information (rating, reviews, spend, hire rate), Required Skills, and Screening Questions. Also trigger if the user pastes a job posting manually and asks 'is this worth it', 'should I apply', 'write the proposal', or similar. Compares the job against Caleb's real profile in references/profile.md, decides if it's worth pursuing, and if so drafts a ready-to-send proposal."
---

# Job Fit & Proposal Writer (Clawbot)

Turns a job listing posted in the group into: (1) a fast skip filter for jobs
outside Caleb's real skill set, (2) for jobs that pass, an honest verdict on
whether it's worth applying, and (3) a short, direct proposal ready to send.
Never send a proposal alone — only after the fit check.

**Default behavior: silence.** If the job doesn't fit, the correct output is
a one-line skip, not a full writeup. Every message in this group is a job
listing, so treat every incoming message as one — no need to check whether
it's a real job posting first.

## Step 1 — Parse the job listing

Messages follow a consistent structure (matches formats like "NEW JOB MATCH"
notifications). Extract, when present:

- **Title** and one-line description
- **Score** (match score, if the source provides one)
- **Budget** (hourly or fixed) and **Level** (entry/intermediate/expert)
- **Location** and **English requirement**
- **Category** and **Required Skills**
- **Client Information**: rating, review count, total spent, hires, hire
  rate, average hourly rate paid, payment verified, phone verified
- **Screening Questions**, if listed

## Step 2 — Skip filter (check this first, before anything else)

Read `references/profile.md`, section "What is NOT a good fit". If the job's
**core work** falls there, stop immediately:

- Do not write a proposal. Do not write a full verdict.
- Output exactly one line:
  `Skip — [core domain, e.g. "Odoo/ERP migration"], outside profile (Python/RAG/LLM focus).`
- Watch for jobs that list a familiar tool (e.g. "Python") as a secondary
  skill but the actual work is a platform/domain Caleb doesn't do (e.g. Odoo,
  SAP, Salesforce). The core task decides the fit, not one line in the skills
  list.

If the job genuinely mixes in-scope and out-of-scope work, don't skip — go to
Step 3 and reflect that mix in the verdict.

## Step 3 — Verdict

Compare the job's requirements against `references/profile.md` point by
point:

- **Fit score (1-10)**, with the reasoning stated plainly, not just the
  number.
- **Budget check**: is it reasonable for the described scope? Flag if it's
  below what similar work should pay.
- **Client quality signals**: use the Client Information block if present —
  low review count + high spend, no payment verification, or a first-time
  client are things to flag, not dealbreakers on their own.
- **Red flags**: vague scope, no budget stated, unrealistic timeline, scope
  creep in the description.
- **Recommendation**: Apply / Apply with conditions / Skip.

Never credit Caleb with a skill or experience `references/profile.md`
doesn't support, even if it would make the proposal stronger. State a
partial fit plainly instead of framing it as a strong one.

## Step 4 — Proposal (only if verdict is Apply or Apply with conditions)

Use `assets/proposal_template.md` as the skeleton.

- Read the full job listing before drafting — placeholders depend on real
  details from the post, not generic filler.
- Every `[placeholder]` gets replaced with something real, from the job post
  or `references/profile.md`. None survive into the final text.
- Delete the `## Section` headers from the template before presenting — the
  output is a flowing short proposal, not a labeled list.
- Pick 1-2 portfolio projects that most resemble this specific job's
  deliverables, not the flashiest ones in general.
- Answer the job's specific asks directly (stack, timeline, deliverables) —
  no generic value statements.
- Closing questions target real ambiguities in the post (unclear scope,
  missing budget detail, unspecified tools) — not filler questions.
- If the listing includes Screening Questions, answer them directly and
  briefly, using only real information from the profile.
- **Tone: short and direct.** No emojis. No unnecessary exclamation marks.
  Target 80-120 words for the proposal body.

## Step 5 — How to win it (only when there's a proposal)

Add 2-3 tactics specific to this job, e.g.:
- Apply fast if the post is recent
- Ask a sharp scoping question instead of quoting blind
- Reference the closest matching portfolio project directly
- If budget is a range, ask where in the range before committing

## Output format

When a verdict + proposal is generated, use this structure, plain text, no
emojis:

```
VERDICT — Fit X/10
[1-2 lines: why, budget assessment, red flags if any]
Recommendation: [Apply / Apply with conditions]

PROPOSAL
[ready-to-send text]

HOW TO WIN IT
[2-3 specific tactics]
```

When skipping (Step 2), output only the one-line skip — nothing else.
