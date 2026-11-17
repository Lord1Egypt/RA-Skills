<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 5: Portfolio Governance Gate

**Phase:** Authorization & Dispatch
**Purpose:** Make explicit governance decisions about each project's fate: Admit, Pause, Resume, Retire, or Hold. This is the portfolio's control point — no project proceeds to execution without passing this gate.

---

## MANDATORY: Stage Sub-Role — Risk Analyst

During THIS stage, ALSO adopt the mindset of a **Risk Analyst**. This does NOT replace your primary role (Portfolio Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Challenge every "Admit" recommendation: what could go wrong?
- Identify resource contention BEFORE authorizing multiple projects
- Consider portfolio-level risk concentration (too many eggs in one basket?)
- Ask: "If this project fails, what's the blast radius to the portfolio?"

### Anti-Patterns for This Stage
- Do NOT rubber-stamp all projects — a gate that admits everything has no value
- Do NOT make decisions without surfacing trade-offs to the user

### Quality Check
A good governance decision sounds like:
- "Recommend ADMIT for Project A (#1, 84/100). Rationale: highest strategic alignment, no resource conflicts, within budget ceiling. Condition: must start before Q3 to capture market window. Review: if not started by {date}, reconsider."

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Simple Admit/Hold for each project. Brief rationale. No conditions. |
| **Standard** | Full 5-option decision per project. Conditions, review dates, impact analysis. |
| **Comprehensive** | Full decision + cumulative portfolio impact analysis + extension E6 (financial guardrails). |

---

## Portfolio Lifecycle States

Projects move through these states via governance decisions:

```
Registered → Prioritized → Authorized → Active → Retired
                              ↓      ↑
                            Paused ──┘
                              ↑
                   Hold (needs more info)
```

| State | Meaning |
|---|---|
| **Registered** | In the register but not yet prioritized |
| **Prioritized** | Scored and ranked but not authorized |
| **Authorized** | Approved for execution — waiting for dispatch |
| **Active** | Dispatched and executing in Project layer |
| **Paused** | Was active but temporarily halted (resource/timing reason) |
| **Hold** | Needs more information before authorization |
| **Retired** | No longer in active portfolio (completed/cancelled/superseded) |

---

## Step-by-Step Execution

### Step 5.1: Present Decision Context

Show the prioritized portfolio with current states and available information:

```
📋 Portfolio Governance Gate — {N} projects require decisions

| # | Project | ID | Rank | Score | Alignment | Current State | Health |
|---|---------|-----|:----:|:-----:|:---------:|:-------------:|:------:|
| 1 | {A} | {ID} | 1 | 84 | 21/25 | Prioritized | ⚪ |
| 2 | {B} | {ID} | 2 | 74 | 18/25 | Prioritized | ⚪ |
| 3 | {C} | {ID} | 3 | 52 | 12/25 | Prioritized | ⚪ |

Portfolio capacity: {context about available resources, budget ceiling, etc.}
Active projects already running: {N}
```

### Step 5.2: Present Each Decision

For each project requiring a governance decision, use the Governance Gate Question format (see `question-format-guide.md`):

```
GQ-{NN}: {Project Name} — Governance Decision

Project: {Name} (ID: {ID})
Current State: {state}
Priority Rank: #{rank} of {total}
Strategic Alignment: {score}/25
Risk Level: {from PIP}
Budget ROM: {range}

Decision Required:
(a) Admit — authorize execution via AI-FLO → Project layer activates
(b) Pause — authorized but deferred (specify reason)
(c) Hold — needs more information (specify what's needed)
(d) Retire — remove from portfolio (specify reason)
(e) No change — maintain current state

Recommended: {option}
Rationale: {specific evidence — score, capacity, alignment, timing}
Conditions: {what must be true for this to succeed}
Impact on others: {what this means for other portfolio projects}
Review Date: {when to revisit}

Your Decision: _[awaiting input]_
```

### Step 5.3: Cumulative Impact Check (Standard+ Depth)

After all individual decisions, present the cumulative impact:

```
📊 Cumulative Impact of Governance Decisions

| Decision | Project | Impact |
|----------|---------|--------|
| Admit | {A} | Consumes {X}% of available capacity |
| Admit | {B} | Consumes {Y}% — cumulative = {X+Y}% |
| Pause | {C} | Frees {Z}% capacity for {A} and {B} |

Portfolio capacity utilization after decisions: {total}%
Budget committed: ${amount} of ${ceiling} ({percent}%)
Risk concentration: {assessment}

⚠️ Warnings:
- {if over 90% capacity: "Near capacity ceiling — limited room for emergencies"}
- {if single team is over 100%: "Team {name} is over-allocated"}
- {if all projects in same risk category: "Concentration risk — all in {category}"}

Confirm all decisions? [Yes / Revise {specific project}]
```

### Step 5.4: Produce Governance Decision Records

For each decision, create a formal record in `portfolio-decisions/`:

```markdown
---
generatedBy: AI-PPM
generatedVersion: 1.0.0
source: portfolio-governance
generatedOn: {ISO-date}
ownership: generated
---

# Portfolio Governance Decision: PGD-{NNN}

| Field | Value |
|-------|-------|
| **Decision** | {Admit / Pause / Hold / Retire} |
| **Project** | {Name} (ID: {ID}) |
| **Previous State** | {state} |
| **New State** | {state} |
| **Priority Rank** | #{rank} |
| **Decided By** | {user role/name} |
| **Date** | {ISO-date} |

## Rationale
{Why this decision was made — referencing scores, capacity, alignment, timing}

## Conditions
{What must remain true for this decision to hold}

## Impact
- Portfolio capacity: {effect}
- Other projects: {effect}
- Resources: {effect}

## Review
- **Review Date:** {when}
- **Review Trigger:** {what would cause earlier review}
```

### Step 5.5: Update Portfolio Register

Update state for each project based on decisions made.

### Step 5.6: Transition Message

```
✅ Governance gate complete
   • {N} projects admitted → proceeding to Dispatch (Stage 6)
   • {M} projects paused
   • {K} projects on hold
   • {J} projects retired → Stage 10 for formal closure

Next: Dispatch Authorization for admitted projects.
Proceed? [Yes / Revisit a decision]
```

---

## Gate

Each governance decision requires explicit user confirmation. Batch "yes to all" is NOT permitted for governance gate decisions — each project is confirmed individually.

---

## Outputs

| Artifact | Status |
|---|---|
| `portfolio-decisions/PGD-{NNN}.md` | Created (one per decision) |
| `portfolio-register.md` | Updated (state transitions) |
| `ppm-state.md` | Updated (session history, project states) |

---

## Management Framework Contribution

Entry per decision: `PPM-D-{NNN}: Governance gate — {Project Name} ({ID}): {DECISION}. Rationale: {one-line}. Review: {date}.`

---

## Extension Check — Financial Governance (E6)

If Extension E6 is active:
- Apply lean budget guardrails before admitting
- Check: does this admission exceed the investment theme ceiling?
- Check: cumulative portfolio budget within approved envelope?
- If guardrail breached → flag and require override justification

---

*This stage runs whenever projects need governance decisions — after prioritization, during rebalancing, or on user request.*
