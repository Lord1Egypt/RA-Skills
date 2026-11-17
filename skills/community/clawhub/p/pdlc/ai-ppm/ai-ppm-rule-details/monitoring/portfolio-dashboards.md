<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 8: Portfolio Health & Dashboards

**Phase:** Monitoring & Dashboards
**Purpose:** Produce portfolio-level dashboard views that aggregate across all projects — surfacing patterns, risks, and governance triggers that are invisible at the single-project level.

---

## MANDATORY: Stage Sub-Role — Financial Analyst

During THIS stage, ALSO adopt the mindset of a **Financial Analyst**. This does NOT replace your primary role (Portfolio Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Aggregate financial data: total investment, variance, ROI distribution
- Look for patterns: are budget overruns concentrated in one category?
- Think in portfolio terms: "portfolio ROI" not just individual project ROI
- Trend over time: is the portfolio getting healthier or sicker?

### Anti-Patterns for This Stage
- Do NOT present raw data without executive summary
- Do NOT show individual project detail without relating it to the portfolio

### Quality Check
A good dashboard sounds like:
- "Portfolio health: 5/8 on track, 2 at risk, 1 off track. Total investment: $3.2M committed, $2.1M spent (66%). Budget variance: +$180K (5.6% over). Key concern: Projects B and D share the same blocker (API vendor delivery)."

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Health Summary + Progress Tracker only. Text-based tables. |
| **Standard** | All core dashboards (6 views). Tables + executive summary. |
| **Comprehensive** | All dashboards + extension dashboards + trend analysis + recommendations. |

---

## Step-by-Step Execution

### Step 8.1: Generate Executive Summary

Before any detail, produce a 5-bullet executive summary:

```markdown
## Portfolio Executive Summary — {date}

1. **Health:** {N} projects total — {G} on track, {Y} at risk, {R} off track
2. **Financial:** ${total} committed, ${spent} spent ({pct}%), variance {+/-}${amt}
3. **Progress:** Average completion {avg}%, {N} projects ahead/behind schedule
4. **Top Concern:** {the single biggest issue facing the portfolio right now}
5. **Recommendation:** {one governance action to consider}
```

### Step 8.2: Portfolio Health Summary

```markdown
## Portfolio Health Distribution

| Status | Count | Projects | Trend |
|--------|:-----:|----------|:-----:|
| 🟢 On Track | {N} | {list} | {↑↓→} |
| 🟡 At Risk | {N} | {list} | {↑↓→} |
| 🔴 Off Track | {N} | {list} | {↑↓→} |
| ⚪ No Data | {N} | {list} | — |

**Health ratio:** {on-track}/{total} = {pct}%
**Threshold:** Portfolio is healthy if ≥70% are 🟢. Currently: {status}.
```

### Step 8.3: Progress Tracker

```markdown
## Progress Tracker

| # | Project | Priority | Progress | Phase | Schedule | Trend |
|---|---------|:--------:|:--------:|-------|:--------:|:-----:|
| 1 | {A} | #1 | 75% | DLC | On time | → |
| 2 | {B} | #2 | 40% | ADLC | 2w behind | ↓ |
| 3 | {C} | #3 | 10% | PILC | On time | → |

**On schedule:** {N}/{total}
**Behind schedule:** {N}/{total} — average slippage: {weeks}
```

### Step 8.4: Financial Summary

```markdown
## Financial Summary

| Metric | Value |
|--------|-------|
| Total budget (planned) | ${sum} |
| Total spent to date | ${sum} |
| Budget utilization | {pct}% |
| Variance | {+/-}${amount} ({pct}%) |
| Projected total at completion | ${estimate} |

### Per-Project Budget Status

| Project | Planned | Actual | Variance | Status |
|---------|--------:|-------:|:--------:|:------:|
| {A} | $100K | $95K | -$5K | 🟢 |
| {B} | $200K | $240K | +$40K | 🔴 |

**Alerts:**
- {Projects over budget by >10%}
- {Projects with no budget data (stale)}
```

### Step 8.5: Risk Heat Map

```markdown
## Portfolio Risk Heat Map

| Project | Top Risk | Probability | Impact | Score | Category |
|---------|----------|:-----------:|:------:|:-----:|----------|
| {A} | {risk description} | 4 | 5 | 20 | Technical |
| {B} | {risk description} | 3 | 4 | 12 | Resource |

**Concentration:** {N} projects share risks in {category} — systemic exposure
**Highest exposure:** {Project} with risk score {score}
**Cross-project risks:** {risks that affect multiple projects}
```

### Step 8.6: Quality Posture (if data available)

```markdown
## Quality Posture

| Project | Compliance (GCE) | Test Coverage (TGE) | Status |
|---------|:----------------:|:-------------------:|:------:|
| {A} | 85/100 | 78% | 🟢 |
| {B} | 62/100 | 45% | 🟡 |

**Portfolio average compliance:** {avg}/100
**Portfolio average coverage:** {avg}%
**Below threshold:** {projects below minimum acceptable}
```

### Step 8.7: Demand Pipeline (from ILC — same layer, direct read)

```markdown
## Demand Pipeline

| Metric | Value |
|--------|-------|
| Ideas in ILC funnel | {N} |
| Approved & awaiting registration | {N} |
| Conversion rate (approved/submitted) | {pct}% |

**Incoming pressure:** {Low / Medium / High} — {N} projects likely entering portfolio in next quarter
```

### Step 8.8: Governance Triggers

Based on dashboard data, identify if any governance action is needed:

```markdown
## Governance Triggers

| Trigger | Condition | Recommendation |
|---------|-----------|----------------|
| 🔴 Health breach | <70% portfolio on track | Consider rebalancing (Stage 9) |
| 🔴 Budget overrun | >15% over across portfolio | Governance gate review for affected projects |
| 🟡 Stale data | {N} projects with data >2 weeks old | Request fresh roll-up |
| 🟡 Capacity breach | Active demand exceeds supply | Pause lowest-priority project |

**Action needed?** {Yes — recommend Stage 9 / No — portfolio is healthy}
```

### Step 8.9: Render Dashboard File

Compile all sections into `portfolio-dashboards/portfolio-health-dashboard.md` with:
- Generation timestamp
- Data source notation (FLO / manual per project)
- Staleness flags on any data >2 weeks old

### Step 8.10: Present to User

```
📊 Portfolio Dashboard Generated — {date}

Key findings:
• {executive summary bullet 1}
• {executive summary bullet 2}
• {top concern}

Governance triggers: {N active / none}
Full dashboard: portfolio-dashboards/portfolio-health-dashboard.md

Actions available:
(a) Investigate a specific project
(b) Trigger rebalancing (Stage 9) — {if triggers active}
(c) End session — portfolio reviewed
(d) Schedule next review

What would you like to do?
```

---

## Gate

No formal gate — dashboards are informational. However, governance triggers may redirect to Stage 9 (rebalancing) or Stage 5 (governance gate re-decision).

---

## Outputs

| Artifact | Status |
|---|---|
| `portfolio-dashboards/portfolio-health-dashboard.md` | Created/updated |
| `ppm-state.md` | Updated (last review date, next scheduled) |

---

## Extension Dashboards

| Extension | Additional Dashboard |
|---|---|
| E1 (Portfolio Balancing) | Horizon distribution chart, risk-spread analysis |
| E4 (Capacity & Demand) | Resource supply vs. demand, over-allocation alerts |
| E7 (Benefits Aggregation) | Benefits delivered vs. promised, value realization curve |

---

*This stage runs at every health review. The dashboard is the portfolio manager's primary instrument for situational awareness.*
