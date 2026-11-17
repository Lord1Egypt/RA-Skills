<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 6: Dispatch Authorization

**Phase:** Authorization & Dispatch
**Purpose:** For projects marked "Admit" or "Resume" at the governance gate, produce the authorization signal that AI-FLO carries across the layer boundary to activate Project-layer packages.

---

## Layered Communication Rule

> **AI-PPM NEVER activates Project-layer packages directly.** Dispatch authorizations are placed for AI-FLO to read and carry across the layer boundary. FLO decides which Project-layer packages to activate based on the authorization scope.

**Fallback (no FLO):** The dispatch authorization document serves as a manual reference for the user to start the appropriate Project-layer packages themselves, pointing at the PIP location.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Simple authorization: Project ID + "proceed." No constraints beyond PIP. |
| **Standard** | Full authorization with scope, constraints, priority, and required packages. |
| **Comprehensive** | Full authorization + inter-project sequencing + capacity allocation + milestone targets. |

---

## Step-by-Step Execution

### Step 6.1: Identify Projects to Dispatch

From Stage 5 decisions, collect all projects with new state = `Authorized`:

```
📤 Projects ready for dispatch:
| # | Project | ID | Priority | Decision |
|---|---------|-----|:--------:|----------|
| 1 | {A} | {ID} | #1 | Admit |
| 2 | {B} | {ID} | #2 | Resume |
```

### Step 6.2: Determine Authorization Scope Per Project

For each project, define what the Project layer is authorized to do:

```
Q-{NN}: Authorization scope for {Project Name}

(a) Full execution — activate all applicable Project-layer packages (POLC leads → UXD + ADLC concurrent → DWG → GCE + TGE → DLC)
(b) Design phase only — activate POLC (lead) + UXD + ADLC; await further authorization before DWG/DLC
(c) Specific packages only — select which: [ ] POLC [ ] UXD [ ] ADLC [ ] DWG [ ] GCE [ ] TGE
(d) Custom scope: ___

Recommended: (a) for top-priority projects with clear requirements; (b) for projects with high uncertainty.
```

> **Project-layer entry — AI-POLC leads.** When AI-FLO opens the Project layer, **AI-POLC is the default first package** (problem/value framing), with AI-UXD and AI-ADLC concurrent. POLC-first is an information-gradient hint, not a hard prerequisite. AI-PPM declares the scope; AI-FLO performs the ordered dispatch.

### Step 6.3: Define Constraints

For each authorized project, capture execution constraints:

| Constraint | Source | Example |
|---|---|---|
| **Budget ceiling** | PIP Business Case / governance override | "Do not exceed $500K without re-authorization" |
| **Timeline deadline** | PIP Charter / market window | "Must deliver MVP by Q3 2026" |
| **Team allocation** | Portfolio capacity decision | "Maximum 5 FTEs from Platform team" |
| **Dependencies** | Cross-project from Stage 4 | "Cannot start DWG until Project X releases shared infra" |
| **Reporting** | Portfolio governance cadence | "Monthly roll-up required via FLO" |

### Step 6.4: Produce Dispatch Authorization

Generate one document per project in `dispatch-authorizations/`:

```markdown
---
generatedBy: AI-PPM
generatedVersion: 1.0.0
source: portfolio-governance
generatedOn: {ISO-date}
ownership: generated
---

# Dispatch Authorization: DA-{Project-ID}

## Authorization Summary

| Field | Value |
|-------|-------|
| **Project ID** | {ID} |
| **Project Name** | {name} |
| **Priority Rank** | #{rank} of {total} |
| **Authorization Type** | {Admit / Resume} |
| **Governance Decision** | PGD-{NNN} |
| **Authorized On** | {ISO-date} |

## Scope

| Aspect | Authorization |
|--------|--------------|
| **Execution scope** | {Full / Design-only / Custom} |
| **Required packages** | {POLC, UXD, ADLC, DWG, GCE, TGE — as applicable} |
| **Parallel/Sequential** | {POLC leads → UXD + ADLC concurrent; all three converge at DWG (default gate = all three); then GCE+TGE+DLC} |

## Constraints

| Constraint | Value | Enforcement |
|---|---|---|
| Budget ceiling | {amount} | Re-authorize if exceeded |
| Timeline | {deadline} | Escalate if at risk |
| Team allocation | {max FTE / specific teams} | No reallocation without PPM approval |
| Dependencies | {list} | Block until satisfied |

## Source Location

| Artifact | Path |
|---|---|
| PIP | {pilc-state.md location} |
| ILC Brief (if applicable) | {ilc-state.md location} |
| Portfolio Register entry | {portfolio-register.md} |

## Roll-Up Requirement

This project MUST provide portfolio roll-up data via AI-FLO at the cadence specified in the portfolio governance schedule. Minimum fields: progress_pct, rag_status, budget_actual, top_blocker.

## Revocation Conditions

This authorization is revoked if:
- Budget ceiling is exceeded without re-authorization
- Timeline deadline passes without delivery or extension request
- Portfolio rebalancing (Stage 9) changes this project's priority below the cut line
- User explicitly pauses or retires the project (Stage 5 re-decision)
```

### Step 6.5: Update State

- Update `ppm-state.md`: add dispatched project IDs, update session history
- Update `portfolio-register.md`: change state from `Authorized` → `Active`
- Log: timestamp of dispatch per project

### Step 6.6: Transition Message

```
✅ Dispatch authorizations issued

| Project | ID | Priority | Scope | Status |
|---------|-----|:--------:|-------|--------|
| {A} | {ID} | #1 | Full | 📤 Dispatched |
| {B} | {ID} | #2 | Design-only | 📤 Dispatched |

FLO status: {Connected — FLO will activate packages | Not connected — manual start required}

{If no FLO:}
📋 Manual activation guide (POLC leads the Project layer):
   1. Start AI-POLC pointing at: {PIP path}   ← leads (problem/value)
   2. Start AI-UXD pointing at: {PIP path}    ← concurrent (experience)
   3. Start AI-ADLC pointing at: {PIP path}   ← concurrent (feasibility)
   (Three run concurrently and converge at AI-DWG, whose default gate waits
    for all three — POLC-first is a gradient hint, not a blocker. See
    FAMILY_STRUCTURE.md for Project-layer flow.)

⚠️ **IMPORTANT: Start each Project-layer package in a NEW session.**
   Each AI-* package loads a full workflow into context;
   a fresh session keeps it fast and focused.

Next actions available:
(a) Register another project
(b) Run portfolio health review (Stage 7-8)
(c) End session — portfolio is governed

What would you like to do?
```

---

## Gate

No explicit gate — dispatch is the result of the governance gate (Stage 5). However, user confirms the scope and constraints for each dispatch.

---

## Outputs

| Artifact | Status |
|---|---|
| `dispatch-authorizations/DA-{project-id}.md` | Created (one per dispatched project) |
| `portfolio-register.md` | Updated (Active state) |
| `ppm-state.md` | Updated (dispatched IDs, session history) |

---

## Management Framework Contribution

Entry: `PPM-D-{NNN}: Dispatch issued for {Project Name} ({ID}). Scope: {full/design/custom}. Constraints: budget {X}, timeline {Y}. FLO: {connected/manual}.`

---

*This stage follows immediately after the governance gate for admitted projects.*
