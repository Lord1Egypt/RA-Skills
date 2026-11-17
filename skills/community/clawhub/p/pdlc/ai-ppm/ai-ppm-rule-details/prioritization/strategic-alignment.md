<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 3: Strategic Alignment

**Phase:** Prioritization & Alignment
**Purpose:** Map organizational strategy to portfolio investment categories, and score each project's alignment to strategic objectives. This ensures every project can justify its existence against the organization's stated direction.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | 2-3 strategic objectives. Simple High/Medium/Low alignment per project. No weighting. |
| **Standard** | 3-5 objectives. Scored alignment matrix (1-5 per cell). Weighted totals. |
| **Comprehensive** | 5-7 objectives. Weighted scoring + investment theme allocation (Extension E5). OKR linkage if available from POLC. |

---

## Step-by-Step Execution

### Step 3.1: Establish Strategic Objectives

**First time:** Elicit organizational strategic objectives from the user.

```
Q-{NN}: What are your organization's strategic objectives?

These are the 3-7 high-level goals that ALL projects should contribute to.
Examples: "Grow revenue 20% YoY", "Reduce operational cost", "Enter new market segment",
"Improve customer retention", "Achieve regulatory compliance", "Build platform capability"

Please list your strategic objectives (or point me to a strategy document):
```

**Subsequent sessions:** Load from `ppm-state.md` → Strategic Objectives. Ask if they need updating.

```
📋 Current strategic objectives:
1. {Objective 1}
2. {Objective 2}
3. {Objective 3}
...

Still accurate? [Yes / Update / Add / Remove]
```

### Step 3.2: Assign Weights (Standard+ Depth)

At Standard or Comprehensive depth, ask user to weight the objectives:

```
Q-{NN}: How important is each objective relative to the others?

Distribute 100 points across your objectives (more points = more important):

| # | Objective | Weight |
|---|-----------|--------|
| 1 | {Obj 1} | _[  ]_ |
| 2 | {Obj 2} | _[  ]_ |
| 3 | {Obj 3} | _[  ]_ |
| Total | | 100 |

Suggested weights: {based on objective language and typical patterns}
Accept suggestion? [Yes / Adjust]
```

At Minimal depth: All objectives weighted equally.

### Step 3.3: Score Projects Against Objectives

For each project being aligned, score its contribution to each objective:

**Scoring scale:**
| Score | Meaning |
|:---:|---|
| 5 | Primary driver — this project directly advances this objective |
| 4 | Strong contribution — significant but not the primary purpose |
| 3 | Moderate contribution — some benefit to this objective |
| 2 | Weak contribution — tangential benefit only |
| 1 | No contribution — this project doesn't serve this objective |
| 0 | Negative — this project may conflict with this objective |

**Presentation (batch format for efficiency):**

```
BQ-{NN}: Score projects against "{Objective 1}"

| # | Project | Suggested | Rationale | Your Score |
|---|---------|:---------:|-----------|:----------:|
| 1 | {Project A} | 4 | Charter states "{relevant objective text}" | _[  ]_ |
| 2 | {Project B} | 2 | No direct mention; tangential benefit via {X} | _[  ]_ |
| 3 | {Project C} | 5 | Primary purpose is "{matches objective}" | _[  ]_ |

Accept all? [Yes / Adjust specific items]
```

Repeat for each objective.

### Step 3.4: Calculate Alignment Scores

Compute weighted alignment score per project:

```
Alignment Score = Σ (score_i × weight_i) / Σ weight_i × 5
```

Normalized to /25 scale (matching PILC's strategic assessment scale for comparability).

### Step 3.5: Produce Strategic Alignment Map

Generate `strategic-alignment-map.md`:

```markdown
# Strategic Alignment Map

## Organizational Objectives

| # | Objective | Weight |
|---|-----------|:------:|
| 1 | {Obj 1} | {W1}% |
| 2 | {Obj 2} | {W2}% |
...

## Alignment Matrix

| Project | Obj 1 | Obj 2 | Obj 3 | ... | Weighted Score | Rank |
|---------|:-----:|:-----:|:-----:|:---:|:--------------:|:----:|
| {Project A} | 4 | 3 | 5 | ... | 21/25 | 1 |
| {Project B} | 2 | 5 | 2 | ... | 18/25 | 2 |
| {Project C} | 1 | 2 | 3 | ... | 12/25 | 3 |

## Findings

- **Highly aligned (20+):** {list}
- **Moderately aligned (13-19):** {list}
- **Weakly aligned (<13):** {list} ← candidates for deprioritization or retirement

## Recommendations

{Any projects with very low alignment that should be questioned}
```

### Step 3.6: Flag Low-Alignment Projects

If any project scores below 10/25:
```
⚠️ Low strategic alignment detected:
   • {Project X}: 8/25 — does not clearly serve any strategic objective
   
   Options:
   (a) Keep and proceed — alignment isn't everything (urgency/compliance may justify)
   (b) Flag for governance gate review — question whether this should be in the portfolio
   (c) Retire now — remove from active portfolio
```

### Step 3.7: Update Portfolio Register

Add alignment scores to the register:

| Column | Value |
|---|---|
| Strategic Alignment | {score}/25 |

### Step 3.8: Extension Check — Investment Themes (E5)

If Extension E5 is active, additionally:
- Categorize projects into investment themes (Growth / Run / Innovate / Compliance / etc.)
- Show distribution: "60% Run, 25% Growth, 10% Innovate, 5% Compliance"
- Flag imbalance: "Portfolio is heavily weighted toward Run — limited growth investment"

---

## Gate

User approves the alignment map and any low-alignment flags → proceed to Stage 4.

---

## Outputs

| Artifact | Status |
|---|---|
| `strategic-alignment-map.md` | Created/updated |
| `portfolio-register.md` | Updated (alignment scores column) |
| `ppm-state.md` | Updated (objectives stored, stage position) |

---

## Management Framework Contribution

Entry: `PPM-D-{NNN}: Strategic alignment scored for {N} projects. {M} weakly aligned (flagged). Model: {weighted/equal}. Objectives: {count}.`

---

*This stage runs whenever: (a) a new project is registered, (b) strategic objectives change, or (c) a quarterly strategic review is triggered.*
