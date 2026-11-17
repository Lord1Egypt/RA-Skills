<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 6: Value-Based Prioritization

**Phase:** Strategy
**Purpose:** Rank the backlog using an explicit, auditable prioritization model with recorded rationale per ordering decision — eliminating opinion-driven ordering.

---

## MANDATORY: Stage Sub-Role

During this stage, also adopt the **Financial Analyst** sub-role:

### Behavioral Shifts
- Think in terms of value quantification: cost of delay, revenue impact, risk reduction value
- Apply economic models to ordering decisions — every position has a rationale
- Challenge "gut feel" prioritization — demand the model's output as justification
- Consider opportunity cost: choosing to build X means NOT building Y — make that trade-off explicit

### Anti-Patterns
- Do NOT accept "this is urgent" as a priority justification without defining "urgent" in model terms
- Do NOT allow HiPPO (Highest Paid Person's Opinion) to override the model without recording why
- Do NOT produce a flat list with no rationale — every position needs a "because" statement
- Do NOT mix models mid-backlog (don't use WSJF for some and MoSCoW for others)

### Quality Check
Every priority position must pass: "Can I explain to a stakeholder WHY item X is ranked above item Y using the declared model?" If no → rationale is missing.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Simple MoSCoW or value/effort 2×2. Rationale in one sentence per item. |
| **Standard** | Full model (WSJF or value-effort with scoring). Rationale paragraph per item. Re-prioritization triggers defined. |
| **Comprehensive** | WSJF with detailed scoring. Multiple stakeholder input weighted. Sensitivity analysis. Documented alternatives considered. |

---

## Steps

### Step 6.1: Select Prioritization Model

Present options to user:

| # | Model | Best For | Trade-off |
|---|-------|----------|-----------|
| 1 | **WSJF** (Weighted Shortest Job First) | Lean/SAFe, continuous flow, quantitative teams | Needs sizing data; most rigorous |
| 2 | **MoSCoW** (Must/Should/Could/Won't) | Fixed-scope projects, stakeholder consensus | Fast but less precise; no ordering within tiers |
| 3 | **Value/Effort Matrix** | Early-stage products, limited data | Intuitive but subjective |
| 4 | **Custom** | Specific organizational needs | User defines criteria and weights |

Recommend based on context:
- SAFe / Kanban → WSJF
- Scrum with fixed sprints → Value/Effort or MoSCoW
- New product (0→1) → Value/Effort (not enough data for WSJF)
- Enterprise with stakeholder committees → MoSCoW (accessible to non-technical)

Record the selection as a governance decision.

### Step 6.2: Apply the Selected Model

#### If WSJF:

For each epic, score:

| Factor | Scale | Description |
|--------|:---:|-------------|
| Business Value | 1-10 | Revenue/user impact if delivered |
| Time Criticality | 1-10 | Cost of delay — what's lost by waiting? |
| Risk Reduction | 1-10 | Uncertainty/risk removed by doing this |
| Job Duration | 1-10 | Relative effort/complexity (higher = longer) — **inform with the AI-ADLC feasibility/cost-risk band for the affected area when present** (effort band S/M/L/XL → Job Duration); raise the score where ADLC flags technical risk/debt |

**WSJF Score = (Business Value + Time Criticality + Risk Reduction) / Job Duration**

Rank by descending WSJF score.

#### If MoSCoW:

Classify each epic:

| Category | Criteria |
|----------|----------|
| **Must** | Without this, the product fails / is non-viable / breaches compliance |
| **Should** | Important for product success but viable without for first release |
| **Could** | Desirable, adds value, but clear workarounds exist |
| **Won't** (this time) | Explicitly out of current scope — acknowledged and deferred |

Within each category, order by value/effort ratio.

#### If Value/Effort:

Score each epic on two axes (1-10):
- **Value:** User impact + business outcome + strategic alignment
- **Effort:** Complexity + dependencies + unknowns

Plot and classify:
- High Value / Low Effort = **Quick Wins** (do first)
- High Value / High Effort = **Big Bets** (plan carefully)
- Low Value / Low Effort = **Fill-ins** (do if capacity allows)
- Low Value / High Effort = **Avoid** (don't build)

### Step 6.3: Record Rationale

For EVERY epic in the prioritized list, record:

```
| Rank | Epic | Score | Rationale |
|:----:|------|:-----:|-----------|
| 1 | EPIC-003: Provider Abstraction | WSJF: 8.5 | Highest CoD: blocks all payment integrations; enables parallel work on providers |
| 2 | EPIC-001: Async Processing | WSJF: 7.2 | Critical path for <2s goal; moderate effort |
| 3 | EPIC-005: Onboarding Redesign | WSJF: 6.8 | High business value (20% drop-off); independent of payment work |
```

### Step 6.4: Define Re-Prioritization Triggers

Document when the priority order should be revisited:

| Trigger | Action |
|---------|--------|
| New feature brief from AI-ILC | Assess and insert into ranked list |
| Approved change request from AI-PILC | Re-evaluate affected epics |
| **AP feasibility / cost-risk update (AI-ADLC)** | **Re-score affected epics — fold the updated effort/complexity band into WSJF Job Duration (or value/effort); a "3× the cost" verdict can reorder the roadmap. This is the Architecture→Product cost loop (same-layer read of `adlc-state.md`).** |
| Blocker from AI-DLC v1 | Move blocked epic down; pull alternative forward |
| Market change / competitor move | Full re-prioritization session |
| Sprint/increment review reveals new data | Selective re-score of affected epics |
| {cadence}: every {N} sprints | Scheduled re-prioritization review |

### Step 6.5: Handle Conflicts

When multiple stakeholders disagree on priority:
1. Make the disagreement visible (who wants what, why)
2. Apply the model — does the quantitative answer resolve it?
3. If model is ambiguous, escalate per PO Charter (Stage 3) escalation rules
4. Record the resolution in the governance spine

### Step 6.6: Persist Prioritization Register

Write `prioritization-register.md` with:
- Model used (and why selected)
- Scoring criteria (if WSJF: the 4 factors; if custom: the defined criteria)
- Ranked list with scores and rationale
- Re-prioritization triggers
- Conflict resolution record (if any)
- Last updated date

---

## Gate

**Gate 6 — Prioritization Confirmed:**

Present to user:
```
Backlog prioritized using: {model name}

Top 5:
1. {Epic} — Score: {X} — {one-line rationale}
2. {Epic} — Score: {X} — {one-line rationale}
3. {Epic} — Score: {X} — {one-line rationale}
4. {Epic} — Score: {X} — {one-line rationale}
5. {Epic} — Score: {X} — {one-line rationale}

{If >5: "+ {N} more epics ranked — see full register"}

Re-prioritization triggers: {N} defined

Does this ordering reflect your value judgment?
Approve to proceed to Release Slicing, or adjust rankings.
```

User must confirm before proceeding.

---

## Governance Spine Entry

Log in Decision Log:
```
POLC-D-005: Prioritization model selected: {model}. 
{N} epics ranked. Top priority: {EPIC-NNN}.
Re-prioritization cadence: {trigger summary}.
```

---

## Transition

→ **Stage 7: Release & Increment Slicing** (Strategy continues)

---

*Detail file for AI-POLC Stage 6 | Phase: Strategy*
