<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Project Charter

## Stage: 9 of 16
## Phase: 🟣 AUTHORIZATION
## Execution: ALWAYS

---

## Purpose

Produce the formal document that authorizes the project to exist. The Charter establishes objectives, scope boundaries, governance authority, and the decision-making framework. Once signed, it becomes the project's constitutional document — all subsequent work references it.

---

## Depth Adaptation

| Depth | Charter Behavior |
|-------|-----------------|
| **Minimal** | Compact charter (3-5 pages): objectives, scope summary, key stakeholders, approach, approval. Suitable for small internal initiatives. |
| **Standard** | Full charter (8-12 pages): all sections below populated with appropriate detail. Suitable for most projects. |
| **Comprehensive** | Detailed charter (12-18 pages): expanded governance, authority matrix, detailed milestone schedule, extensive risk section, multiple approval tiers. Suitable for large, high-investment, multi-stakeholder programmes. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Business Case (Stage 8) — recommended approach, costs, benefits, timeline
2. Feasibility Assessment (Stage 6) — conditions, rating
3. Prioritization (Stage 7) — strategic alignment, priority rank
4. Requirement Intake Form (Stage 3) — stakeholders, constraints, estimates
5. Clarification outcomes (Stage 5) — resolved decisions
6. Decision Log — all decisions made to date
7. Assumptions & Dependencies register

---

### Step 2: Confirm Project Identity

The **Project ID** was minted at Stage 1 (Workspace Detection) and stored in `pilc-state.md`. The Charter **confirms** it — it does NOT regenerate or reformat it (the ID is immutable; it is the family-wide correlation key). Read the remaining identity fields from prior stages or confirm with the user:

| Field | Source | Action |
|-------|--------|--------|
| Project Name | Stage 1 (already set) | Confirm with user |
| Project ID | Stage 1 (`pilc-state.md`) | **Read from state — do NOT regenerate.** Format: `PRJ-{ABBREV}-{YEAR}-{NNN}` |
| Project Manager | Source/stakeholders | Use if known; `_[TBD]_` if not |
| Project Sponsor | Source/stakeholders | Must be identified (ask if unknown) |
| Product Owner | Source/stakeholders | Use if known; may be same as requestor |
| Start Date | Business Case timeline | "Upon Charter approval" if no specific date |
| Target End Date | Business Case timeline | Relative or absolute |
| Priority | Stage 7 output | {MoSCoW} — {Pn} |

> **Identity reconciliation:** The "Request ID" generated during Stage 3 (Requirement Structuring) and the `Project ID` are the **same identity thread** — the Request ID is the intake-time handle that resolves to this Project ID once the project is authorized. Ensure all artifacts reference the single `Project ID`; do not introduce a competing identifier.

**If Sponsor is unknown:**

```markdown
### Q-AUT-01: Project Sponsor

**Context:** The Charter requires an identified sponsor — the executive with budget authority and ultimate accountability for the project's success.

**Your input:** Who is the executive sponsor for this initiative?

**Format expected:** Name and title/role

**If unknown:** Provide the role/level expected (e.g., "CIO", "VP Engineering", "Director of Operations") and I'll use the role as placeholder.
```

---

### Step 3: Define Objectives

Transform business case benefits and requirements into measurable project objectives:

**Objective format:**

