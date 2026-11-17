# Metric Definitions (Metrics)

Unified metric definitions to ensure outputs are comparable across methodologies and Agents.

## 1. Earned Value Management EVM (mainly for waterfall / hybrid, usable for iteration)
From `evm.py`, inputs `pv / ev / ac` (optional `bac`):

| Metric | Formula | Meaning |
|------|------|------|
| PV planned value | —— | budget of work planned to be complete by period end |
| EV earned value | —— | budget of work actually completed |
| AC actual cost | —— | actual spend |
| CPI cost performance | EV/AC | <1 cost overrun |
| SPI schedule performance | EV/PV | <1 behind schedule |
| CV cost variance | EV−AC | negative means overrun |
| SV schedule variance | EV−PV | negative means behind |
| EAC estimate at completion | BAC/CPI | total cost projected at current performance |
| ETC estimate to complete | EAC−AC | —— |
| VAC variance at completion | BAC−EAC | negative means will exceed budget |

**Health flags**: CPI<0.95 → cost overrun; SPI<0.95 → behind schedule; otherwise healthy.

## 2. Agile Metrics (mainly for agile)
| Metric | Meaning | Data |
|------|------|------|
| Velocity | story points completed in one Sprint | `metrics.burndown[].points_done` |
| Burn-down | remaining work declining over time | `metrics.burndown[]` sequence |
| Lead Time | duration from a requirement entering to completion | Kanban flow records |
| WIP | number of work items in progress | Kanban work in progress |
| Flow efficiency | active work time / total duration | Kanban metrics |

## 3. Iteration Metrics (mainly for iteration)
- Iteration burndown (remaining points per iteration)
- Iteration completion rate = completed items / committed items
- Iteration velocity trend (across iterations)

## 4. Program Metrics (program)
- Component health rollup (each project's CPI/SPI red/yellow/green)
- Dependency-blocker count ("blocked" entries in dependency_map)
- Benefits realization rate = verified benefits / planned benefits (`benefits_realization`)

## 5. Health Grading (generic)
- 🟢 Green: CPI≥0.95 and SPI≥0.95 (or stable agile velocity, no blocked dependencies)
- 🟡 Yellow: 0.85≤CPI<0.95 or 0.85≤SPI<0.95
- 🔴 Red: CPI<0.85 or SPI<0.85, or a critical dependency is blocked / a critical risk is unmitigated
