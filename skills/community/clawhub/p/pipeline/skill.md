---
name: Pipeline
description: >
  Diagnose pipeline health, detect stalled deals, and surface what needs
  attention this week. Built for sales teams managing active opportunities.
version: 2.0.0
---

# Pipeline

> **A pipeline's job is not to make you feel good about your forecast. Its job is to tell you the truth.**

Pipeline is a truth-enforcing control skill for active sales opportunities.

Use this skill when you need to:
- identify which deals are truly advancing vs sitting idle
- detect stalled or fake-active opportunities
- enforce stage discipline
- surface the few deals that need attention this week
- improve forecast accuracy by cleaning pipeline pollution
- turn a messy deal list into a pipeline you can actually trust

This skill does NOT:
- find new targets (use `@dpetcr/prospect`)
- qualify a single engaged contact from scratch (use `@AGIstack/lead`)
- write or structure formal proposals (use `@dpetcr/proposal`)
- redesign your full sales process from zero

---

## Pipeline vs Lead

These skills handle different layers of the sales process.

| | Pipeline | Lead |
|---|---|---|
| **Scope** | Many active opportunities | One engaged opportunity |
| **Question** | "What is the health of my whole deal flow?" | "Should I keep pursuing this person?" |
| **Input** | Deal list, stages, dates, next steps, values | One prospect, reply history, buying signals |
| **Output** | Health diagnosis, priorities, pipeline actions | Qualification score, next action |
| **Focus** | System truth and control | Single-opportunity judgment |

**Typical flow:**
1. `@dpetcr/prospect` filters who is worth pursuing  
2. outreach happens  
3. `@AGIstack/lead` judges engaged opportunities  
4. **Pipeline** manages the whole active book  
5. `@dpetcr/proposal` supports formal closing progression

Use **Lead** for one opportunity.  
Use **Pipeline** for the full active system.

---

## What This Skill Does

Pipeline helps:
- identify stalled deals
- detect stage pollution
- find unsupported forecast optimism
- surface which deals need action now
- spot weak next-step discipline
- reveal where the pipeline is unhealthy
- recommend clean-up actions that improve control

Pipeline is not a design lecture.  
It is an operating view for active opportunities.

---

## What to Provide

Useful input includes:
- deal or account name
- current stage
- owner
- last activity date
- next scheduled step
- expected close timing
- deal size or value
- blockers or risks
- notes from recent conversations

The more concrete the pipeline data, the more reliable the diagnosis.

---

## Standard Output Format

PIPELINE HEALTH  
━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: [Healthy / Warning / Critical / Broken]

BREAKDOWN  
━━━━━━━━━━━━━━━━━━━━━━━━━━
Hygiene: [Strong / Weak] — [one-line reason]  
Stagnation: [Low / Medium / High] — [one-line reason]  
Balance: [Healthy / Uneven] — [one-line reason]  
Forecast Credibility: [High / Medium / Low] — [one-line reason]

TOP 5 TO ACT ON NOW  
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [Deal] — [why it matters now]
2. [Deal] — [why it matters now]
3. [Deal] — [why it matters now]
4. [Deal] — [why it matters now]
5. [Deal] — [why it matters now]

STALLED / FALSE-ACTIVE DEALS  
━━━━━━━━━━━━━━━━━━━━━━━━━━
- [Deal] — [days inactive] — [why it no longer looks truly active]
- [Deal] — [days inactive] — [why it no longer looks truly active]

STAGE RISKS  
━━━━━━━━━━━━━━━━━━━━━━━━━━
- [Stage] is accumulating stalled deals
- [Deal] appears over-advanced for the evidence available
- [Deal] has no credible next step
- [Forecast] is inflated by weak late-stage deals

IMMEDIATE ACTIONS  
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [Action]
2. [Action]
3. [Action]

WORKS WELL WITH  
━━━━━━━━━━━━━━━━━━━━━━━━━━
- `@dpetcr/prospect` for pre-contact filtering
- `@AGIstack/lead` for single-opportunity judgment
- `@dpetcr/proposal` for formal deal progression

If user provides a small pipeline, include deal-by-deal detail.  
If user provides a large pipeline, summarize first, then expand only the top-risk and top-opportunity deals.

---

## Core Truth Principles

- A deal without a real next step is weaker than it appears.
- A stage name means nothing without stage evidence.
- A stale deal is not active just because it still exists in CRM.
- Forecast quality comes from honesty, not optimism.
- Pipeline control is about truth, not comfort.

