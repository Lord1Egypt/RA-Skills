<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 5: Approve

**Lead persona:** `#persona-product-manager`
**Sub-role:** `#persona-subrole-risk-analyst` (challenge assumptions, assess feasibility risks, stress-test readiness)
**Execution:** CONDITIONAL — only if Stage 4 (Scope) completes
**Purpose:** Explicit go/no-go decision with recorded rationale. This is THE moment the idea either becomes an initiative or is formally parked/rejected.

---

## Why This Stage Exists

An evaluated and scoped idea is not yet approved. Approval is an explicit, recorded act — it means: "We are committing to pursue this." Without a formal gate, ideas drift into action without accountability, or languish in limbo with no decision. AI-ILC requires that every idea gets one of three outcomes: Approved, Parked, or Rejected. All three are valid, governed results.

---

## Depth Adaptation

| Depth | Approval Behavior |
|-------|------------------|
| **Minimal** | Quick summary + single go/no-go question. Decision record is concise (1 page). |
| **Standard** | Full approval summary with score, scope, risks, recommendation. Decision record has all sections. |
| **Comprehensive** | Full summary + explicit risk challenge ("devil's advocate" pass) + conditions for approval + stakeholder alignment check. Decision record includes conditions and contingencies. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Read `ilc-state.md` — confirm idea is Scoped, load all accumulated context
2. Load: Idea Statement (Stage 2), Score + Value Analysis (Stage 3), Scope Summary (Stage 4)
3. Activate the Risk Analyst sub-role: challenge assumptions, look for what could fail, stress-test readiness

### Step 2: Produce Approval Summary

Present the complete picture in one view:

```markdown
## Approval Decision: {Idea Name}

### Summary
{One paragraph: what this idea is, what it does, who benefits}

### Score
**{n}/35** — {band} ({Strong Proceed / Proceed})

| Criterion | Score | Key Point |
|-----------|:-----:|-----------|
| Problem Clarity | {n} | {one phrase} |
| User Need | {n} | {one phrase} |
| Strategic Fit | {n} | {one phrase} |
| Differentiation | {n} | {one phrase} |
| Feasibility | {n} | {one phrase} |
| Reusability | {n} | {one phrase} |
| Chain Value | {n} | {one phrase} |

### Scope (agreed)
- **Included:** {n} items
- **Deferred:** {n} items
- **Effort:** {size} ({timeline signal})
- **Dependencies:** {count} ({met/unmet status})

### Value Proposition (from Value Analysis)
{2-3 sentences: why this matters}

### Key Risks
1. {risk 1} — Mitigation: {approach}
2. {risk 2} — Mitigation: {approach}
3. {risk 3} — Mitigation: {approach}

### Recommendation
**{APPROVE / PARK / REJECT}**
**Rationale:** {why this recommendation, grounded in evidence}
{If conditions exist:} **Conditions:** {what must remain true for this approval to hold}
```

### Step 3: Risk Challenge (Comprehensive depth only)

If depth = Comprehensive, before asking for the decision, run a "devil's advocate" pass:

```markdown
### Risk Challenge — Before You Decide

Playing devil's advocate, here are reasons this could fail:
1. {challenge 1 — from lowest-scoring criterion}
2. {challenge 2 — from unmet dependency}
3. {challenge 3 — from market/timing/feasibility concern}

**Counter-argument:** {why it's still worth proceeding despite these}

This is meant to stress-test, not discourage. Proceed? [Yes, with full awareness / Address a concern first / Park based on this]
```

### Step 4: Ask for Explicit Decision

```markdown
### Q-{nn}: Go / No-Go Decision

**Context:** This is the formal decision point. Your choice here is recorded and governs what happens next.

**Options:**
- (a) **APPROVE** — Proceed to routing and handoff. This idea becomes an initiative.
- (b) **PARK** — Valid idea, but not now. (I'll ask for a revisit date.)
- (c) **REJECT** — Doesn't fit or isn't viable. (I'll ask for the rationale to record.)

**Recommended:** ({x}) — {rationale}

**Your Decision:** _[awaiting input]_
```

### Step 5: Handle Decision

#### If APPROVE:
1. Ask for any conditions: "Are there conditions that must remain true for this approval? (e.g., 'only if budget is confirmed by Q3') Or unconditional?"
2. Proceed to Step 6

#### If PARK:
```markdown
### Q-{nn}: Revisit Date

**Context:** Parked ideas re-enter the pipeline when conditions change.

When should we revisit this?
- (a) Specific date: ___
- (b) When {condition} is met: ___
- (c) No specific date — I'll decide later

**Your Decision:** _[awaiting input]_
```

