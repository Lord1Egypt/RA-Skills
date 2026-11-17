<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension E7: Benefits Realization Aggregation

**Stages affected:** 8 (Portfolio Dashboards), 10 (Project Retirement)
**Adds:** Cross-project benefits tracking, realization curve, value-gap analysis, estimation accuracy lessons

---

## Data Source

Benefits data comes from:
- **AI-POLC Stage 16** (Value & Metrics Engine) — per-project KPI actuals, benefits_realized_pct
- **Carried by FLO** (cross-layer) — roll-up payload includes benefits slice
- **Retirement records** — final benefits status captured at project closure

AI-PPM never computes per-project benefits — it aggregates what POLC and retirement records provide.

---

## Additional Steps for Stage 8 (after Step 8.6)

### Step 8.E7.1: Benefits Realization Dashboard Section

```markdown
## Benefits Realization (Extension E7)

### Portfolio Benefits Summary

| Metric | Value |
|--------|------:|
| Total benefits promised (all projects) | ${amount} or {count} KPIs |
| Benefits realized to date | ${amount} or {count} ({pct}%) |
| Benefits pending (projects still active) | ${amount} or {count} |
| Benefits not realized (retired without delivery) | ${amount} or {count} |

### Per-Project Benefits Status

| Project | State | Benefits Promised | Realized | Status |
|---------|:-----:|:-----------------:|:--------:|:------:|
| {A} | Active | ${X} / 5 KPIs | ${Y} / 3 KPIs ({pct}%) | 🟢 On track |
| {B} | Active | ${X} / 3 KPIs | ${Y} / 1 KPI ({pct}%) | 🟡 Behind |
| {C} | Retired | ${X} / 4 KPIs | ${Y} / 4 KPIs (100%) | ✅ Delivered |
| {D} | Retired | ${X} / 3 KPIs | ${Y} / 0 KPIs (0%) | ❌ Not delivered |

### Value Gap Analysis

Projects consuming significant budget but not delivering proportional benefits:

| Project | Budget Spent | Benefits Realized | Value Ratio | Concern |
|---------|:-----------:|:-----------------:|:-----------:|---------|
| {B} | ${spent} | ${realized} | {ratio} | {Low return — investigate} |

### Estimation Accuracy (Learning Loop)

| Metric | Average Across Portfolio |
|--------|:-----------------------:|
| Benefits predicted vs. actual | {pct}% accuracy |
| Time to realize (predicted vs. actual) | {months predicted} vs. {months actual} |
| Systematic bias | {Over-estimate by {pct}% / Under-estimate / Accurate} |

**Implication for future scoring:** {If we systematically over-estimate benefits by X%, future business cases should be discounted by X% in prioritization scoring}
```

---

## Additional Steps for Stage 10 (after Step 10.3)

### Step 10.E7.1: Benefits Closure Analysis

During project retirement, produce a comprehensive benefits assessment:

```markdown
## Benefits Closure Analysis (Extension E7)

### Benefit-by-Benefit Status

| # | Benefit (from Business Case) | Target | Actual | Realization % | Notes |
|---|------------------------------|--------|--------|:-------------:|-------|
| 1 | {benefit} | {target metric} | {actual metric} | {pct}% | {context} |
| 2 | {benefit} | {target} | {actual} | {pct}% | {context} |

### Time-to-Realize

| Benefit | Predicted Timeline | Actual Timeline | Variance |
|---------|:------------------:|:---------------:|:--------:|
| {benefit 1} | {N months post-delivery} | {M months} | {+/- weeks} |

### Lessons for Portfolio Governance

| Finding | Impact on Future Decisions |
|---------|---------------------------|
| {e.g., "Benefits took 2× longer to realize than predicted"} | {e.g., "Extend benefits measurement window from 6→12 months"} |
| {e.g., "Qualitative benefits realized but hard to measure"} | {e.g., "Include proxy metrics for qualitative benefits in future business cases"} |

### Contribution to Estimation Model

This project's actuals improve our portfolio-level estimation accuracy:
- Benefits prediction accuracy: {pct}% (this project) vs. {pct}% (portfolio average)
- Recommendation: {adjust scoring model / maintain current / flag systematic bias}
```

---

## Portfolio-Level Learning Loop

Over time (>5 retired projects), E7 can produce:

```markdown
## Benefits Estimation Accuracy — Portfolio Learning

Based on {N} retired projects:

| Category | Avg. Prediction | Avg. Actual | Bias |
|----------|:--------------:|:----------:|:----:|
| Financial benefits ($) | ${predicted} | ${actual} | {over/under by pct}% |
| Timeline to realize | {months} | {months} | {over/under by pct}% |
| KPI achievement | {predicted count} | {actual count} | {pct}% hit rate |

**Recommended adjustment to scoring model:**
- Discount financial benefit estimates by {pct}% in prioritization (Stage 4)
- Add {N months} buffer to benefits measurement timeline
- Weight {category} benefits lower in future (unreliable predictor)
```

---

*This extension closes the feedback loop: did our portfolio investments actually deliver what was promised? It makes future governance decisions better-calibrated.*
