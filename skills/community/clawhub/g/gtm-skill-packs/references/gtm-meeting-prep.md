---
name: gtm-meeting-prep
description: >
  Prepare a seller or growth rep for an upcoming sales or partnership meeting.
  Produces a pre-meeting brief with account context, attendee research, discovery
  questions, and a recommended conversation arc. Use when a user has a call, demo,
  or intro meeting scheduled. Triggers: "prep me for my call with X," "I have a
  meeting with [company] tomorrow," "what should I ask [title] at [company],"
  or when a calendar invite or attendee list is provided.
license: MIT
compatibility: Requires web search access for attendee and account research.
metadata:
  author: iCustomer
  version: "1.0.0"
  website: https://icustomer.ai
---

# GTM Meeting Prep

Produce a pre-meeting brief. Tailor everything to the specific company, attendees,
and meeting type — no generic output.

## Steps

1. **Identify meeting type** — Cold Intro, Demo, POC Kick-off, Proposal, Partnership,
   or QBR. Each has a different focus and tone.
2. **Account context** — pull key facts: business model, size, stack, recent news.
   Reuse an existing account brief if one was run via `gtm-account-research`.
3. **Attendee research** — for each attendee: title, seniority, LinkedIn activity,
   tenure, likely priorities based on role. Flag any warm path (mutual connection,
   partner network, prior engagement).
4. **Discovery questions** — generate 5 prioritized questions. Default stack:
   open → current state → pain → success criteria → decision process.
   Tailor to title (technical evaluator ≠ economic buyer ≠ end user).
5. **Landmines** — flag topics to avoid: internal builds they're proud of, recent
   org changes, competitors to not name-drop without reason.
6. **Narrative arc** — recommend a 4-act flow: Open (5min) → Discover (15–20min)
   → Show (10–15min) → Close (5min). Define the meeting "win" — rarely "close the
   deal" for a first call.

## Output

```
# Meeting Brief: [Company] — [Meeting Type] | [Date]

Account: [3-sentence snapshot]
Segment: [ICP segment] | Product angle: [what you're positioning]
Stack: [Relevant tools]
Signals: [1–2 buying signals with dates]

Attendees:
[Name · Title · Key priority · Warm path if any]

Landmines: [What to avoid]

Narrative Arc:
Open → [agenda, rapport] → Discover → [top 3 areas] → Show → [what to demo] → Close → [ask]

Top 5 Discovery Questions:
1.
2.
3.
4.
5.

Meeting Win: [What "success" looks like for this specific call]
Proposed Next Step: [Specific ask to close the meeting]
```