#### If REJECT:
```markdown
### Q-{nn}: Rejection Rationale

**Context:** Recording why helps future ideas avoid the same issues, and respects the effort that went into shaping.

Why is this idea being rejected?
- (a) Not strategically aligned (priorities changed)
- (b) Not feasible with current capabilities
- (c) Already covered by something else
- (d) Not enough value for the effort required
- (e) Other: ___

**Your Decision:** _[awaiting input]_
```

### Step 6: Produce Go/No-Go Decision Record

Create `{NNN}-{idea-slug}/{NNN}-{idea-slug}_GoNoGo_Decision_Record.md` (inside the idea's subfolder — path from `ilc-state.md` → Idea Folder). The record carries provenance front-matter (`generatedBy: AI-ILC`, `ownership: user`, `Status: {Approved/Parked/Rejected}`):

```markdown
# Go/No-Go Decision Record: {Idea Name}

| Field | Value |
|-------|-------|
| **Idea** | {name} |
| **Date** | {date} |
| **Decision** | {APPROVED / PARKED / REJECTED} |
| **Score** | {n}/35 ({band}) |
| **Effort** | {size} |
| **Decision Maker** | {user — as confirmed} |
| **Conditions** | {conditions if any, or "Unconditional"} |

## Rationale
{Why this decision was made — grounded in evaluation + scope + value analysis}

## Key Factors
- {factor 1}
- {factor 2}
- {factor 3}

## What Happens Next
{Route-specific: "Proceeds to routing" / "Revisit on {date}" / "Closed — archived in register"}

{If PARKED:}
## Revisit Plan
- **Revisit date/condition:** {value}
- **What would need to change:** {conditions for re-entry}

{If REJECTED:}
## Why Not
- **Primary reason:** {selected option}
- **Detail:** {user's explanation}
- **Could this be revisited?** {Yes if conditions change / No — fundamental misfit}
```

### Step 7: Finalize

1. Save the Decision Record to the idea's subfolder (`{NNN}-{idea-slug}/`)
2. Update `ilc-state.md`:
   - Status: Approved / Parked / Rejected
   - Current Stage: 6 (if Approved) or terminal (if Parked/Rejected)
3. Update Idea Register: Status + Decision columns
4. Log in Decision Log: "D-{nn} | Go/No-Go: {DECISION}. Score: {n}/35. Rationale: {summary}. Conditions: {if any}."

---

## Gate

**Condition to proceed to Stage 6:** Decision = APPROVED (explicit user confirmation).

**Terminal paths:**
- PARKED → Workflow pauses. State file persists. User can revisit later.
- REJECTED → Workflow closes. State file marked terminal. Idea remains in register for audit.

**Post-gate actions (if Approved):**
1. Decision Record saved
2. Decision logged
3. State updated to Stage 6

---

## Transition Message (if Approved)

```
───────────────────────────────────────────────────────
✅ APPROVED

Moving to Stage 6: ROUTE & HANDOFF

Now I need to determine where this approved idea goes.
I'll ask a few questions to understand: is this a new
project, a big change to an existing project, or a small
feature for the backlog?

Activating: Change Manager lens (impact assessment,
organizational readiness, adoption scope)
───────────────────────────────────────────────────────
```

## Closure Message (if Parked or Rejected)

```
───────────────────────────────────────────────────────
{PARKED / REJECTED}

📋 Idea: "{idea_name}"
📊 Score: {n}/35
📝 Decision: {PARKED — revisit {date/condition} / REJECTED — {reason}}
📄 Decision Record: {filename}

Idea Register and Decision Log updated.
{If PARKED: "I'll remind you when the revisit date arrives."}
{If REJECTED: "This idea stays in the register for future reference."}

Audit trail complete. Workflow closed cleanly.
───────────────────────────────────────────────────────
```

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| User says "Approve" without engaging the summary | Accept it — the user has authority. Log that approval was given after summary was presented. |
| User wants to approve with conditions | Capture conditions explicitly in the Decision Record; they carry into the brief at handoff |
| User changes mind after approving (same session) | Allow reversal: "Understood — changing decision to {Park/Reject}." Update all records. |
| Idea was Parked previously and is now being re-evaluated | Load previous context; note in Decision Record: "Previously parked on {date} — re-entering pipeline." |
| User asks someone else to make the decision | Log: "Decision deferred to {person}. Set as Pending Decision in state file." Do not proceed until decision is received. |

---

*Version: 1.0.0 | Part of AI-ILC — AI-Driven Idea Life Cycle*
