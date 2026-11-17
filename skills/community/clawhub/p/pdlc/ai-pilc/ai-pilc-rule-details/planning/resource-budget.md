<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Resource & Budget Planning

## Stage: 12 of 16
## Phase: 🟢 PLANNING
## Execution: ALWAYS

---

## Purpose

Determine what people, infrastructure, and budget the project needs — by role, by phase, and by cost category. Produce a Resource Plan with team structure, allocation timeline, sourcing strategy, and a ROM (Rough Order of Magnitude) budget estimate with phased breakdown.

---

## MANDATORY: Stage Sub-Role — Resource & Schedule Planner

During THIS stage, ALSO adopt the mindset of a **Resource & Schedule Planner**. This does NOT replace your primary role (PMO Professional / Senior Project Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Decompose before estimating — never estimate a large undifferentiated blob
- Express every estimate as a confidence range tied to a stated technique (analogous, parametric, etc.), not a single point
- Match skills to work (capability), not just headcount
- Plan for <100% productive capacity (meetings, ramp-up, context-switching) and phase the resource curve

### Anti-Patterns for This Stage
- Do NOT assume 100% utilization — plan 70-80% productive capacity
- Do NOT present the budget as a single figure without variance and a basis of estimate

### Quality Check
A good output at this stage sounds like:
- "Team: 2 senior backend, 1 mid frontend, 0.5 DevOps; ROM budget $480K (±30%); basis: analogous to Project X +20% for tech unfamiliarity..."

---

## Depth Adaptation

| Depth | Resource Detail | Budget Detail |
|-------|----------------|---------------|
| **Minimal** | Role list with headcount and allocation %. Single total ROM range. | Single cost table with broad categories. ±50% accuracy. |
| **Standard** | Full role table with phase allocation, sourcing strategy, and team ramp plan. | Categorized cost table by year/phase. ±30% accuracy. Contingency calculated. |
| **Comprehensive** | Detailed role profiles, individual rate ranges, resource loading heatmap, sourcing risk analysis, make-vs-buy decisions. | Detailed cost model by category, phase, and year. Sensitivity analysis. ±15-20% accuracy where data supports. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Scope Statement (Stage 11) — WBS, phases, milestones, deliverables
2. Project Charter (Stage 9) — timeline, methodology, constraints
3. Feasibility Assessment (Stage 6) — skills/infrastructure scores
4. Business Case (Stage 8) — any ROM figures already stated
5. Stakeholder Register (Stage 10) — known named resources
6. Source requirements — team size indicators, infrastructure needs

---

### Step 2: Identify Required Roles

Based on the WBS and delivery approach, identify all roles needed:

#### Core Project Team (Governance & Management)

| # | Role | Responsibility Summary | Full-Time/Part-Time | Phase Active |
|---|------|----------------------|:-------------------:|:------------:|
| 1 | Project Sponsor | Strategic direction, budget authority, escalation | Part-time (5-10%) | All |
| 2 | Product Owner | Requirements ownership, acceptance, priority | Part-time (50-75%) | All |
| 3 | Project Manager | Planning, delivery oversight, reporting, risk | Full-time (100%) | All |

#### Delivery Team (Technical & Specialist)

Derive from WBS work packages — each significant work area needs an owner:

```markdown
### Delivery Team

| # | Role | Headcount | Allocation | Start Phase | End Phase | Key Responsibilities |
|---|------|:---------:|:----------:|:-----------:|:---------:|---------------------|
| {n} | {Role title} | {1-n} | {50-100%} | {Phase} | {Phase} | {What they do on this project} |
```

**Role identification heuristics:**

| WBS Area | Likely Roles |
|----------|-------------|
| Design / Architecture | Technical Lead, Architect, UX Designer |
| Backend development | Senior Developers, Database Engineer |
| Frontend development | Frontend Developers, UI Developer |
| Integration | Integration Specialist, Full-Stack Developer |
| Infrastructure | DevOps Engineer, Infrastructure Lead |
| Testing | QA Lead, QA Engineers, Performance Tester |
| Security | Security Lead (often part-time from existing team) |
| Change management | Change Manager, Training Developer |
| Operations | Support Lead (for transition/hypercare) |

**Ask user for context if needed:**

```markdown
### Q-PLN-03: Team Composition

**Context:** Based on the WBS and project complexity, I'm estimating the team structure. I need to confirm a few points:

1. **Internal vs. external:** Will the team be fully internal, or will contractors/vendors be involved?
2. **Existing team:** Are any team members already identified/available, or is this a full recruitment exercise?
3. **Rate information:** Do you have day/month rate ranges for budgeting, or should I use market-standard placeholders?

**Your input:** _[Any guidance on team composition, sourcing, or rates]_
```

---

### Step 3: Produce Resource Loading by Phase

Map roles to project phases showing allocation:

```markdown
## Resource Loading by Phase

| Role | {Phase 1} | {Phase 2} | {Phase 3} | {Phase 4} | {Phase 5} | Total Months |
|------|:---------:|:---------:|:---------:|:---------:|:---------:|:------------:|
| Project Manager | 100% | 100% | 100% | 100% | 100% | {n} |
| Technical Lead | 100% | 100% | 100% | 75% | 50% | {n} |
| {Role} × {headcount} | {%} | {%} | {%} | {%} | {%} | {n} |
```

#### Team Summary by Phase

```markdown
### Team Size Summary

| Phase | Duration (est.) | Min FTE | Max FTE | Notes |
|-------|:--------------:|:-------:|:-------:|-------|
| {Phase 1} | {n weeks} | {n} | {n} | {Ramp-up, key activities} |
| {Phase 2} | {n weeks} | {n} | {n} | {Peak resourcing} |
| {Phase 3} | {n weeks} | {n} | {n} | {Wind-down} |
| **Average** | | **{n}** | **{n}** | |
```

---

### Step 4: Define Sourcing Strategy

```markdown
## Sourcing Strategy

| Approach | Roles | Rationale |
|----------|-------|-----------|
| **Internal (existing staff)** | {Roles that can be filled from current headcount} | {Why — availability, cost, knowledge retention} |
| **Internal (new hire)** | {Roles requiring recruitment} | {Why — long-term need, core capability} |
| **Contractor** | {Roles suitable for contract engagement} | {Why — temporary need, specialist skill, speed} |
| **Vendor/Partner** | {Roles or work packages outsourced} | {Why — capability gap, fixed-price, risk transfer} |

### Sourcing Risks

| Risk | Impact | Mitigation |
|------|:------:|-----------|
| {Recruitment takes longer than expected} | {Schedule delay} | {Start early; contractor bridge} |
| {Contractor rates higher than budgeted} | {Budget overrun} | {Rate cap in contracts; prioritize internal} |
| {Key skill unavailable in market} | {Capability gap} | {Train existing; adjust scope; alternative approach} |
```

---

### Step 5: Estimate Budget

#### Cost Category Structure

```markdown
## Budget Estimate (ROM)

### Estimation Confidence: {±50% / ±30% / ±15%}
### Estimation Basis: {Top-down analogy / Bottom-up from WBS / Parametric / Expert judgment}

| Cost Category | {Period 1} | {Period 2} | {Period 3} | Total |
|---------------|:----------:|:----------:|:----------:|:-----:|
| **People — Internal** | {$X} | {$X} | {$X} | {$X} |
| **People — Contractors** | {$X} | {$X} | {$X} | {$X} |
| **People — Vendor/Partner** | {$X} | {$X} | {$X} | {$X} |
| **Infrastructure (HW/Cloud)** | {$X} | {$X} | {$X} | {$X} |
| **Software / Tooling / Licenses** | {$X} | {$X} | {$X} | {$X} |
| **Training & Change Management** | {$X} | {$X} | — | {$X} |
| **Security (Audits, Pentests)** | {$X} | — | {$X} | {$X} |
| **Travel / Facilities** | {$X} | {$X} | {$X} | {$X} |
| **Ongoing Maintenance (post go-live)** | — | {$X} | {$X} | {$X} |
| **Contingency ({n}%)** | {$X} | {$X} | {$X} | {$X} |
| **Total** | **{$X}** | **{$X}** | **{$X}** | **{$X}** |
```

#### Budget Estimation Methods

| Method | When to Use | Accuracy |
|--------|-------------|:--------:|
| **Top-down (analogy)** | Similar past projects exist; early-stage estimate | ±50% |
| **Parametric** | Cost drivers known (e.g., $/FTE/month × team × duration) | ±30% |
| **Bottom-up** | WBS fully decomposed; effort per package estimated | ±15% |
| **Vendor quotes** | External work packages with proposals received | ±10% |

**Rules:**
- State which method was used
- If using rates, state the rate assumption (e.g., "Senior Developer: $X/month")
- If rates are unknown, use placeholders: `_[TBD — rate to be confirmed]_` and calculate based on team structure only
- Always include contingency:
  - ±50% estimate → 25% contingency
  - ±30% estimate → 20% contingency
  - ±15% estimate → 15% contingency

---

### Step 6: CapEx vs. OpEx Split (if relevant)

```markdown
### Capital vs. Operational Classification

| Category | CapEx | OpEx | Notes |
|----------|:-----:|:----:|-------|
| Development team (build phase) | ✅ | | Capitalizable if creating new asset |
| Infrastructure (servers/hardware) | ✅ | | Capital asset |
| Software licenses (perpetual) | ✅ | | Capital if multi-year |
| Software licenses (subscription) | | ✅ | Operational expense |
| Maintenance & support (post go-live) | | ✅ | Operational |
| Training | | ✅ | Typically operational |
| Contractors (build phase) | ✅ | | Capitalizable with internal team |
| Project management | Mixed | Mixed | Often split by phase |
```

**Note:** Only include this section if the user indicates CapEx/OpEx classification matters for their organization. Ask if unclear.

---

### Step 7: Identify Budget Assumptions

```markdown
### Budget Assumptions

| # | Assumption | Impact if Wrong | Confidence |
|---|-----------|-----------------|:----------:|
| 1 | {Rate assumption — e.g., "Developer monthly rate: $X"} | {Budget variance: +$Y} | {H/M/L} |
| 2 | {Duration assumption} | {Impact} | {H/M/L} |
| 3 | {Infrastructure assumption} | {Impact} | {H/M/L} |
| 4 | {Scope assumption — no scope creep} | {Impact} | {H/M/L} |
```

Log all assumptions to the Assumptions & Dependencies register.

---

### Step 8: Produce Funding Request (if applicable)

```markdown
### Funding Summary

| Field | Value |
|-------|-------|
| Total Investment Required | {$X — range: $Low to $High} |
| Funding Period | {Year 1 to Year N} |
| Estimation Confidence | {±X%} |
| Contingency Included | {$X ({n}%)} |
| Recommended Funding Model | {Lump sum / Phased release / Phase 1 then gate / Annual budget} |
| Approval Required From | {Finance / Sponsor / Board — per governance matrix} |
```

---

### Step 9: Assemble Document

Using template `templates/resource-plan.md`, compile:

1. Section 1: Resource Requirements (core team + delivery team tables)
2. Section 2: Resource Loading by Phase (allocation matrix + summary)
3. Section 3: Sourcing Strategy (approach + risks)
4. Section 4: Budget Estimate (categorized cost table)
5. Section 5: Budget Assumptions
6. Section 6: Funding Summary
7. Section 7: CapEx/OpEx (if applicable)

Validate per `common/content-validation.md`:
- Team size consistent with Business Case estimates
- Timeline aligns with Scope Statement milestones
- Budget categories are complete (no major category missing)
- Contingency calculated correctly

---

### Step 10: Present for Review

```markdown
## Review: Resource & Budget Plan — {project_name}

I've produced the Resource & Budget Plan. Key highlights:

- **Team size:** {min}-{max} FTE across phases (avg: {n})
- **Key roles:** {Top 3-4 roles and headcounts}
- **Sourcing:** {Primary approach — internal/mixed/contractor-heavy}
- **Total investment (ROM):** {$Low — $High} (±{n}%)
- **Contingency:** {$X} ({n}%)
- **Duration covered:** {n months/years}
- **Biggest cost driver:** {Category accounting for largest share}

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Resource and budget plan is sufficient; proceed
- (b) **Adjust team** — Headcount or roles need revision
- (c) **Refine costs** — I have rate data or cost information to add
- (d) **Challenge estimates** — Numbers seem too high/low; discuss
- (e) **Add detail** — Need more granularity in specific areas
```

---

### Step 11: Log and Transition

1. **Decision Log:** D-{nnn}: "Resource & Budget Plan approved. Team: {min}-{max} FTE. ROM: {$range}. Contingency: {n}%."
2. **State File:** Stage 12 = ✅ Done; Current Stage = 13
3. **Assumptions Register:** All budget assumptions logged
4. **Action Items:** A-{nnn}: "Obtain budget approval from {Finance/Sponsor}" if not yet secured

Display:

```
✅ Stage 12: Resource & Budget Planning — Complete

👥 Team: {min}-{max} FTE | 💰 ROM: {$range}
📄 Saved to: {file_path}

Next → Stage 13: Risk Management
```

---

## Output File

Save to:
- Numbered: `{output_root}/07_Resource_Budget/Resource_Plan.md`
- Flat: `{output_root}/pilc-docs/planning/Resource_Plan.md`

---

## Common Budget Pitfalls

| Pitfall | Prevention |
|---------|-----------|
| Forgetting ongoing costs | Always include Year 2+ operational/maintenance costs |
| No contingency | Never present a budget without contingency — it's not padding, it's risk management |
| Precision theater | Don't present "$3,247,891" when accuracy is ±30% — use ranges and round numbers |
| Missing categories | Check: people, infrastructure, licenses, training, security, travel, change management |
| Ignoring ramp-up | Team doesn't hit full productivity on day 1 — account for onboarding/ramp |
| Single-point estimate | Always provide a range (low-likely-high) rather than a single number |
| Forgetting inflation | Multi-year budgets should account for rate increases |
