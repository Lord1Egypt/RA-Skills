<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 2: Shape

**Lead persona:** `#persona-product-manager`
**Sub-role:** `#persona-subrole-business-analyst` (requirements decomposition, ambiguity detection)
**Execution:** ALWAYS
**Purpose:** Turn a vague notion into a structured problem/solution statement through guided conversation.

---

## Why This Stage Exists

A raw idea ("what about X?") can't be evaluated. Shaping turns it into something assessable: a clear problem, a defined beneficiary, explicit capabilities, and stated boundaries. Without this, evaluation becomes subjective guesswork.

---

## Depth Adaptation

| Depth | Shaping Behavior |
|-------|-----------------|
| **Minimal** | 3 core questions only (problem, who benefits, rough scope). Fast, assumption-heavy — user can correct later. |
| **Standard** | Full 5-section shaping: problem, current state, desired state, capabilities, boundaries. One iteration with user. |
| **Comprehensive** | Full shaping + prior art exploration + stakeholder impact + dependency mapping. Multiple iterations until user confirms completeness. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Read `ilc-state.md` — confirm idea name, captured content, depth level, domain signal
2. Review what the user provided at Capture (their raw words)
3. Activate the Business Analyst sub-role lens: focus on ambiguity detection, gap identification, and requirements structuring

### Step 2: Ask Shaping Questions

Present questions adapted to depth level:

#### Minimal Depth (3 questions)

```markdown
### Q-{nn}: What problem does this solve?
**Context:** We need a clear problem statement to evaluate against.
→ In one or two sentences, what pain or gap does this idea address?

### Q-{nn}: Who benefits and how?
**Context:** Knowing the beneficiary helps us assess value and urgency.
→ Who is the primary user/beneficiary, and what do they gain?

### Q-{nn}: How big is this?
**Context:** Scale affects depth of evaluation and routing.
**Options:**
- (a) Small — a bounded feature or improvement
- (b) Medium — a significant capability or initiative
- (c) Large — a new product, platform, or strategic bet
**Recommended:** {based on Capture signals}
```

#### Standard Depth (5 sections)

Ask for each section (present as a batch per `question-format-guide.md`):

1. **Problem Statement** — What specific problem does this solve? Be precise.
2. **Current State** — How do people handle this today? What's painful?
3. **Desired State** — What does the world look like after this exists?
4. **Key Capabilities** — What would it do? (3-5 bullet points)
5. **Explicit Boundaries** — What would it NOT do? (2-3 exclusions)

#### Comprehensive Depth (5 sections + extensions)

All Standard sections, PLUS:
6. **Prior Art / Inspiration** — What existing solutions, frameworks, or tools inspired this?
7. **Stakeholder Impact** — Who else is affected beyond the primary beneficiary?
8. **Dependencies** — What must exist or be true for this to work?
9. **Risks (early signal)** — What could make this harder than it looks?

### Step 3: Domain Refinement

Based on the user's shaping answers, refine the domain detection:

| Keywords / Themes | Domain |
|-------------------|--------|
| Components, APIs, system design, microservices, data models | architecture |
| Compliance, audit, hooks, rules, enforcement, standards | governance |
| Pipeline, deployment, workspace, repo, infrastructure | devops |
| Testing, QA, coverage, validation, regression | testing |
| License, IP, attribution, commercial, open-source | licensing |
| Project, charter, stakeholders, governance, PMO | pmo |
| Process, workflow, stages, gates | process |
| None of the above / mixed | general |

Update `ilc-state.md` → Domain Detected if refined.

### Step 4: Produce the Idea Statement

Synthesize the user's answers into a structured **Idea Statement** (internal working document):

```markdown
# Idea Statement: {Idea Name}

## Problem
{synthesized from user's answers}

## Current State (without this)
{how people handle it today}

## Desired State (with this)
{what changes}

## Key Capabilities
1. {capability}
2. {capability}
3. {capability}
...

## Boundaries (what it does NOT do)
1. {exclusion}
2. {exclusion}
...

## Domain: {detected domain}
## Scale: {small / medium / large}
## Beneficiary: {primary user/persona}

{Additional sections if Comprehensive depth:}
## Prior Art
## Stakeholder Impact
## Dependencies
## Early Risk Signals
```

### Step 5: Present for Review

Present the Idea Statement to the user:

```
Here's the structured version of your idea:

{Idea Statement content}

Does this accurately capture what you're thinking?
[Approve / Adjust sections / Add more detail / Restart shaping]
```

### Step 6: Iterate (if needed)

- If user says "Approve" → finalize
- If user adjusts → incorporate changes, re-present the adjusted sections only
- If Comprehensive depth → expect 2-3 iterations before finalization
- If user says "Restart" → clear shaping, go back to Step 2

### Step 7: Finalize

1. Save the final Idea Statement (internal working doc — NOT the handoff brief) into the idea's subfolder as `{NNN}-{idea-slug}/Idea_Statement.md` (path from `ilc-state.md` → Idea Folder)
2. Update `ilc-state.md`:
   - Status: Shaped
   - Current Stage: 3 (ready for Evaluate)
   - Domain Detected: {refined value}
3. Update Idea Register: Status = Shaped
4. Log in Decision Log: "D-{nn} | Idea shaped and confirmed. Domain: {X}. Scale: {Y}. Beneficiary: {Z}."

---

## Gate

**Condition to proceed:** User approves the Idea Statement.

**Acceptable user responses:**
- "Approved" / "Looks good" / "Yes" → proceed to Stage 3
- "Adjust {section}" → iterate, then re-gate
- "Park this" → set Status = Parked; log rationale; close cleanly
- "This isn't worth pursuing" → offer to jump to Reject (skip evaluation) or continue to Evaluate for a formal score

**Post-gate actions:**
1. Log shaping decision in Decision Log
2. Update state to Stage 3

---

## Transition Message

```
───────────────────────────────────────────────────────
Moving to Stage 3: EVALUATE

Now that we have a clear picture of what this idea IS,
I'll score it against consistent criteria and build a
value analysis. This tells us: should we pursue it?

Activating: Financial Analyst lens (value scoring,
investment framing, cost-of-not-doing)
───────────────────────────────────────────────────────
```

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| User already provided a fully-shaped proposal at Capture | Validate it against the 5 sections; fill gaps with quick questions; don't force redundant answers |
| User can't articulate the problem clearly | Use the BA lens to help: "It sounds like the pain is {X} — is that right?" Offer framings to react to rather than blank-page questions |
| User's idea scope grows during shaping | Flag it: "This is getting larger than originally captured (was Small, now looks Medium/Large). Should I adjust the depth?" |
| User contradicts themselves between sections | Surface the contradiction explicitly: "In the problem statement you said X, but in capabilities you said Y — which is the intent?" |
| Idea is clearly identical to something that exists | Flag honestly: "This sounds similar to {existing thing}. Is the idea to replace it, extend it, or differentiate from it?" |

---

*Version: 1.0.0 | Part of AI-ILC — AI-Driven Idea Life Cycle*
