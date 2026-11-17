<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 10: Project Retirement & Closure

**Phase:** Optimization
**Purpose:** Formally remove a project from the active portfolio — whether completed successfully, cancelled, or superseded. Retirement captures final state, records lessons, releases capacity, and updates the portfolio register.

---

## MANDATORY: Stage Sub-Role — Change Manager

During THIS stage, ALSO adopt the mindset of a **Change Manager**. This does NOT replace your primary role (Portfolio Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think about organizational impact of closure: who needs to know? What changes for teams?
- Capture lessons that improve FUTURE portfolio governance (not just project lessons)
- Ensure clean resource release: capacity genuinely freed, not just on paper
- Close the loop: did this project deliver what was promised when admitted?

### Anti-Patterns for This Stage
- Do NOT retire without recording the retirement reason
- Do NOT skip the lessons step — portfolio lessons are different from project lessons

### Quality Check
A good retirement sounds like:
- "Project A retired (Completed). Actual: 14 months, $480K (planned: 12 months, $450K — +7% budget, +17% timeline). Benefits: partially realized (3 of 5 KPIs on track; 2 require 6 more months to measure). Portfolio lesson: our ROM estimates for infrastructure projects are systematically 15% low — adjust future scoring."

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Record reason + final state. Update register. Release capacity. Done. |
| **Standard** | Full retirement record: reason, actuals vs. planned, lessons, benefit status. |
| **Comprehensive** | Full record + benefits handover plan + portfolio governance lessons + contribution to scoring model improvement. |

---

## Retirement Reasons

| Reason | Meaning | Typical Trigger |
|---|---|---|
| **Completed** | Delivered its objectives — exiting successfully | FLO signals completion |
| **Cancelled** | Stopped before completion — deliberate decision | Governance gate decision |
| **Superseded** | Replaced by another initiative | New project made this one redundant |
| **Merged** | Combined with another project | Overlap detected; consolidated |
| **Failed** | Could not deliver — stopped due to inability | Persistent 🔴 + no viable path forward |

---

## Step-by-Step Execution

### Step 10.1: Confirm Retirement

```
Q-{NN}: Confirm retirement for {Project Name} (ID: {ID})

Current state: {Active / Paused}
Reason for retirement:
(a) Completed — delivered its objectives
(b) Cancelled — stopped by governance decision
(c) Superseded — replaced by {other project}
(d) Merged — combined with {other project}
(e) Failed — unable to deliver

Your selection: _[awaiting input]_
```

### Step 10.2: Capture Final State

Compare actuals against what was committed at admission (from original PIP / dispatch authorization):

```markdown
## Actuals vs. Planned

| Metric | Planned (at admission) | Actual (at retirement) | Variance |
|--------|:----------------------:|:---------------------:|:--------:|
| Duration | {N months} | {M months} | {+/- difference} |
| Budget | ${planned} | ${actual} | {+/- $amount} ({pct}%) |
| Scope delivered | {description} | {description} | {full / partial / exceeded} |
| Team size (peak) | {N FTE} | {M FTE} | {+/- N} |
| Priority rank (at admission) | #{rank} | #{final rank} | {change} |
```

### Step 10.3: Benefits Status

Record whether the project delivered the value that justified its admission:

```markdown
## Benefits Status

| Benefit (from Business Case) | Status | Evidence |
|------------------------------|:------:|----------|
| {benefit 1} | ✅ Realized | {measurement} |
| {benefit 2} | ⏳ Pending | {expected timeline for measurement} |
| {benefit 3} | ❌ Not realized | {reason} |

**Overall benefit realization:** {Fully / Partially / Not realized}
**Value delivered vs. promised:** {assessment}
```

If Extension E7 (Benefits Aggregation) is active: export final benefits data for portfolio-level aggregation.

### Step 10.4: Portfolio Lessons

Capture lessons that improve future PORTFOLIO governance (distinct from project-level lessons in the governance spine):

```
Q-{NN}: What did this project teach us about portfolio governance?

Consider:
- Was our prioritization model accurate? (Did high-ranked projects actually deliver more value?)
- Were our estimates reliable? (Budget, timeline — systematic bias?)
- Was the governance cadence appropriate? (Did we catch issues early enough?)
- Were resource allocation assumptions correct?
- Should our scoring criteria change based on this experience?

Portfolio lessons (enter 1-3):
```

Record in:
- `management_framework/Lessons_Learned.md` with prefix `PPM-L-{NNN}`
- `ppm-state.md` session history

### Step 10.5: Release Capacity

Update portfolio capacity tracking:

```markdown
## Capacity Released

| Resource | Allocation Released | Available From |
|----------|:-------------------:|:--------------:|
| {Team/role} | {N FTE / $amount} | {date} |
| {Budget} | ${amount} | Immediate |

**Impact on pending projects:** {which paused/held projects could now proceed}
```

If paused projects exist that were waiting for capacity: flag them as candidates for resumption.

### Step 10.6: Produce Retirement Record

Generate `retirement-record-{project-id}.md`:

```markdown
---
generatedBy: AI-PPM
generatedVersion: 1.0.0
source: portfolio-governance
generatedOn: {ISO-date}
ownership: generated
---

# Project Retirement Record: {Project Name}

| Field | Value |
|-------|-------|
| **Project ID** | {ID} |
| **Project Name** | {name} |
| **Retirement Reason** | {Completed / Cancelled / Superseded / Merged / Failed} |
| **Retirement Date** | {ISO-date} |
| **Active Duration** | {from admission to retirement} |
| **Governance Decision** | PGD-{NNN} (if via governance gate) |

## Actuals vs. Planned
{table from Step 10.2}

## Benefits Status
{table from Step 10.3}

## Portfolio Lessons
{from Step 10.4}

## Capacity Released
{from Step 10.5}

## Final Notes
{any additional context}
```

### Step 10.7: Update Portfolio Register

- Change project state: → `Retired`
- Add retirement date
- Move to bottom of register (or archive section)

### Step 10.8: Signal Downstream (Via FLO)

If FLO is connected:
- Signal: "Project {ID} retired — cease roll-up reporting"
- FLO stops carrying snapshots for this Project ID

If FLO not connected:
- Note in record: "Manual notification needed — tell Project-layer teams this project is formally closed"

### Step 10.9: Transition

```
✅ Project retired: {Name} (ID: {ID})
   Reason: {reason}
   Duration: {actual}
   Budget: ${actual} (variance: {pct}%)
   Benefits: {status}
   Capacity freed: {summary}

{If paused projects could resume:}
💡 Capacity freed — {Project X} (currently Paused) could now resume. 
   Trigger governance gate review? [Yes / Not now]

Portfolio register updated. Session complete.
```

---

## Gate

User confirms retirement is appropriate (especially for cancellation/failure reasons) before the record is finalized.

---

## Outputs

| Artifact | Status |
|---|---|
| Retirement record document | Created |
| `portfolio-register.md` | Updated (Retired state, date) |
| `management_framework/Lessons_Learned.md` | Updated (PPM-L-{NNN} entries) |
| `ppm-state.md` | Updated (project counts, session history) |

---

## Management Framework Contribution

Entries:
- `PPM-D-{NNN}: Project {name} ({ID}) retired. Reason: {reason}. Duration: {actual}. Budget variance: {pct}%.`
- `PPM-L-{NNN}: {Portfolio lesson learned from this retirement}`

---

*This stage runs whenever a project exits the portfolio — on completion signal, governance gate decision, or user request.*
