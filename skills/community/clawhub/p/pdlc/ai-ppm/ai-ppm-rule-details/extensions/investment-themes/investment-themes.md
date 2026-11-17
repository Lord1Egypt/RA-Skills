<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension E5: Investment Themes / Strategic Buckets

**Stages affected:** 3 (Strategic Alignment)
**Adds:** Investment categories, target allocation, per-project classification, distribution tracking

---

## Additional Steps for Stage 3 (after Step 3.2, before scoring)

### Step 3.E5.1: Define Investment Categories

```
Q-{NN}: What investment categories does your organization use?

Common patterns:
(a) Run / Grow / Transform (3 buckets)
(b) Run / Grow / Innovate / Comply (4 buckets)
(c) Core / Adjacent / Transformational (McKinsey 3 Horizons)
(d) Custom categories: ___

For each category, define target budget allocation:

| # | Category | Target % | Description |
|---|----------|:--------:|-------------|
| 1 | {Run} | {40}% | {Maintain current business operations} |
| 2 | {Grow} | {30}% | {Expand existing capabilities/markets} |
| 3 | {Innovate} | {20}% | {New capabilities, R&D, experiments} |
| 4 | {Comply} | {10}% | {Regulatory, security, mandatory} |
| | **Total** | **100%** | |
```

### Step 3.E5.2: Classify Projects into Categories

```
BQ-{NN}: Classify each project into an investment category

| Project | Budget | Suggested Category | Rationale | Your Classification |
|---------|-------:|:------------------:|-----------|:-------------------:|
| {A} | ${X} | Run | "Infrastructure maintenance" | _[   ]_ |
| {B} | ${Y} | Grow | "New market expansion" | _[   ]_ |
| {C} | ${Z} | Innovate | "AI platform — new capability" | _[   ]_ |
```

### Step 3.E5.3: Calculate Distribution

```markdown
## Investment Theme Distribution

| Category | Target | Actual (Budget) | Actual (Count) | Variance | Status |
|----------|:------:|:---------------:|:--------------:|:--------:|:------:|
| Run | {40}% | {pct}% (${amt}) | {N} projects | {+/-}% | {🟢/🟡/🔴} |
| Grow | {30}% | {pct}% (${amt}) | {N} projects | {+/-}% | {🟢/🟡/🔴} |
| Innovate | {20}% | {pct}% (${amt}) | {N} projects | {+/-}% | {🟢/🟡/🔴} |
| Comply | {10}% | {pct}% (${amt}) | {N} projects | {+/-}% | {🟢/🟡/🔴} |

Status: 🟢 = within ±5% of target | 🟡 = ±5-15% variance | 🔴 = >15% variance
```

### Step 3.E5.4: Investment Alerts

```
⚠️ Investment theme alerts:

• {Category} is over-invested: {actual}% vs. {target}% target (+{delta}%)
  → Consider: move ${amount} to {under-invested category}
  
• {Category} is under-invested: {actual}% vs. {target}% target (-{delta}%)
  → The portfolio has a gap in {category} — new projects in this category should be prioritized
```

### Step 3.E5.5: Update Alignment Map

Add investment theme column to `strategic-alignment-map.md`.

---

## Impact on Governance Gate (Stage 5)

When E5 is active, the governance gate additionally checks:
- "If we admit this project, does it push its category over the threshold?"
- If yes → flag as a guardrail concern (user can override with rationale)

---

*This extension ensures portfolio investment is intentionally distributed across strategic categories, not accidentally concentrated.*
