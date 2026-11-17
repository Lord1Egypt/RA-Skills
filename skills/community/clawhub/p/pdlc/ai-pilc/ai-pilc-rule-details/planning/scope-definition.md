<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Scope Definition

## Stage: 11 of 16
## Phase: 🟢 PLANNING
## Execution: ALWAYS

---

## Purpose

Transform the high-level scope from the Charter into a detailed, baselined Scope Statement with Work Breakdown Structure (WBS), deliverables table, milestone schedule, acceptance criteria, and change control process. This document becomes the scope baseline — any deviation requires a formal change request.

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS stage, ALSO adopt the mindset of a **Business Analyst**. This does NOT replace your primary role (PMO Professional / Senior Project Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Decompose scope into atomic, verifiable work packages before baselining
- Write acceptance criteria that are testable — "how would we prove this deliverable is done?"
- Make in-scope AND out-of-scope boundaries explicit; ambiguous boundaries become change-request disputes later
- Trace every WBS item back to a charter objective or a structured requirement

### Anti-Patterns for This Stage
- Do NOT leave scope boundaries implicit — state what is explicitly OUT of scope
- Do NOT create deliverables without acceptance criteria

### Quality Check
A good output at this stage sounds like:
- "WBS decomposed to 3 levels, 18 work packages, each with testable acceptance criteria; 6 explicit out-of-scope items to prevent creep..."

---

## Depth Adaptation

| Depth | WBS Levels | Deliverables Detail | Milestone Detail |
|-------|:----------:|--------------------:|:----------------:|
| **Minimal** | 2 levels (phases → work packages) | 8-12 deliverables, brief descriptions | 5-8 milestones, relative dates |
| **Standard** | 3 levels (phases → packages → tasks) | 12-20 deliverables with acceptance criteria | 8-12 milestones with gate decisions |
| **Comprehensive** | 4 levels (phases → packages → tasks → sub-tasks) with estimation | 15-25 deliverables, detailed criteria, ownership | 10-15 milestones, dependency chains, critical path indicators |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Project Charter (Stage 9) — high-level scope (in/out), objectives, milestones, constraints
2. Requirement Intake Form (Stage 3) — functional/NFR requirements
3. Clarification outcomes (Stage 5) — any scope-affecting decisions
4. Business Case (Stage 8) — recommended approach, phasing, timeline
5. Decision Log — all scope-related decisions made so far

---

### Step 2: Draft Scope Description

Produce a narrative scope description (2-4 paragraphs):

```markdown
## Project Scope Description

{Paragraph 1: What is being delivered — the solution/product/capability in plain language}

{Paragraph 2: Key architectural or approach characteristics — how it will be built/delivered}

{Paragraph 3: Scale and coverage — who it serves, how many users, geographic scope, language support}

{Paragraph 4 (Comprehensive only): Integration landscape and technical context}
```

**Rules:**
- Written for a non-technical executive to understand
- Derived from source requirements and Business Case approach
- Should answer: "What will exist at the end of this project that doesn't exist today?"

---

### Step 3: Define Scope Boundaries

#### In-Scope Table

```markdown
### In Scope

| # | Item | Description | Source Reference |
|---|------|-------------|:---------------:|
| 1 | {Capability/component name} | {What this includes — specific enough to verify} | {Req ID or source section} |
| 2 | {Item} | {Description} | {Reference} |
```

**Rules:**
- Every in-scope item must trace back to a requirement or decision
- Description should be specific enough that a stakeholder can confirm delivery
- Include supporting scope (security, infrastructure, training) not just features
- Number items sequentially for reference in WBS and elsewhere

#### Out-of-Scope Table

```markdown
### Out of Scope

| # | Item | Reason for Exclusion | Decided |
|---|------|---------------------|:-------:|
| 1 | {Excluded item} | {Deferred to v2 / Separate project / Not required / etc.} | D-{nnn} |
| 2 | {Item} | {Reason} | {Decision ref or source ref} |
```

**Rules:**
- Include items stakeholders might ASSUME are included
- Reference the decision that excluded them (from Decision Log or source)
- This is a defensive section — it prevents scope creep arguments later

---

### Step 4: Produce Deliverables Table

```markdown
## Deliverables

| # | Deliverable | Description | Acceptance Criteria | Owner |
|---|-------------|-------------|---------------------|-------|
| 1 | {Name} | {What it is — tangible artifact or outcome} | {How we know it's acceptable — measurable} | {Role} |
```

**Acceptance criteria guidance:**

| Type | Good Example | Bad Example |
|------|-------------|------------|
| Quality gate | "Functional test pass rate ≥ 95%" | "Works properly" |
| Performance | "Page load < 2s at target load" | "Fast enough" |
| Compliance | "Pentest pass with zero critical findings" | "Secure" |
| Sign-off | "UAT signed off by PO and SME" | "Approved" |
| Coverage | "100% endpoint coverage in API docs" | "Documented" |
| Verification | "Zero cross-tenant data leakage confirmed" | "Isolated" |

**Rules:**
- Every deliverable needs at least one acceptance criterion
- Criteria must be verifiable (yes/no determination possible)
- Owner = the role PRODUCING it (not the role approving it)
- 10-25 deliverables is typical range

---

### Step 5: Produce Work Breakdown Structure (WBS)

The WBS decomposes the project into manageable work packages.

#### Structure Format (Text-Based Tree)

```markdown
## Work Breakdown Structure

```
{Project Name} ({Project ID})
│
├── 1.0 {TOP-LEVEL CATEGORY}
│   ├── 1.1 {Work Package}
│   ├── 1.2 {Work Package}
│   │   ├── 1.2.1 {Task} (Comprehensive only)
│   │   └── 1.2.2 {Task}
│   └── 1.3 {Work Package}
│
├── 2.0 {TOP-LEVEL CATEGORY}
│   ├── 2.1 {Work Package}
│   ├── 2.2 {Work Package}
│   └── 2.3 {Work Package}
│
├── 3.0 {TOP-LEVEL CATEGORY}
│   ├── ...
│
└── N.0 {FINAL CATEGORY}
    └── ...
```
```

#### WBS Decomposition Rules

| Rule | Description |
|------|-------------|
| **100% rule** | The WBS must capture 100% of project scope — nothing in-scope should be absent |
| **Mutual exclusivity** | No overlap between work packages at the same level |
| **Deliverable-oriented** | Decompose by WHAT is produced, not by WHO does it or HOW |
| **Manageable size** | Lowest-level packages should be estimable (days-weeks, not months) |
| **8/80 rule** | Work packages should be 8-80 hours of effort (guideline, not absolute) |
| **No orphans** | Every work package rolls up to a parent category |

#### Standard Top-Level Categories

Adapt based on project type, but typical structure:

| Category | Contains |
|----------|----------|
| **1.0 Project Management** | Initiation, planning, execution oversight, reporting, closure |
| **2.0 Design / Architecture** | Technical design, UX design, architecture documentation |
| **3.0 Build / Development** | Core construction — often split into phases or components |
| **4.0 Integration** | External system connections, data flows, API contracts |
| **5.0 Testing & QA** | Test strategy, execution, defect management |
| **6.0 Deployment & Infrastructure** | Environments, CI/CD, release management |
| **7.0 Change Management & Training** | Communications, training, adoption support |
| **8.0 Project Closure** | Handover, documentation, lessons learned, benefits review |

**Ask user if unsure about decomposition:**

```markdown
### Q-PLN-02: WBS Organization

**Context:** The WBS can be organized by project phase, by deliverable/component, or by a hybrid approach. The right choice depends on your delivery model.

**Options:**
- (a) **By phase** — Design → Build Phase 1 → Build Phase 2 → Test → Deploy (sequential focus)
- (b) **By component** — Platform Core → Module A → Module B → Integration (component focus)
- (c) **By discipline** — Management → Design → Development → Testing → Deployment (role focus)
- (d) **Hybrid** — Management + phases containing components (most common)

**Recommended:** Option (d)
**Rationale:** Hybrid provides both phase-gated visibility for governance and component-level tracking for delivery teams.

**Your Decision:** _[awaiting input]_
```

---

### Step 6: Define Milestone Schedule

```markdown
## High-Level Milestone Schedule

| # | Milestone | Target Date | Predecessor | Gate Decision |
|---|-----------|:-----------:|:-----------:|---------------|
| M1 | {Milestone name} | {Date or relative} | {What must complete first} | {Who decides / what criteria} |
| M2 | {Name} | {Date} | M1 | {Gate} |
```

**Milestone selection criteria:**
- Marks completion of a significant phase or deliverable
- Requires a decision or approval to proceed
- Represents a point where value is demonstrable
- Is meaningful to stakeholders (not just the delivery team)

**Rules:**
- First milestone: Project Kickoff (already happened or imminent)
- Last milestone: Post-Implementation Review / Benefits Review
- Include gates explicitly (Design Gate, Security Gate, Go-Live Decision)
- Use relative dates ("Week 10-12") if no baseline date exists
- Add predecessor column for dependency clarity

---

### Step 7: Define Delivery Phases (if applicable)

If the project is phased (common for medium/large projects):

```markdown
## Delivery Phases

| Phase | Duration (est.) | Content | Exit Criteria |
|-------|:--------------:|---------|---------------|
| {Phase name} | {n weeks} | {What's built/delivered} | {What must be true to exit this phase} |
```

**Rules:**
- Phases should deliver incrementally (each phase produces demonstrable value)
- Exit criteria should be verifiable (test pass, demo acceptance, sign-off)
- Later phases can depend on earlier ones — note dependencies

---

### Step 8: Define Project-Level Acceptance Criteria

```markdown
## Acceptance Criteria (Project Level)

The project will be accepted as complete when:

1. {Criterion 1 — e.g., All deliverables listed in Section X delivered and accepted}
2. {Criterion 2 — e.g., Performance targets met under load test}
3. {Criterion 3 — e.g., Security review passed}
4. {Criterion 4 — e.g., UAT signed off by PO}
5. {Criterion 5 — e.g., Steering Committee approves Go-Live}
```

**Rules:**
- 5-10 criteria typical
- Each must be binary (pass/fail — no partial credit)
- Must cover: functional completion, quality, security, user acceptance, governance approval
- Must align with Charter objectives (every objective should be checkable via these criteria)

---

### Step 9: Define Scope Change Control

```markdown
## Scope Change Control

All scope changes must follow the formal change control process:

1. **Raise:** Change Request documented in `management_framework/Change_Log.md`
2. **Assess:** PM and Technical Lead evaluate impact (scope, schedule, budget, quality, risk)
3. **Approve:** Authority per governance matrix in Project Charter
4. **Implement:** Baseline updated only after formal approval
5. **Communicate:** All stakeholders notified of approved changes

**Baseline documents:** This Scope Statement and the source requirements document together form the scope baseline. Any deviation requires a Change Request.
```

---

### Step 10: Assemble and Validate

1. Compile all sections using template `templates/scope-statement.md`
2. Validate:
   - [ ] Every in-scope item from Charter appears in the WBS (100% rule)
   - [ ] Every deliverable maps to one or more WBS work packages
   - [ ] Milestones are consistent with Business Case and Charter timelines
   - [ ] Acceptance criteria cover all Charter objectives
   - [ ] Out-of-scope items don't appear anywhere in the WBS
   - [ ] No WBS work package lacks a parent or sits orphaned
3. Add metadata: version, date, status, references

---

### Step 11: Present for Review

```markdown
## Review: Scope Statement — {project_name}

I've produced the Scope Statement with WBS. Key highlights:

- **Scope items:** {n} in-scope; {m} explicitly excluded
- **Deliverables:** {n} with acceptance criteria
- **WBS:** {levels} levels; {n} top-level categories; {m} total work packages
- **Milestones:** {n} over {timeline}
- **Phases:** {n} delivery phases (if applicable)
- **Acceptance criteria:** {n} project-level criteria

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Scope is well-defined; proceed to Resource & Budget Planning
- (b) **Adjust boundaries** — In/out scope needs revision
- (c) **Refine WBS** — Need more/less decomposition in specific areas
- (d) **Revise milestones** — Timeline or phasing needs adjustment
- (e) **Add deliverables** — Missing deliverables to include
```

---

### Step 12: Log and Transition

1. **Decision Log:** D-{nnn}: "Scope Statement approved. {n} in-scope items. WBS: {levels} levels, {packages} packages. {milestones} milestones."
2. **State File:** Stage 11 = ✅ Done; Current Stage = 12
3. **Assumptions Register:** Any scope assumptions (e.g., "ASM-{nnn}: Historical data migration is a separate project")

Display:

```
✅ Stage 11: Scope Definition — Complete

📐 Scope: {n} items | WBS: {levels}L / {packages} packages | Milestones: {n}
📄 Saved to: {file_path}

Next → Stage 12: Resource & Budget Planning
```

---

## Output File

Save to:
- Numbered: `{output_root}/06_Scope_Planning/Scope_Statement.md`
- Flat: `{output_root}/pilc-docs/planning/Scope_Statement.md`

---

## WBS Quality Checks

| Check | Pass Criteria |
|-------|---------------|
| 100% coverage | Every in-scope item traceable to at least one work package |
| No scope leak | No work package covers out-of-scope items |
| Correct granularity | Lowest level is estimable (8-80 hours guideline) |
| Clean hierarchy | No orphans; no overlaps; clear parent-child relationships |
| Deliverable-oriented | Named by WHAT is produced, not by activity or role |
| Consistent naming | Same naming convention throughout (noun phrases preferred) |
| Manageable breadth | No more than 7±2 items at any single level (cognitive limit) |
