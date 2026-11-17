<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 4: Scope

**Lead persona:** `#persona-process-designer`
**Sub-role:** `#persona-subrole-resource-planner` (WBS-like boundary setting, effort estimation, dependencies)
**Execution:** CONDITIONAL — only if Stage 3 (Evaluate) = Proceed
**Purpose:** Define what's in vs. out, estimate rough effort, and identify dependencies and risks — so the go/no-go decision in Stage 5 is informed by realistic boundaries.

---

## Why This Stage Exists

Evaluation tells us an idea is WORTH doing. Scoping tells us what "doing it" MEANS — and at what cost. Without scope, "approved" ideas arrive at their destination undefined, leading to scope creep, misaligned expectations, and wasted effort. A scoped idea is a bounded idea.

---

## Depth Adaptation

| Depth | Scoping Behavior |
|-------|-----------------|
| **Minimal** | In/out list + T-shirt effort estimate. No dependency mapping. Single question batch. |
| **Standard** | Structured scope: included, deferred, dependencies, risks, effort estimate. One iteration. |
| **Comprehensive** | Full scope with phased delivery, resource implications, explicit trade-offs, dependency chain, and risk mitigation strategies. Multiple iterations. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Read `ilc-state.md` — confirm idea is Evaluated (Proceed), load depth
2. Load the Idea Statement from Stage 2
3. Load the Evaluation score and Value Analysis from Stage 3 (use low-scoring criteria to inform risk/boundary decisions)
4. Activate the Resource Planner sub-role: think in terms of work decomposition, estimation, and constraint management

### Step 2: Define Scope Boundaries

Ask the user to confirm or adjust:

```markdown
### Q-{nn}: What MUST be included?

**Context:** Defining the "first version" boundary — what's essential for this idea to deliver its core value?

Based on your shaped capabilities, I'd suggest these are essential:
1. {capability 1 from Idea Statement}
2. {capability 2}
3. {capability 3}

Are these right? Add/remove/adjust: _[awaiting input]_
```

```markdown
### Q-{nn}: What is explicitly DEFERRED (not now)?

**Context:** Naming what's OUT prevents scope creep. These are valid but not first-version.

Based on your boundaries from shaping, I'd suggest deferring:
1. {exclusion 1 — reframed as "deferred to later"}
2. {optional capability — if any}
3. {nice-to-have identified during evaluation}

Agree with these deferrals? Adjust: _[awaiting input]_
```

### Step 3: Dependencies (Standard + Comprehensive only)

```markdown
### Q-{nn}: What must exist or be true for this to work?

**Context:** Dependencies are things OUTSIDE this idea that it relies on. If they're missing, the idea is blocked.

I've identified these potential dependencies from your shaping:
- {dependency 1 — if any were mentioned}
- {dependency 2}

Any others? Or confirm these: _[awaiting input]_
```

### Step 4: Risks (Standard + Comprehensive only)

```markdown
### Q-{nn}: What could go wrong or make this harder than expected?

**Context:** Naming risks now means we can plan for them, not be surprised by them.

From the evaluation, these scored lowest and signal risk:
- {lowest-scoring criterion}: {what it implies}
- {second-lowest}: {what it implies}

Any other risks you see? _[awaiting input]_
```

### Step 5: Effort Estimate

```markdown
### Q-{nn}: Rough Effort Estimate

**Context:** Not a commitment — a directional signal for the decision-maker.

**Options:**
- (a) Small — days to 1-2 weeks; one person could handle it
- (b) Medium — 2-6 weeks; small team needed
- (c) Large — 1-3 months; dedicated team or significant resources
- (d) X-Large — 3+ months; major initiative, multiple teams

**Recommended:** ({x}) — based on {scope size, dependency count, risk level}
**Rationale:** {explanation}

**Your Decision:** _[awaiting input]_
```

### Step 6: Comprehensive-Only Extensions

If depth = Comprehensive, additionally:

**Phased delivery:**
```markdown
### Q-{nn}: Should this be delivered in phases?

**Context:** Large initiatives often benefit from phased delivery — ship value incrementally.

**Options:**
- (a) Single delivery — build it all, ship once
- (b) Phased — Phase 1 = {core}, Phase 2 = {extensions}
- (c) Let me define the phases: ___

**Recommended:** {based on scope size and risk}
```

**Trade-offs:**
- What would you sacrifice to ship faster? (scope vs. time vs. quality)
- What's the minimum viable version that still delivers the core value?

### Step 7: Produce Scope Summary

Compile the scope into a structured summary:

```markdown
## Scope Summary: {Idea Name}

### Included (v1 / first version)
1. {item}
2. {item}
3. {item}

### Deferred (explicitly not now)
1. {item} — Rationale: {why later}
2. {item} — Rationale: {why later}

### Dependencies
- {dependency} — Status: {met / unmet / unknown}

### Risks
- {risk} — Mitigation: {approach}

### Effort Estimate
- **Size:** {S / M / L / XL}
- **Timeline signal:** {rough duration}
- **Team signal:** {solo / small team / dedicated team}

{If Comprehensive:}
### Phased Delivery
- Phase 1: {scope} — {timeline}
- Phase 2: {scope} — {timeline}
```

### Step 8: Present for Agreement

```
Here's the scope definition for "{idea_name}":

{Scope Summary}

Does this accurately bound the idea?
[Agree / Adjust included / Adjust deferred / Change effort / Add risks]
```

### Step 9: Finalize

1. Update `ilc-state.md`:
   - Status: Scoped
   - Current Stage: 5 (ready for Approve)
2. Update Idea Register: Status = Scoped
3. Log in Decision Log: "D-{nn} | Scope agreed. Size: {X}. {n} items included, {m} deferred. Dependencies: {count}. Risks: {count}."

---

## Gate

**Condition to proceed:** User agrees on the scope (explicitly, not implied).

**Acceptable responses:**
- "Agree" / "Confirmed" / "Good" → proceed to Stage 5
- "Adjust {section}" → iterate, re-present, re-gate
- "This is too big — park it" → Park with rationale
- "Reduce scope" → re-do Step 2 with tighter constraints

**Post-gate actions:**
1. Decision logged
2. State updated to Stage 5

---

## Transition Message

```
───────────────────────────────────────────────────────
Moving to Stage 5: APPROVE

Scope is defined. Now the formal decision: should this
idea be approved, parked, or rejected? I'll present the
full picture and ask for your explicit call.

Activating: Risk Analyst lens (challenge assumptions,
assess feasibility risks, stress-test readiness)
───────────────────────────────────────────────────────
```

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| User says "just build it, skip scope" | Explain why: "Scope protects you from the idea growing silently. Even 3 bullet points of 'in' and 'out' is enough at Minimal depth." Offer Minimal-depth scoping. |
| Scope grows during the conversation | Flag: "Scope is expanding — this started as {size} but now looks like {larger}. Should I adjust the effort estimate?" |
| All items are "must have" (nothing deferred) | Challenge: "If nothing is deferrable, the idea may be too tightly coupled. Is there a phased approach where core value ships first?" |
| User can't estimate effort | Offer anchoring: "Similar ideas at this scope tend to be {size}. Does that feel directionally right?" Don't force precision. |
| Dependencies are all unmet | Flag risk: "Multiple unmet dependencies increase the chance this blocks. Consider: should we park until {key dependency} resolves?" |

---

*Version: 1.0.0 | Part of AI-ILC — AI-Driven Idea Life Cycle*
