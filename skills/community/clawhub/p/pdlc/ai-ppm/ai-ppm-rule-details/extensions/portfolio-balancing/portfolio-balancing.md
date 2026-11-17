<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension E1: Portfolio Balancing & Visualization

**Stages affected:** 4 (Cross-Project Prioritization), 8 (Portfolio Dashboards)
**Adds:** Bubble chart data, horizon distribution, risk-spread analysis, balance guardrails

---

## Additional Steps for Stage 4 (after Step 4.7)

### Step 4.E1.1: Classify Projects by Horizon

For each project, assign an innovation horizon:

| Horizon | Meaning | Examples |
|:-------:|---------|---------|
| **H1 — Core** | Protecting/optimizing current business | Compliance, maintenance, performance improvement |
| **H2 — Adjacent** | Extending into related opportunities | New feature lines, market expansion, integration |
| **H3 — Transformational** | Creating new capabilities for the future | R&D, new platform, disruptive innovation |

Present for user confirmation:
```
BQ-{NN}: Classify projects by innovation horizon

| Project | Suggested Horizon | Rationale | Your Classification |
|---------|:-----------------:|-----------|:-------------------:|
| {A} | H1 | "Regulatory compliance — protects current" | _[H1/H2/H3]_ |
| {B} | H2 | "New market segment — adjacent growth" | _[H1/H2/H3]_ |
| {C} | H3 | "AI platform — transformational bet" | _[H1/H2/H3]_ |
```

### Step 4.E1.2: Generate Bubble Chart Data

Produce data for a Value × Effort bubble chart:

```markdown
## Bubble Chart Data

| Project | X (Effort) | Y (Value) | Size (Budget) | Color (Horizon) |
|---------|:----------:|:---------:|:-------------:|:---------------:|
| {A} | {1-10} | {1-10} | ${budget} | H1 (blue) |
| {B} | {1-10} | {1-10} | ${budget} | H2 (green) |
| {C} | {1-10} | {1-10} | ${budget} | H3 (orange) |

Quadrant interpretation:
• Top-left (high value, low effort): "Do first" — quick wins
• Top-right (high value, high effort): "Invest" — strategic bets
• Bottom-left (low value, low effort): "Fill" — opportunistic
• Bottom-right (low value, high effort): "Reconsider" — poor investment
```

### Step 4.E1.3: Horizon Distribution Analysis

```markdown
## Horizon Distribution

| Horizon | Count | Budget % | Target % | Variance |
|:-------:|:-----:|:--------:|:--------:|:--------:|
| H1 — Core | {N} | {pct}% | {target}% | {+/-}% |
| H2 — Adjacent | {N} | {pct}% | {target}% | {+/-}% |
| H3 — Transformational | {N} | {pct}% | {target}% | {+/-}% |

Typical balanced target: 70% H1 / 20% H2 / 10% H3 (adjust per org strategy)

Assessment: {Balanced / Skewed toward {horizon} / Critically imbalanced}
```

### Step 4.E1.4: Risk-Spread Analysis

Check for concentration risk:

```markdown
## Risk Concentration

| Risk Category | Project Count | Budget Exposed | Concentration Level |
|---------------|:------------:|:--------------:|:-------------------:|
| {Technical} | {N} | ${amount} | {Low/Medium/High} |
| {Resource} | {N} | ${amount} | {Low/Medium/High} |
| {Market} | {N} | ${amount} | {Low/Medium/High} |

⚠️ Concentration alerts:
- {if >50% of budget in one risk category: flag}
- {if >3 projects share the same key risk: flag}
```

### Step 4.E1.5: Balance Guardrails (Optional)

If user wants enforcement:
```
Q-{NN}: Set balance guardrails?

(a) No guardrails — visualization only (advisory)
(b) Soft guardrails — warn when distribution exceeds thresholds
(c) Hard guardrails — block admission if it would breach thresholds

If (b) or (c), define thresholds:
• H1 maximum: _[  ]_% (e.g., 80%)
• H2 minimum: _[  ]_% (e.g., 15%)
• H3 minimum: _[  ]_% (e.g., 5%)
• Risk concentration max: _[  ]_% in any single category
```

---

## Additional Steps for Stage 8 (after Step 8.6)

### Step 8.E1.1: Balance Dashboard Section

Add to portfolio-health-dashboard.md:

```markdown
## Portfolio Balance (Extension E1)

### Horizon Distribution
{table from 4.E1.3 — refreshed with current data}

### Bubble Chart Data
{table from 4.E1.2 — refreshed}

### Risk Spread
{table from 4.E1.4 — refreshed}

### Guardrail Status
| Guardrail | Threshold | Current | Status |
|-----------|:---------:|:-------:|:------:|
| H1 max | {pct}% | {actual}% | {🟢✅ / 🔴⚠️} |
| H2 min | {pct}% | {actual}% | {🟢✅ / 🔴⚠️} |
| Risk concentration | {pct}% | {actual}% | {🟢✅ / 🔴⚠️} |
```

---

*This extension transforms ranking from a one-dimensional list into a multi-dimensional portfolio view.*
