# AI-PPM Extensions

**Purpose:** Optional capabilities that extend AI-PPM's core 10-stage engine with advanced portfolio management patterns. Extensions are opt-in — they activate only when triggered by user request, portfolio context, or depth level.

---

## Extension Inventory

| ID | Extension | Stage(s) | Trigger | What It Adds |
|:--:|-----------|:--------:|---------|--------------|
| E1 | Portfolio Balancing & Visualization | 4, 8 | "balance" / "portfolio mix" / >10 projects / Comprehensive | Bubble charts, horizon distribution, risk-spread, balance guardrails |
| E2 | What-If Scenario Modeling | 9 | "what-if" / "scenario" / capacity constraints | Scenario comparison, trade-off analysis, impact prediction |
| E3 | Cross-Project Dependency Mapping | 4, 7 | >5 projects / shared resources / "dependencies" | Dependency graph, critical path across projects, blocked-by chains |
| E4 | Portfolio-Level Capacity & Demand | 3, 8 | "capacity" / "resource contention" / >3 shared teams | Supply vs. demand visualization, over-allocation alerts |
| E5 | Investment Themes / Strategic Buckets | 3 | "investment themes" / "strategic buckets" / formal budget categories | Budget allocation by category, distribution enforcement |
| E6 | Financial Governance | 5, 8 | "budget" / "funding" / "financial governance" / enterprise | Lean budget guardrails, funding approval thresholds, portfolio ROI |
| E7 | Benefits Realization Aggregation | 8, 10 | "benefits" / "value realized" / projects completing | Cross-project benefits tracking, value-delivered vs. promised |

---

## How Extensions Work

1. **Opt-in files** (`{name}.opt-in.md`) are scanned at engine start — one paragraph each
2. If trigger condition is met → present activation prompt to user
3. On "yes" → load full detail file (`{name}.md`)
4. Extension adds sub-steps to affected stage(s) — **additive, never replacing** core steps
5. Active extensions recorded in `ppm-state.md` → Active Extensions field

---

## Activation Rules

- Extensions can be activated at any time (not just engine start)
- User can say "activate {extension}" mid-session
- Extensions can be deactivated: "deactivate {extension}" — stops adding sub-steps
- Multiple extensions can be active simultaneously (no conflicts by design)
- At Comprehensive depth, all contextually-relevant extensions auto-suggest

---

## File Structure

```
extensions/
├── README.md                          ← This file
├── portfolio-balancing/
│   ├── portfolio-balancing.opt-in.md  ← Lightweight trigger check
│   └── portfolio-balancing.md         ← Full extension rules
├── what-if-scenarios/
│   ├── what-if-scenarios.opt-in.md
│   └── what-if-scenarios.md
├── dependency-mapping/
│   ├── dependency-mapping.opt-in.md
│   └── dependency-mapping.md
├── capacity-demand/
│   ├── capacity-demand.opt-in.md
│   └── capacity-demand.md
├── investment-themes/
│   ├── investment-themes.opt-in.md
│   └── investment-themes.md
├── financial-governance/
│   ├── financial-governance.opt-in.md
│   └── financial-governance.md
└── benefits-aggregation/
    ├── benefits-aggregation.opt-in.md
    └── benefits-aggregation.md
```
