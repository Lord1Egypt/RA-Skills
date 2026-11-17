<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Business Case Development

## Stage: 8 of 16
## Phase: 🟡 JUSTIFICATION
## Execution: ALWAYS

---

## Purpose

Build the formal investment case that justifies committing organizational resources to this initiative. The business case synthesizes all prior analysis (requirements, feasibility, priority) into a decision-ready document for sponsor/executive approval.

---

## MANDATORY: Stage Sub-Role — Financial Analyst

During THIS stage, ALSO adopt the mindset of a **Financial Analyst**. This does NOT replace your primary role (PMO Professional / Senior Project Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Quantify benefits in measurable financial terms wherever data supports; qualify honestly where it doesn't (no fabricated precision)
- Always include the "do nothing" baseline as the comparator — every case is "this vs. status quo"
- Separate one-time (CapEx) from recurring (OpEx) costs; present confidence ranges, never single-point figures
- Challenge every claimed saving with a "how is this measured?" test before it enters the case

### Anti-Patterns for This Stage
- Do NOT present a single cost number without stating assumptions and a variance range
- Do NOT compute NPV/IRR when the underlying inputs don't exist — say so and use simpler measures

### Quality Check
A good output at this stage sounds like:
- "Option A 3-year TCO $X (±20%) vs. do-nothing baseline; payback ~14 months (realistic); sensitivity: +6 months if adoption is 30% slower..."

---

## Depth Adaptation

| Depth | Business Case Behavior |
|-------|----------------------|
| **Minimal** | Executive summary + problem + single recommended solution + high-level benefits + ROM costs + recommendation. 3-5 pages. |
| **Standard** | Full business case with options analysis (2-3 options), quantified benefits, cost table, risk summary, timeline, approval section. 8-12 pages. |
| **Comprehensive** | Detailed business case with 3-4 options, financial model (NPV/ROI/IRR if data available), sensitivity analysis, detailed risk section, implementation roadmap, governance implications. 12-20 pages. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Requirement Intake Form (Stage 3) — business need, stakeholders, constraints
2. Requirements Analysis findings (Stage 4) — any unresolved complexities
3. Clarification outcomes (Stage 5) — resolved decisions affecting scope
4. Feasibility Assessment (Stage 6) — scores, conditions, overall rating
5. Prioritization results (Stage 7) — strategic alignment, MoSCoW, value/effort
6. Decision Log — all decisions made so far
7. Assumptions & Dependencies register — active assumptions

---

### Step 2: Determine Options Approach

Ask the user (if not already clear from source/context):

```markdown
### Q-JUS-01: Solution Options

**Context:** A business case typically evaluates alternatives before recommending one. How should we approach options analysis?

**Options:**
- (a) **Single approach** — The solution is already decided; business case justifies the chosen approach vs. "do nothing"
- (b) **Options comparison** — Present 2-3 viable alternatives with pros/cons/cost comparison
- (c) **Full options analysis** — Present 3-4 options including do-nothing, with detailed financial and risk comparison per option

**Recommended:** {Based on context — if source document already specifies approach, recommend (a); if genuinely open, recommend (b)}
**Rationale:** {Why}

**Your Decision:** _[awaiting input]_
```

---

### Step 3: Draft Problem Statement

Synthesize from the Requirement Intake Form (Section 3: Business Need):

**Structure:**
```markdown
## Problem Statement

### Current State
- {Bullet 1 — what exists today and why it's inadequate}
- {Bullet 2 — pain point}
- {Bullet 3 — operational impact}
- {Bullet 4 — specific metrics if available}

### Consequences of Inaction
- {What happens if we do nothing — business impact}
- {Financial consequence}
- {Competitive/strategic consequence}
- {Operational/user consequence}
- {Risk/compliance consequence}
```

**Rules:**
- Draw ONLY from source document and confirmed information
- Be specific — avoid generic "efficiency" claims without context
- Quantify where data is available; acknowledge where data is estimated
- Frame as business problem, not technical problem

---

### Step 4: Develop Solution Options

Based on Q-JUS-01 response:

#### If Single Approach (option a):

```markdown
## Proposed Solution

{Description of the recommended approach — 2-3 paragraphs covering what, how, and why this approach}

### Why This Approach
- {Key differentiator 1}
- {Key differentiator 2}
- {Why alternatives were not chosen — brief}

### Alternative Considered: Do Nothing
{Brief statement of why doing nothing is unacceptable — reference Consequences of Inaction}
```

#### If Options Comparison (option b or c):

```markdown
## Solution Options Considered

| Option | Description | Pros | Cons | Est. Cost (ROM) |
|--------|-------------|------|------|:---------------:|
| **A: {Name}** | {Brief description} | {Key advantages} | {Key disadvantages} | {Range} |
| **B: {Name}** | {Brief description} | {Key advantages} | {Key disadvantages} | {Range} |
| **C: {Name} (Recommended)** | {Brief description} | {Key advantages} | {Key disadvantages} | {Range} |
| **D: Do Nothing** | Maintain current state | No investment required | All current problems persist and worsen | {Ongoing cost / opportunity cost} |

### Recommended: Option {X} — {Name}

**Rationale:** {3-5 sentences explaining why this is the recommended option. Reference feasibility, strategic alignment, risk balance, and cost-benefit.}
```

**Option generation rules:**
- Options must be genuinely distinct (not trivial variations)
- Always include "Do Nothing" as a baseline comparator
- Each option must be feasible (don't include strawmen)
- Clearly mark the recommended option
- Provide enough detail for a decision-maker to evaluate without reading the full requirements

---

### Step 5: Articulate Benefits

#### Quantitative Benefits

```markdown
### Quantitative Benefits

| Benefit | Metric | Current State | Target State | Est. Annual Value |
|---------|--------|:-------------:|:------------:|:-----------------:|
| {Benefit 1} | {How measured} | {Current performance} | {Expected with solution} | {$ or % — even if ROM} |
| {Benefit 2} | {Metric} | {Current} | {Target} | {Value} |
```

**Rules:**
- Only include benefits that can be measured (even if estimate)
- State the basis for any value claims: "Based on {assumption/benchmark/source data}"
- If precise values aren't available, use ranges or state `_[To be quantified]_`
- Don't inflate — conservative estimates build credibility

#### Qualitative Benefits

```markdown
### Qualitative Benefits

1. **{Benefit title}** — {1-2 sentences explaining the benefit and why it matters}
2. **{Benefit title}** — {Description}
3. **{Benefit title}** — {Description}
```

**Rules:**
- 4-8 qualitative benefits is typical
- Order by importance to the organization
- Each should be distinct (not restatements of the same point)
- Connect each to a stakeholder group who cares about it

---

### Step 6: Estimate Costs

```markdown
## Cost Estimate

| Cost Category | Year 1 | Year 2 | Year 3 | Total |
|---------------|:------:|:------:|:------:|:-----:|
| {Category 1 — e.g., People/Team} | {$X or TBD} | {$X} | {$X} | {$X} |
| {Category 2 — e.g., Infrastructure} | {$X} | {$X} | {$X} | {$X} |
| {Category 3 — e.g., Tooling/Licenses} | {$X} | {$X} | {$X} | {$X} |
| {Category 4 — e.g., Training} | {$X} | {$X} | — | {$X} |
| {Category 5 — e.g., External services} | {$X} | {$X} | {$X} | {$X} |
| Contingency ({n}%) | {$X} | {$X} | {$X} | {$X} |
| **Total** | **{$X}** | **{$X}** | **{$X}** | **{$X}** |
```

**Cost estimation approach by depth:**

| Depth | Estimation Method |
|-------|------------------|
| Minimal | Single ROM figure with ±50% range. State: "Detailed estimation in Resource Planning (Stage 12)" |
| Standard | Category-level breakdown with ±30% range. Key assumptions stated. |
| Comprehensive | Detailed breakdown with rates, headcount, duration. ±15% range where possible. |

**Rules:**
- Always state the estimation confidence level (ROM ±50%, Budget ±30%, Definitive ±10%)
- Always include contingency (15-25% depending on uncertainty)
- If costs can't be estimated yet, say so explicitly and note: "To be refined in Stage 12 (Resource & Budget Planning)"
- Never invent financial figures — if source provides no data, use `_[TBD — pending Stage 12]_`

---

### Step 7: Financial Analysis (Standard/Comprehensive depth)

```markdown
## Financial Analysis

| Metric | Value |
|--------|-------|
| Total Investment ({n} years) | {$X or TBD} |
| Total Benefits ({n} years) | {$X or TBD} |
| Net Present Value (NPV) | {$X or TBD} |
| Return on Investment (ROI) | {%X or TBD} |
| Payback Period | {n months/years or TBD} |
| Internal Rate of Return (IRR) | {%X or TBD} |
```

**Rules:**
- Only calculate metrics where data exists to support them
- If data is insufficient: state "Financial analysis will be completed once cost estimates are finalized" and list which inputs are needed
- For ROM-level business cases, qualitative + strategic justification is acceptable without full financial model
- State assumptions (discount rate, benefit growth rate, cost inflation)

**For Comprehensive depth additionally:**
- Sensitivity analysis: "What if costs are 20% higher? What if benefits are 30% lower?"
- Break-even analysis: "At what benefit level does the investment break even?"

---

### Step 8: Timeline & Milestones

```markdown
## Timeline & Key Milestones

| Milestone | Target Date | Dependency |
|-----------|:-----------:|-----------|
| Business Case Approval | {date or relative} | This document |
| Project Charter Sign-off | {+n weeks} | Business Case approved |
| Project Kickoff | {+n weeks} | Charter signed |
| {Key delivery milestone 1} | {+n months} | Kickoff |
| {Key delivery milestone 2} | {+n months} | Milestone 1 |
| Go-Live / Delivery | {+n months} | All milestones |
| Benefits Realization Review | {+n months post go-live} | Go-Live |
```

**Rules:**
- Use relative dates if absolute dates aren't known ("+ 3 months from kickoff")
- Include only high-level milestones (5-10 max for business case level)
- More detailed scheduling happens in Stage 11 (Scope Definition)

---

### Step 9: Risks & Dependencies Summary

```markdown
## Risks & Dependencies

### Key Risks
| Risk | Probability | Impact | Mitigation |
|------|:-----------:|:------:|-----------|
| {Risk 1} | {H/M/L} | {H/M/L} | {Brief mitigation} |
| {Risk 2} | {H/M/L} | {H/M/L} | {Brief mitigation} |

### Dependencies
| Dependency | Required By | Owner |
|-----------|:-----------:|:-----:|
| {Dependency 1} | {Milestone/phase} | {Role} |
| {Dependency 2} | {Milestone/phase} | {Role} |
```

**Rules:**
- Include only top 5-6 risks here (full register in Stage 13)
- Focus on risks relevant to the investment decision (not implementation risks)
- Dependencies should be things that could block the project starting or delivering

---

### Step 10: Formulate Recommendation

```markdown
## Recommendation

{1-2 paragraph professional recommendation statement covering:}
- What is recommended (proceed / proceed with conditions / defer / reject)
- Why (reference strategic alignment, feasibility, priority)
- What is needed next (approval, budget confirmation, next phase)
- Key conditions or prerequisites (if any from feasibility)

**Recommendation:** {☑ Approve / ☑ Approve with Conditions / ☐ Defer / ☐ Reject}
```

---

### Step 11: Add Approval Table

```markdown
## Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Project Sponsor | {name or TBD} | _[Pending]_ | |
| Finance Approval | {name or TBD} | _[Pending]_ | |
| Technical Approval | {name or TBD} | _[Pending]_ | |
| PMO Approval | {name or TBD} | _[Pending]_ | |
| Product Owner / Requestor | {name or TBD} | _[Pending]_ | |
```

**Rules:**
- Populate names from Stakeholder data in Intake Form
- Use `_[TBD]_` for roles not yet assigned
- Roles included should match organizational governance (ask user if unclear)

---

### Step 12: Assemble and Validate

1. Compile all sections into the full Business Case document using template `templates/business-case.md`
2. Run content validation (per `common/content-validation.md`):
   - Cross-reference check: costs mentioned in text match cost table
   - Timeline consistency: milestones here match any dates mentioned elsewhere
   - Scope consistency: what's described matches Intake Form
   - No contradictions with Feasibility Assessment
3. Add document metadata: version, date, status, prepared by

---

### Step 13: Present for Review

```markdown
## Review: Business Case — {project_name}

I've produced the Business Case document. Key highlights:

- **Problem:** {1 sentence summary}
- **Recommended approach:** {Option name — 1 sentence}
- **Investment required:** {Total ROM or range}
- **Key benefits:** {Top 2-3 benefits — 1 line each}
- **Priority justification:** {MoSCoW} — {Pn} — Strategic score: {n}/25
- **Recommendation:** {Approve / Approve with Conditions / Defer / Reject}

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Business case captures the justification; proceed to Charter
- (b) **Request changes** — Specific sections need adjustment
- (c) **Strengthen financials** — I have additional cost/benefit data to add
- (d) **Change recommendation** — I want a different conclusion
- (e) **Park here** — Business case is sufficient; don't need full PIP
```

---

### Step 14: Iterate and Finalize

If user requests changes:
1. Ask which sections to modify
2. Apply changes
3. Re-validate
4. Re-present summary
5. Repeat until approved

---

### Step 15: Log and Transition

1. **Decision Log:** D-{nnn}: "Business Case approved. Recommended approach: {option}. Investment: {ROM}. Recommendation: {approve/conditions/defer}."
2. **State File:** Stage 8 = ✅ Done; Current Phase = AUTHORIZATION; Current Stage = 9
3. **Assumptions Register:** Add any financial assumptions made
4. **Lessons Learned:** Note if cost data was unavailable (common lesson)

Display transition:

```
✅ Stage 8: Business Case Development — Complete

📄 Business Case: {recommendation} — {approach_name}
💰 Investment: {ROM range}
📊 Strategic alignment: {n}/25

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ JUSTIFICATION PHASE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next → AUTHORIZATION PHASE
Stage 9: Project Charter — I'll formalize the project's authority,
objectives, and boundaries.

Proceeding...
```

---

## Output File

Save to:
- Numbered: `{output_root}/03_Business_Case/Business_Case.md`
- Flat: `{output_root}/pilc-docs/justification/Business_Case.md`

---

## Business Case Anti-Patterns (Avoid)

| Anti-Pattern | Why It's Wrong | What to Do Instead |
|-------------|---------------|-------------------|
| Benefits without basis | "Save millions" with no supporting logic | State assumptions; use ranges; cite sources |
| Hidden costs | Omitting training, change management, maintenance | Include ALL cost categories; use contingency for unknowns |
| Single-option framing | Only presenting the preferred approach | Always include "Do Nothing" + at least one alternative |
| Technology-first justification | Focusing on tech features rather than business outcomes | Lead with business problem and value; tech is the how, not the why |
| Precision without data | "$3,247,891" when no real data exists | Use ranges; state confidence level; round appropriately |
| Ignoring ongoing costs | Only showing project cost, not operational run cost | Include Year 2/3 operational costs |
