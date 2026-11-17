<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension E4: Portfolio-Level Capacity & Demand

**Stages affected:** 3 (Strategic Alignment), 8 (Portfolio Dashboards)
**Adds:** Supply vs. demand visualization, over-allocation detection, capacity-constrained scheduling

---

## Additional Steps for Stage 3 (after Step 3.5)

### Step 3.E4.1: Build Resource Supply Model

Elicit available capacity from user:

```
Q-{NN}: What resource capacity is available for portfolio execution?

List key teams/roles and their available capacity (FTE or hours/week):

| # | Team / Role | Available FTE | Shared Across | Notes |
|---|-------------|:-------------:|---------------|-------|
| 1 | {e.g., Platform Team} | {N} | {projects using them} | {constraints} |
| 2 | {e.g., Senior Architect} | {N} | {projects} | {part-time} |
| 3 | {e.g., QA Team} | {N} | {projects} | {seasonal} |
```

### Step 3.E4.2: Build Resource Demand Model

From PIP resource plans (read via PILC — same layer, direct), aggregate demand:

```markdown
## Resource Demand (from PIPs)

| Team / Role | Project A | Project B | Project C | Total Demand | Supply | Gap |
|-------------|:---------:|:---------:|:---------:|:------------:|:------:|:---:|
| Platform Team | 3 FTE | 2 FTE | 1 FTE | 6 FTE | 4 FTE | -2 🔴 |
| Senior Architect | 0.5 | 0.5 | 0.3 | 1.3 FTE | 1 FTE | -0.3 🟡 |
| QA Team | 1 | 2 | 1 | 4 FTE | 5 FTE | +1 🟢 |
```

### Step 3.E4.3: Identify Contention

```
⚠️ Capacity contention detected:

| Resource | Demand | Supply | Over-allocated By | Affected Projects |
|----------|:------:|:------:|:-----------------:|-------------------|
| Platform Team | 6 FTE | 4 FTE | 2 FTE (50% over) | A, B, C |

Options:
(a) Sequence projects to avoid overlap (extend timelines)
(b) Reduce scope of lower-priority projects
(c) Acquire additional capacity (hire/contract)
(d) Accept reduced velocity for all (shared allocation)

This contention MUST be resolved before dispatch (Stage 6).
```

---

## Additional Steps for Stage 8 (after Step 8.5)

### Step 8.E4.1: Capacity Dashboard Section

Add to portfolio-health-dashboard.md:

```markdown
## Resource Capacity & Demand (Extension E4)

### Supply vs. Demand

| Team / Role | Supply | Demand | Utilization | Status |
|-------------|:------:|:------:|:-----------:|:------:|
| {team} | {N FTE} | {M FTE} | {pct}% | {🟢≤85% / 🟡86-100% / 🔴>100%} |

### Over-Allocation Alerts

| Resource | Over By | Affected Projects | Risk |
|----------|:-------:|-------------------|------|
| {team} | {N FTE} | {list} | {timeline impact} |

### Capacity Trend

| Period | Avg Utilization | Trend |
|--------|:--------------:|:-----:|
| This month | {pct}% | {↑↓→} |
| Last month | {pct}% | — |
| 3-month trend | {direction} | — |

**Capacity health:** {Sustainable / Strained / Critical}
```

---

*This extension makes resource contention visible BEFORE it becomes a delivery crisis.*
