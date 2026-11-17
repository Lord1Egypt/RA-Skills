<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 4: Cross-Project Prioritization

**Phase:** Prioritization & Alignment
**Purpose:** Rank all active portfolio projects against each other using an explicit, auditable model. This is AI-PPM's core unique value — no other package does project-vs-project ranking.

---

## MANDATORY: Stage Sub-Role — Financial Analyst

During THIS stage, ALSO adopt the mindset of a **Financial Analyst**. This does NOT replace your primary role (Portfolio Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in terms of investment return, cost of delay, and opportunity cost
- Frame every project as an investment competing for finite capital
- Challenge soft justifications: "important" means nothing without a number
- Quantify where possible, estimate where not, acknowledge uncertainty explicitly

### Anti-Patterns for This Stage
- Do NOT accept "all projects are high priority" — forced ranking is the point
- Do NOT prioritize without a stated model — opinion is not governance

### Quality Check
A good prioritization sounds like:
- "Project A ranks #1 (score: 87/100) because it has the highest cost-of-delay ($50K/week) combined with strong strategic alignment (22/25). Project B ranks #2 despite higher alignment (24/25) because its effort is 3× larger, making the value/effort ratio unfavorable."

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Simple Value vs. Effort (2-axis). One score per axis. Quick forced rank. |
| **Standard** | Multi-criteria weighted scoring (4-6 dimensions). Composite score. Formal rank. |
| **Comprehensive** | Full scoring + pairwise validation + cost-of-delay/WSJF + extension E1 (balancing). |

---

## Step-by-Step Execution

### Step 4.1: Select Prioritization Model

If first time (no model established), present options:

```
Q-{NN}: Which prioritization model should we use?

(a) Value vs. Effort — simple 2-axis scoring (good for ≤5 projects)
(b) Weighted Multi-Criteria — score on 4-6 dimensions with weights (good for 5-15 projects)
(c) WSJF (Weighted Shortest Job First) — time-sensitivity emphasis (SAFe/Lean style)
(d) Pairwise Comparison — forced head-to-head (good for ≤7 projects, hard to game)

Recommended: {based on portfolio size and depth level}
Rationale: {why}
```

If model already established (stored in `ppm-state.md`): confirm it's still appropriate.

### Step 4.2: Define Scoring Dimensions

**For Value vs. Effort (Model A):**
- Value (1-10): Business impact + strategic alignment + urgency
- Effort (1-10): Complexity + duration + resource demand

**For Weighted Multi-Criteria (Model B):**

| Dimension | Description | Suggested Weight |
|---|---|---|
| Strategic Alignment | Score from Stage 3 (normalized to 1-10) | 30% |
| Business Value | Revenue impact, cost savings, customer impact | 25% |
| Urgency | Time sensitivity, regulatory deadline, competitive pressure | 20% |
| Risk (inverse) | Lower risk = higher score | 15% |
| Feasibility | From PIP feasibility score, normalized | 10% |

Ask user to confirm or adjust dimensions and weights:
```
Q-{NN}: Confirm scoring dimensions and weights.

| # | Dimension | Weight | Source |
|---|-----------|:------:|--------|
| 1 | Strategic Alignment | 30% | Stage 3 score (auto) |
| 2 | Business Value | 25% | PIP Business Case / user assessment |
| 3 | Urgency | 20% | Deadline pressure / cost of delay |
| 4 | Risk (low = better) | 15% | PIP Feasibility (inverted) |
| 5 | Feasibility | 10% | PIP Feasibility score |

Accept? [Yes / Adjust weights / Add dimension / Remove dimension]
```

**For WSJF (Model C):**
- WSJF = (User-Business Value + Time Criticality + Risk Reduction) / Job Size
- Each numerator scored 1-10 via Fibonacci-style relative sizing

### Step 4.3: Score Each Project

Present scoring in batch format per dimension (see `question-format-guide.md` → Batch Questions):

```
BQ-{NN}: Score all projects on "Business Value" (1-10)

Scoring guide:
  1-2: Marginal impact, nice-to-have
  3-4: Moderate impact, measurable benefit
  5-6: Significant impact, clear business case
  7-8: High impact, strong ROI
  9-10: Transformative, strategic breakthrough

| # | Project | PIP Evidence | Suggested | Your Score |
|---|---------|-------------|:---------:|:----------:|
| 1 | {A} | "NPV $2.1M, ROI 180%" | 8 | _[  ]_ |
| 2 | {B} | "Cost avoidance $400K/yr" | 6 | _[  ]_ |
| 3 | {C} | "Customer satisfaction improvement" | 4 | _[  ]_ |
```

Repeat for each dimension.

**Auto-populated dimensions:**
- Strategic Alignment: pulled directly from Stage 3 (normalized to 1-10 scale)
- Feasibility: pulled from PIP feasibility score if available
- Risk (inverted): pulled from PIP risk assessment if available

### Step 4.4: Calculate Composite Scores & Rank

```
Composite Score = Σ (dimension_score × weight) / Σ weights × 10 → normalized to /100
```

### Step 4.5: Produce Prioritization Scorecard

Generate `prioritization-scorecard.md`:

```markdown
# Portfolio Prioritization Scorecard

## Model
- **Type:** {Weighted Multi-Criteria / Value-Effort / WSJF}
- **Dimensions:** {list with weights}
- **Scored on:** {ISO-date}

## Results

| Rank | Project | ID | Strat. Align. | Bus. Value | Urgency | Risk⁻¹ | Feasibility | Composite | Delta |
|:----:|---------|-----|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | {A} | {ID} | 9 | 8 | 7 | 8 | 9 | 84/100 | — |
| 2 | {B} | {ID} | 8 | 6 | 9 | 7 | 7 | 74/100 | -10 |
| 3 | {C} | {ID} | 5 | 4 | 3 | 9 | 8 | 52/100 | -22 |

## Key Observations
- {Top-ranked project and why}
- {Biggest gap between projects (natural cut line)}
- {Any conflicts: top-ranked projects competing for same resources}

## Governance Override (if any)
| Project | Score Rank | Actual Rank | Override Rationale |
|---------|:----------:|:-----------:|---|
| — | — | — | No overrides |
```

### Step 4.6: Identify Resource Conflicts

If multiple highly-ranked projects share key resources (teams, infrastructure, dependencies):

```
⚠️ Resource conflict detected:
   • Projects {A} (#1) and {B} (#2) both require the {Platform Team}
   • Running both in parallel exceeds team capacity

   Options:
   (a) Sequence them: A first, then B (adds {N} weeks to B)
   (b) Sequence them: B first, then A (adds {N} weeks to A)
   (c) Run in parallel with reduced velocity for both
   (d) Flag for governance gate decision (Stage 5)
```

### Step 4.7: Present & Confirm

```
📊 Portfolio Prioritization Complete

Ranked portfolio (top to bottom):
1. {Project A} — 84/100 ⬆️
2. {Project B} — 74/100
3. {Project C} — 52/100 ⬇️

Natural cut line: Between #2 and #3 (22-point gap)
Conflicts: {list or "none"}

Approve this ranking? [Yes / Adjust scores / Override a rank / Re-weight dimensions]
```

---

## Gate

User approves the prioritized ranking → proceed to Stage 5 (Governance Gate).

---

## Outputs

| Artifact | Status |
|---|---|
| `prioritization-scorecard.md` | Created/updated |
| `portfolio-register.md` | Updated (priority rank column) |
| `ppm-state.md` | Updated (model stored, last ranked date) |

---

## Management Framework Contribution

Entry: `PPM-D-{NNN}: Portfolio prioritized. Model: {type}. {N} projects ranked. Top: {name}. Natural cut line at #{M}.`

---

## Extension Check — Portfolio Balancing (E1)

If Extension E1 is active, additionally after ranking:
- Generate bubble chart data (Value × Effort, size = budget)
- Show horizon distribution (H1/H2/H3 across ranked projects)
- Check balance guardrails (if defined)
- Flag: "Portfolio is imbalanced: 80% H1, 20% H2, 0% H3"

---

*This stage runs whenever: (a) new projects are registered, (b) rebalancing is triggered, or (c) quarterly strategic review occurs.*
