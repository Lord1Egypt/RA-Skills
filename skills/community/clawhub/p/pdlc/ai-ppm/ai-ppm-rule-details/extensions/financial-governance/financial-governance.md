<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension E6: Financial Governance

**Stages affected:** 5 (Governance Gate), 8 (Portfolio Dashboards)
**Adds:** Budget guardrails, approval thresholds, portfolio ROI tracking, burn-rate monitoring

---

## Setup (First Activation)

### Step E6.0: Configure Financial Guardrails

```
Q-{NN}: Define your portfolio's financial governance rules:

| Guardrail | Value | Description |
|-----------|-------|-------------|
| Portfolio budget ceiling | $_____ | Maximum total portfolio commitment |
| Per-project max (auto-approve) | $_____ | Projects below this: no escalation needed |
| Per-project escalation threshold | $_____ | Projects above this: require sponsor sign-off |
| Contingency reserve | ___% | Percentage held back for emergencies |
| Overrun tolerance | ___% | Acceptable variance before escalation |
| Funding model | {Project-based / Incremental / Hybrid} | How funding is released |
```

---

## Additional Steps for Stage 5 (before Step 5.2)

### Step 5.E6.1: Financial Guardrail Check

Before presenting governance decisions, validate financial feasibility:

```markdown
## Financial Guardrail Check

| Guardrail | Threshold | Current | If Admitted | Status |
|-----------|:---------:|:-------:|:-----------:|:------:|
| Portfolio ceiling | ${ceiling} | ${committed} | ${with new} | {🟢/🔴} |
| Per-project threshold | ${max} | — | ${project budget} | {🟢/🟡/🔴} |
| Contingency remaining | {pct}% | {actual}% | {after}% | {🟢/🟡/🔴} |
| Overrun tolerance | {pct}% | {actual variance}% | — | {🟢/🔴} |
```

### Step 5.E6.2: Escalation Logic

| Project Budget | Action |
|:--------------:|--------|
| ≤ Auto-approve threshold | Admit without financial escalation |
| Between thresholds | Flag: "Requires sponsor financial sign-off" |
| ≥ Escalation threshold | Block: "Cannot admit without CFO/board approval" |
| Would breach ceiling | Block: "Portfolio ceiling exceeded — must pause/retire another project first" |

### Step 5.E6.3: Funding Release Schedule

For admitted projects, define funding release:

```markdown
## Funding Release

| Project | Total Budget | Release Model | Tranches |
|---------|:-----------:|:-------------:|----------|
| {A} | ${total} | Incremental | ${T1} at start, ${T2} at gate 1, ${T3} at gate 2 |
| {B} | ${total} | Full | ${total} at dispatch |
```

---

## Additional Steps for Stage 8 (after Step 8.4)

### Step 8.E6.1: Financial Governance Dashboard Section

```markdown
## Financial Governance (Extension E6)

### Portfolio Financial Position

| Metric | Value |
|--------|------:|
| Budget ceiling | ${amount} |
| Committed | ${amount} ({pct}%) |
| Remaining capacity | ${amount} ({pct}%) |
| Contingency reserve | ${amount} ({pct}%) — {healthy/depleted} |
| Portfolio-wide overrun | {+/-}${amount} ({pct}%) |

### Guardrail Status

| Guardrail | Threshold | Current | Status |
|-----------|:---------:|:-------:|:------:|
| Portfolio ceiling | ${X} | ${Y} | {🟢 Under / 🟡 Near / 🔴 Breached} |
| Contingency | >{min}% | {actual}% | {🟢/🔴} |
| Overrun tolerance | <{max}% | {actual}% | {🟢/🔴} |

### Portfolio ROI Summary

| Project | Planned ROI | Projected ROI | Status |
|---------|:-----------:|:------------:|:------:|
| {A} | {pct}% | {pct}% | {🟢 Tracking / 🟡 Below / 🔴 Negative} |

**Portfolio aggregate ROI:** {weighted average or total}
**Value at risk:** ${amount} in projects with projected ROI below target

### Burn Rate

| Period | Planned Burn | Actual Burn | Variance |
|--------|:-----------:|:----------:|:--------:|
| This month | ${X} | ${Y} | {+/-} |
| Cumulative | ${X} | ${Y} | {+/-} |

**Projection:** At current burn rate, portfolio exhausts budget by {date} (planned: {date})
```

---

*This extension adds financial rigor to portfolio governance — essential for organizations where budget accountability is formal.*