---

## Heuristic Health Assessment

When user asks about overall pipeline health, assess these dimensions:

### Hygiene
Look for:
- deals with no recent activity
- vague or missing next steps
- close dates that look arbitrary
- old deals still sitting in active stages

### Stagnation
Look for:
- stages where deals enter but rarely exit
- deals aging without visible movement
- repeated follow-up with no real progression
- “still alive” deals that show no buying behavior

### Balance
Look for:
- too much weight in early stages
- too many late-stage deals with weak evidence
- weak pipeline replenishment
- an unhealthy mix of deal age and stage position

### Forecast Credibility
Look for:
- close dates unsupported by current behavior
- advanced-stage deals lacking stakeholder movement
- proposal/late-stage deals with no scheduled next step
- pipeline value that depends on fake-active deals

Use these dimensions as judgment aids, not fake precision.

---

## Review Routes

Use these default routes:

**Advance**
- deal has momentum
- stage evidence is real
- next step is clear

**Recover**
- deal may still be viable
- momentum has weakened
- action is needed quickly

**Watch**
- deal is not dead, but not worth heavy effort this week

**Downgrade**
- stage is too optimistic for the evidence
- move deal back to a more honest stage

**Close Out**
- no credible momentum remains
- remove from active forecast and stop pretending

---

## When to Use Pipeline

Use this skill when:
- you want to review the health of an active deal book
- you need to find stalled or fake-active deals
- you want to know what deserves attention this week
- you need a more honest forecast view
- you need to clean up stage discipline

Do not use this skill when:
- you are still selecting targets before contact (`@dpetcr/prospect`)
- you are judging one engaged opportunity (`@AGIstack/lead`)
- you need proposal help (`@dpetcr/proposal`)
- you need broad sales-process consulting rather than pipeline control

---

## Execution Protocol (for AI agents)

When user provides pipeline data, follow this sequence:

### Step 1: Parse Pipeline
Extract:
- deal names
- stages
- owners
- last activity
- next steps
- values
- expected close timing
- blockers

### Step 2: Detect False Activity
Identify deals that look active in name only:
- no recent activity
- no real next step
- late stage without supporting evidence
- close date based on hope rather than movement

### Step 3: Assess Health
Review:
- Hygiene
- Stagnation
- Balance
- Forecast Credibility

### Step 4: Surface Top 5
Pick the 5 deals that most deserve attention now:
- biggest upside with real recoverability
- biggest forecast risk
- biggest stage-discipline issue
- biggest next-step urgency

### Step 5: Assign Route
For each key deal, recommend:
- Advance
- Recover
- Watch
- Downgrade
- Close Out

### Step 6: Produce Actions
Return:
- overall pipeline status
- main risks
- top 5 priorities
- concrete actions for this week

### Step 7: Handoff When Needed
If a deal needs one-opportunity judgment, suggest `@AGIstack/lead`.  
If a deal is ready for formal closing progression, suggest `@dpetcr/proposal`.  
If user is still filtering targets before contact, suggest `@dpetcr/prospect`.

---

## Activation Rules (for AI agents)

### Use this skill when the user asks about:
- pipeline health
- stalled deals
- forecast reliability
- stage discipline
- deal-book review
- what needs attention across many active opportunities

### Do NOT use this skill when:
- the task is pre-contact filtering
- the task is single-lead qualification
- the task is proposal writing
- the task is a non-sales workflow unless explicitly reframed into active opportunity control

### Ambiguous cases
If pipeline is mentioned but the user may mean a general workflow, ask:
"Are you asking about a sales opportunity pipeline, or a different kind of process?"

Proceed as Pipeline only if the context is active opportunities and stage control.

---

## Quality Check Before Delivering

- [ ] Health status is clear
- [ ] False-active deals are identified
- [ ] Top 5 priorities are justified
- [ ] Stage risks are explicit
- [ ] Forecast credibility is addressed
- [ ] Actions are concrete
- [ ] Handoffs to related skills are used when helpful

---

## Boundaries

This skill supports active opportunity control for sales pipelines.

It does not replace:
- legal or compliance review
- finance approval logic
- CRM administration
- hiring, onboarding, or delivery workflow design
- ethical judgment about forecast reporting

Adapt outputs to your actual sales motion, stage definitions, and operating rules.
