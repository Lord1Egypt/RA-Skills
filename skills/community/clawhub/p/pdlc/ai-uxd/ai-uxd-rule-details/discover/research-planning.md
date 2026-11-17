<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 2: Research Planning & Synthesis

## Purpose

Define what we need to learn about users, plan research methods, synthesize existing data from predecessor documents, and produce a research synthesis that forms the evidence base for persona development.

---

## Depth Adaptation

| Depth | Research Scope |
|-------|---------------|
| **Minimal** | Synthesize existing data only; 2-3 focused research questions; skip primary research planning |
| **Standard** | Existing data + research plan for 4-6 questions; methods recommended |
| **Comprehensive** | Full research plan including primary methods, card sorting plan, tree testing plan, empathy mapping methodology |

---

## Steps

### Step 1: Define Research Questions

Based on the unknowns identified in Stage 1, formulate research questions:

**Categories:**
- **Who:** Who are the users? What segments exist? What differentiates them?
- **What:** What tasks do they need to accomplish? What are their goals?
- **How:** How do they currently accomplish these tasks? What tools/processes do they use?
- **Why:** Why do they struggle? What frustrates them? What motivates them?
- **Where:** In what context do they use the product? (Device, environment, time pressure)

**Focus by product value (Product→UX feed).** If AI-POLC value goals / OKRs / target outcomes were read in Stage 1 (peer `polc-state.md` present), use them to **focus and prioritize** the research questions: weight questions toward the segments and behaviors that drive POLC's value goals, and tag each question with the value goal it informs. This keeps research aimed at the users that matter to the product outcome rather than spreading evenly. If no POLC value goals are available, prioritize by the unknowns and stakeholder signals from the PIP/brief alone (standalone-safe).

**Format:**
```markdown
## Research Questions

| # | Question | Category | Priority | Focuses Value Goal (POLC) | Method |
|---|----------|----------|----------|---------------------------|--------|
| RQ1 | {question} | Who | High | {OKR/value goal ref or —} | {method} |
| RQ2 | {question} | What | High | {OKR/value goal ref or —} | {method} |
```

### Step 2: Synthesize Existing Data

Extract user-relevant information from available inputs:

**From PIP (Mode A/B):**
- Stakeholder register → user groups and their interests
- Scope statement → who's in scope, who's out
- Requirements → implied user needs and workflows
- Feasibility assessment → user-facing constraints

**From AP (Mode A):**
- System context → external actors (these are users or adjacent systems)
- Container diagram → user-facing containers (web app, mobile app, portal)
- Security architecture → user authentication flows, access patterns
- API architecture → user-initiated operations

**From product brief (Mode C):**
- Target audience descriptions
- Competitive analysis insights
- User feedback/research already conducted
- Analytics data if available

**From existing design (Mode D):**
- Current user base data
- Support tickets / pain point patterns
- Analytics (most-used features, drop-off points)
- Existing persona documents (assess currency)

**From AI-POLC (any mode, if `polc-state.md` present — Product→UX feed):**
- Value goals / OKRs / target outcomes → use to **focus** which segments and questions matter most
- Target segments POLC is prioritizing → cross-check against UX-discovered segments
- Success metrics / north-star → frame "what good looks like" for the experience
- Treat POLC direction as a focusing lens, not a substitute for user evidence — research still validates/invalidates assumptions (standalone-safe if absent)

### Step 3: Plan Research Methods

For Standard and Comprehensive depth, recommend methods:

| Method | When to Use | Output |
|--------|-------------|--------|
| **Stakeholder interviews** | Always (even synthesized) | User segment confirmation, priority insights |
| **User interviews** | When direct user access exists | Goals, behaviors, pain points |
| **Surveys** | When quantitative validation needed | Segment sizes, priority ranking |
| **Card sorting** | When IA is complex or unfamiliar domain | Category mental models |
| **Tree testing** | When validating IA decisions | Navigation effectiveness |
| **Competitive analysis** | When market context matters | Pattern library, differentiation opportunities |
| **Analytics review** | When existing product data available | Behavioral patterns, drop-offs |
| **Contextual inquiry** | Comprehensive + physical/environmental context | Real-world usage patterns |

**At Comprehensive depth** also include:
- Empathy mapping methodology (Think/Feel/Say/Do framework)
- Diary study plan (for longitudinal behavior understanding)

### Step 4: Produce Research Synthesis

Consolidate all findings into a structured document:

```markdown
# Research Synthesis

## Executive Summary
{2-3 sentences: key user insight + primary opportunity}

## Research Questions & Findings

### RQ1: {question}
**Finding:** {answer}
**Evidence:** {source — PIP page X / interview quote / analytics data}
**Confidence:** High / Medium / Low
**Implication for design:** {what this means for UX decisions}

### RQ2: ...

## User Segments Identified
| Segment | Description | Estimated Size | Priority |
|---------|-------------|----------------|----------|
| {name} | {behavioral description} | {%} | {Primary/Secondary/Tertiary} |

## Key Themes
1. {Theme name} — {description + supporting evidence}
2. ...

## Opportunities
| # | Opportunity | Source | Confidence | Priority |
|---|-------------|--------|------------|----------|
| 1 | {description} | {RQ reference} | {level} | {H/M/L} |

## Unknowns Remaining
{What we still don't know — feeds into ongoing research during later stages}
```

### Step 5: Present for Approval

Present the research synthesis to the user:
- Highlight key findings
- Confirm user segments (these become personas in Stage 3)
- Flag any disagreements between sources
- Note confidence levels on each finding

---

## Gate

**Approval required before proceeding to Stage 3.**

User must confirm:
- User segments identified are correct and complete
- Research findings are accurate (no misinterpretation of PIP/AP/brief)
- Priority ordering of segments is agreed
- Remaining unknowns are acknowledged (will be addressed in later stages or ongoing research)

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 2 with date and artifact (`01_Research_Synthesis.md`)
- Current Stage: 3

If design decisions were made (e.g., "focus on segment X first"): log in `management_framework/Decision_Log.md` as `UXD-D-NNN`.

---

## Transition

After gate approval:
```
Stage 2 complete. Research synthesis approved.

Moving to Stage 3: Persona Definition. I'll now transform the user
segments and research findings into evidence-backed personas with
goals, pain points, and behavioral patterns.
```

Load `discover/persona-definition.md`.
