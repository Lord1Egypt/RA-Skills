<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 5: Epic Decomposition

**Phase:** Strategy
**Purpose:** Break product goals into epics — the structural hierarchy that makes every story traceable to business value. Each epic is a governed unit with clear acceptance criteria and goal linkage.

---

## MANDATORY: Stage Sub-Role

During this stage, also adopt the **Business Analyst** sub-role:

### Behavioral Shifts
- Think in terms of requirement decomposition: goal → capability → epic → (story)
- Ensure each epic is bounded, testable, and independently valuable
- Challenge epics that are too broad ("improve user experience") or too narrow ("change button color")
- Map dependencies between epics explicitly

### Anti-Patterns
- Do NOT produce epics that are just re-worded goals — epics are concrete capabilities, not aspirations
- Do NOT prescribe implementation decomposition — that's AI-DLC v1's job (epic-to-story breakdown is DLC Inception)
- Do NOT create epics without acceptance criteria — every epic needs a testable definition of "done at epic level"
- Do NOT skip dependency mapping — undetected dependencies cause sprint failures

### Quality Check
Every epic must pass: "Can a development team read this and understand WHAT to deliver (not how) and WHEN it's done (acceptance criteria)?" If no → refine.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | 3-8 epics. One-line AC per epic. Minimal dependency mapping. |
| **Standard** | 5-15 epics. 3-5 AC per epic. Dependency matrix. Size estimation (S/M/L/XL). |
| **Comprehensive** | 10-30 epics. Detailed AC. Full dependency graph. Risk per epic. Cross-team coordination epics identified. |

---

## Steps

### Step 5.1: Identify Epics From Goals and Roadmap

For each product goal and roadmap "Now" item, ask: "What capabilities must exist for this goal to be achieved?"

```
Goal: "Reduce payment processing time to <2s"
├── Epic: Enable async payment processing
├── Epic: Implement payment provider caching
└── Epic: Add payment performance monitoring

Goal: "Support 3 payment providers"
├── Epic: Build provider abstraction layer
├── Epic: Integrate Stripe
├── Epic: Integrate PayPal
└── Epic: Integrate Bank Transfer
```

**Rules:**
- Each epic serves exactly one goal (or clearly stated multiple goals)
- Each epic is independently deliverable (not dependent on ALL other epics completing first)
- Each epic name starts with a verb (Enable, Build, Integrate, Implement, Create, Establish)

### Step 5.2: Write Epic Definitions

For each epic, create a definition file in `epics/EPIC-NNN_{name}.md`:

```markdown
---
generatedBy: AI-POLC
generatedVersion: 1.0.0
source: {goal reference}
generatedOn: {ISO-date}
ownership: hybrid
---

# EPIC-{NNN}: {Epic Name}

## Goal Linkage
- Serves: {Goal name + metric}
- Theme: {Strategic theme}
- Roadmap Horizon: {Now | Next | Later}

## Description
{2-3 sentences: what this epic delivers, why it matters, who benefits}

## Acceptance Criteria (Epic Level)
- [ ] {Criterion 1 — testable}
- [ ] {Criterion 2 — testable}
- [ ] {Criterion 3 — testable}

## Dependencies
- Depends on: {EPIC-XXX or "none"}
- Blocks: {EPIC-YYY or "none"}
- External: {any external dependency}

## Size Estimate
- Complexity: {S | M | L | XL}
- Rationale: {one sentence why this size}

## Context-Aware Notes
{Any notes from context factors — e.g., "DDD architecture means this epic maps to the Payment bounded context"}
```

### Step 5.3: Map Dependencies

Build a dependency matrix:

| Epic | Depends On | Blocks | External Deps |
|------|-----------|--------|---------------|
| EPIC-001 | — | EPIC-003 | — |
| EPIC-002 | — | EPIC-004 | Payment provider API access |
| EPIC-003 | EPIC-001 | — | — |
| EPIC-004 | EPIC-002 | — | — |

Flag circular dependencies as errors. Flag long dependency chains (>3 deep) as risks.