| # | Objective | Success Criteria | Measurement |
|---|-----------|-----------------|-------------|
| 1 | {What will be achieved} | {How we know it's done — specific, measurable} | {How it will be measured/verified} |

**Rules for objectives:**
- 5-8 objectives is ideal (3 minimum, 10 maximum)
- Each must be SMART: Specific, Measurable, Achievable, Relevant, Time-bound
- Derived from requirements and business case benefits — not invented
- Include both delivery objectives (build the thing) and outcome objectives (the thing delivers value)
- Each must have a verifiable success criterion

**Common objective categories:**
- Capability delivery (features/functions built and operational)
- Performance targets (NFR targets met under load)
- Quality gates (test pass rates, security compliance)
- Scale targets (capacity/volume goals)
- User adoption (training complete, users active)
- Compliance (standards met, audit passed)
- Integration (systems connected, data flowing)

---

### Step 4: Define High-Level Scope

#### In Scope

Derived from Requirement Intake Form and Scope decisions made during clarification:

```markdown
### In Scope (v1)
1. {Capability/deliverable — brief description}
2. {Capability/deliverable}
...
```

**Rules:**
- Numbered list, not paragraphs
- Each item is a distinct, recognizable capability or deliverable
- Level of detail: enough that a stakeholder can confirm "yes, that's what I expect"
- Include both functional and supporting items (infrastructure, security, training)

#### Out of Scope

Derived from source document exclusions and deferral decisions:

```markdown
### Out of Scope (Deferred / Excluded)
1. {Item} — {Reason for exclusion: deferred to v2 / separate project / not required}
2. {Item} — {Reason}
...
```

**Rules:**
- Be explicit about WHY each item is excluded
- This section prevents scope creep — it's a defensive boundary
- Include items that stakeholders might ASSUME are included but aren't

---

### Step 5: Define Key Deliverables

```markdown
## Key Deliverables

| # | Deliverable | Target Phase | Owner |
|---|-------------|:------------:|-------|
| 1 | {Deliverable name} | {When} | {Role} |
| 2 | {Deliverable name} | {When} | {Role} |
```

**Rules:**
- 10-20 deliverables is typical
- Each should be a tangible, reviewable artifact or system component
- Owner = the role accountable for producing it (not the person approving)
- Target phase = when it's expected (Design, Build Ph1, Testing, etc.)

---

### Step 6: Define Milestones

```markdown
## High-Level Milestones

| Milestone | Target Date | Gate/Decision |
|-----------|:-----------:|---------------|
| M1: {name} | {date or relative} | {What decision/approval happens here} |
| M2: {name} | {date} | {Gate} |
```

**Rules:**
- 8-12 milestones for standard projects; 5-8 for minimal; up to 15 for comprehensive
- Each milestone should have a clear gate decision (who approves, what criteria)
- Use relative dates ("Week 10-12", "+3 months") if absolute dates aren't set
- First milestone should be "Project Kickoff"
- Last milestone should be "Post-Implementation Review"
- Include key decision points, not just delivery points

---

### Step 7: Document Assumptions and Constraints

#### Assumptions

Drawn from the Assumptions register, filtered to those relevant to the Charter level:

```markdown
## Assumptions
1. {Assumption — what we believe to be true but haven't verified}
2. {Assumption}
```

**Rules:**
- 5-10 Charter-level assumptions
- Each should be something that, if wrong, would materially impact the project
- Operational assumptions (e.g., "team available within 4 weeks") not just technical

#### Constraints

```markdown
## Constraints
1. **{Constraint type}:** {What is constrained — the hard limit}
2. **{Constraint type}:** {Constraint}
```

**Rules:**
- Constraints are NON-NEGOTIABLE boundaries (unlike assumptions which are beliefs)
- Common types: Technology, Regulatory, Budget, Timeline, Resource, Security
- Each must be specific enough to be verifiable ("on-premises only" not "should prefer on-prem")

---

### Step 8: Identify Key Risks (Charter Level)

Select top 5-7 risks from analysis so far:

```markdown
## Key Risks (Initial)

| Risk | Impact | Probability | Response |
|------|:------:|:-----------:|----------|
| {Risk description} | {H/M/L} | {H/M/L} | {Brief response strategy} |
```

**Rules:**
- These are the HEADLINE risks for executive awareness
- Full risk register produced in Stage 13
- Focus on risks that could derail the project entirely or require executive intervention
- Include at least one from each category: Technical, Resource, Scope, Schedule

---

### Step 9: Define Project Approach

```markdown
## Project Approach

| Aspect | Approach |
|--------|----------|
| **Methodology** | {Agile / Waterfall / Hybrid / Other — brief description} |
| **Delivery Model** | {Iterative sprints / Phase-gated / Continuous / etc.} |
| **Design Approach** | {Design-first / Emergent / Prototype-driven / etc.} |
| **Testing** | {Continuous / Phase-end / Both} |
| **Deployment** | {Continuous / Staged / Big-bang} |
| **Change Control** | {Formal CR process / Backlog management / Both} |
| **Reporting** | {Cadence and audience summary} |
```

**If methodology is unknown, ask:**

```markdown
### Q-AUT-02: Project Methodology

**Context:** The Charter should state how the project will be run. This affects planning, reporting, and team expectations.

**Options:**
- (a) **Agile** — Iterative delivery in sprints; backlog-driven; continuous feedback
- (b) **Waterfall** — Sequential phases; formal stage-gates; comprehensive upfront planning
- (c) **Hybrid** — Agile delivery within a waterfall governance framework (sprints + phase gates)
- (d) **Not decided yet** — Leave as TBD; decide during Planning phase

**Recommended:** {Based on project complexity, team context, and organizational norms}
**Rationale:** {Why}

**Your Decision:** _[awaiting input]_
```

---

### Step 10: Define Governance & Authority

```markdown
## Authority & Governance

| Decision Type | Authority | Escalation Path |
|---------------|-----------|-----------------|
| Day-to-day tactical | Project Manager | → Sponsor if blocked > {n} hours |
| Scope changes (minor) | PM + Product Owner | → Steering Committee if disputed |
| Scope changes (major) | Steering Committee | — |
| Budget variance < {n}% | PM + Sponsor | → Finance if > threshold |
| Budget variance > {n}% | Steering Committee + Finance | — |
| Schedule variance < {n} weeks | Project Manager | → Sponsor |
| Schedule variance > {n} weeks | Steering Committee | — |
| Technical decisions | Technical Lead | → Steering Committee if strategic |
| Security/compliance exceptions | Security Lead | → Sponsor if risk accepted |
| Go-Live decision | Steering Committee | — |
```

**Steering Committee composition** (ask user if unclear):

```markdown
### Steering Committee
- {Role 1 — name if known} — Chair
- {Role 2}
- {Role 3}
- {Role 4}
- {Role 5}
```

**Rules:**
- Steering Committee should be 4-7 people maximum
- Must include Sponsor (usually Chair), PM, and at least one technical representative
- Decision thresholds (%, weeks) should match organizational norms — ask user if unsure

---

### Step 11: Add Approval Section

```markdown
## Charter Approval

By signing this charter, the signatories authorize the project to proceed, commit to providing necessary support and resources, and agree to the scope, approach, and governance defined herein.

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Project Sponsor | {name} | _[Pending]_ | |
| Product Owner / Requestor | {name} | _[Pending]_ | |
| {Key stakeholder role} | {name} | _[Pending]_ | |
| Project Manager | {name or TBD} | _[Pending]_ | |
| Technical Lead | {name or TBD} | _[Pending]_ | |
```

**Rules:**
- Minimum 3 signatories: Sponsor + Requestor/PO + one other
- PM and Tech Lead sign if already appointed
- Additional signatories based on organizational governance requirements

---

### Step 12: Assemble and Validate

1. Compile all sections using template `templates/project-charter.md`
2. Validate per `common/content-validation.md`:
   - Scope items match those in Business Case and Intake Form
   - Budget summary matches Business Case
   - Stakeholder names consistent across documents
   - Milestones consistent with Business Case timeline
   - No contradictions with prior deliverables
3. Add metadata: version, date, status ("Awaiting Sponsor Signature"), references

---

### Step 13: Present for Review

```markdown
## Review: Project Charter — {project_name}

I've produced the Project Charter. Key highlights:

- **Project ID:** {PRJ-XXX-YYYY-NNN}
- **Sponsor:** {name}
- **Objectives:** {n} measurable objectives defined
- **Scope:** {n} in-scope items; {m} explicitly excluded
- **Milestones:** {n} milestones over {timeline}
- **Methodology:** {approach}
- **Governance:** Steering Committee of {n}; authority matrix defined
- **Top risks:** {top 2-3 risk headlines}
- **Signatories:** {n} approval signatures required

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Charter is ready for signatures; proceed to Planning
- (b) **Request changes** — Specific sections need adjustment
- (c) **Expand governance** — Need more detail on authority/escalation
- (d) **Adjust scope** — Scope boundaries need revision
- (e) **Add signatories** — Additional approvers needed
```

---

### Step 14: Iterate and Finalize

If user requests changes:
1. Ask which sections to modify
2. Apply changes
3. Re-validate cross-references
4. Re-present summary
5. Repeat until approved

---

### Step 15: Log and Transition

1. **Decision Log:**
   - D-{nnn}: "Project Charter produced. ID: {PRJ-ID}. Methodology: {approach}. Signatories: {n}."
   - D-{nnn}: (if methodology decided here) "Methodology: {chosen}. Rationale: {reason}."
2. **State File:** Stage 9 = ✅ Done; Current Phase = PLANNING; Current Stage = 10
3. **Action Items:** A-{nnn}: "Obtain Charter signatures from {signatories}" — Owner: PM

Display transition:

```
✅ Stage 9: Project Charter — Complete

📜 Charter: {PRJ-ID} — Awaiting signatures
🎯 {n} objectives | 📐 {n} scope items | ⚙️ {methodology}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ AUTHORIZATION PHASE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next → PLANNING PHASE (Stages 10-14)
I'll now plan stakeholders, scope, resources, risks, and governance.

Note: Planning stages (10-14) can be done in any order.
Default sequence: Stakeholders → Scope → Resources → Risks → Governance

Proceed with default order? [Yes / Custom order / Skip to specific stage]
```

---

## Output File

Save to:
- Numbered: `{output_root}/04_Project_Charter/Project_Charter.md`
- Flat: `{output_root}/pilc-docs/authorization/Project_Charter.md`

---

## Charter Quality Checks

| Check | What to Verify |
|-------|---------------|
| Objectives are measurable | Each has a quantifiable success criterion |
| Scope matches source | Every in-scope item traceable to requirements |
| Out-of-scope is explicit | Common assumptions addressed (what people might expect that ISN'T included) |
| Governance is actionable | Thresholds are specific numbers, not vague |
| Risks are charter-level | Not every risk — just the strategic/existential ones |
| Approval is achievable | Named signatories can actually sign (they exist and are available) |
| Timeline is consistent | Milestones match Business Case and don't contradict feasibility |
| Budget is consistent | Figures match Business Case ROM |