### Step 5.4: Context-Factor Adaptation

| Context Factor | Epic Decomposition Impact |
|---|---|
| Architecture = DDD | Epics should align to bounded contexts where natural |
| Architecture = Microservices | Epics may span services — flag coordination needs |
| Scale = Multi-team | Add "coordination epics" for cross-team work |
| Compliance = Heavy | Add mandatory compliance epics (audit trail, data retention, consent) |
| Tech Debt = High | Identify refactoring epics; mark them explicitly as tech-debt |

### Step 5.5: Validate Epic Set

Check the complete epic set against:
- [ ] Every "Now" roadmap item has at least one epic
- [ ] Every product goal has at least one epic serving it
- [ ] No orphan epics (every epic links to a goal)
- [ ] No duplicate/overlapping epics
- [ ] Dependencies are acyclic
- [ ] Size distribution is reasonable (not all XL; not all S)

### Step 5.6: Tier 2 Integration Point

If Tier 2 is active (story elaboration enabled):
- After each epic is confirmed, decompose it into INVEST-compliant stories
- Load `tier2/story-elaboration.md` for story writing rules
- Stories become sub-items under the epic

If Tier 2 is inactive (default in chain mode):
- Epics are the terminal output of this stage
- AI-DLC v1's Inception will decompose epics into stories later

**On-the-fly Tier 2 offer:** POLC does NOT silently assume the Tier 2 setting. At the Stage 5 gate (Step 5.7 below), it explicitly asks the user whether to keep Tier 2 off (epics are the handoff) or turn it on now (elaborate stories). The user can flip this decision at any time during the workflow, not only here — if they later say "elaborate stories", activate Tier 2 and return to this integration point for the confirmed epics.

### Step 5.7: Offer Tier 2 at the Gate

Before closing the stage, surface the Tier 2 choice as a structured question so the user makes an informed, explicit decision:

```
### Q-5T: Story elaboration (Tier 2)

Context: Epics are confirmed. By default I stop at the epic level — in chain
mode AI-DLC v1 elaborates these into user stories during its Inception phase.
You can keep it there, or have me (POLC) write PO-quality user stories now.

Options:
  a) No — keep Tier 2 OFF; epics are the handoff artifact
  b) Yes — turn Tier 2 ON now; I'll elaborate stories (you'll then pick the format)

Recommended: (a) in chain mode with AI-DLC v1 present · (b) in standalone mode
or when you want PO-quality pre-elaboration before development.

Rationale: {state-derived — mention detected mode and whether AI-DLC v1 is chained}

Your Decision: _[awaiting input]_
```

- **On (a) "No":** set `Tier 2: inactive` in `polc-state.md`, log the decision, proceed to Gate 5.
- **On (b) "Yes":** set `Tier 2: active` in `polc-state.md`, load `tier2/story-elaboration.md`, ask the story-format question (Q2), then elaborate stories per confirmed epic before proceeding.
- Skip Q-5T only if the user has ALREADY explicitly set the Tier 2 state earlier in the session (then just confirm the recorded setting in one line).

---

## Gate

**Gate 5 — Epics Confirmed:**

Present to user:
```
Epic decomposition complete:
• Total epics: {N}
• By theme: {Theme A: N, Theme B: N, ...}
• Dependencies: {N} inter-epic dependencies identified
• Size distribution: {S: N, M: N, L: N, XL: N}
• Coverage: All {N} goals have serving epics ✅
• Tier 2 (story elaboration): {ON — format: {style} | OFF — epics are the handoff}

Review the epic list. Any additions, removals, or adjustments?
Approve to proceed to Prioritization.
```

User must confirm before proceeding.

---

## Governance Spine Entry

Log in Decision Log:
```
POLC-D-004: Epic decomposition complete. {N} epics defined across {N} themes.
Size distribution: {summary}. Dependencies: {N} identified.
All product goals covered.
```

---

## Transition

→ **Stage 6: Value-Based Prioritization** (Strategy continues)

---

*Detail file for AI-POLC Stage 5 | Phase: Strategy*
