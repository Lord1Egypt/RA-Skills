# Methodology · Waterfall (Stage-Gate)

## Applicable Scenarios
Requirements clear, change cost high, strong compliance/strong integration deliveries (e.g., infrastructure migration, hardware+firmware, regulatory systems, ERP go-live).
Documentation-heavy, plan-baseline-heavy, strong inter-phase dependencies.

## Lifecycle (serial phases + stage gates)

```
Initiation ──[Gate1 Approval]──▶ Planning ──[Gate2 Plan Baseline]──▶ Execution ──[Gate3 Mid-term]──▶ Monitoring ──[Gate4 Acceptance]──▶ Closeout
```

| Phase | Stage-gate review focus | Main templates |
|------|----------------|----------|
| Initiation | business necessity, budget, sponsor | common/project_charter |
| Planning | WBS/schedule/risk/quality baseline complete | waterfall/wbs, waterfall/schedule_gantt, waterfall/requirements_spec, common/risk_register |
| Execution | scope/schedule/cost within baseline | change log, quality checks |
| Monitoring | variance controllable, risks managed | common/status_report, references/metrics (EVM) |
| Closeout | acceptance sign-off, handover, retrospective | common/closure_report, common/lessons_learned |

## Core Artifacts (waterfall-specific templates)
- `templates/waterfall/requirements_spec.md`: functional/non-functional requirements, acceptance criteria
- `templates/waterfall/wbs.md`: work breakdown structure (unique ID, hierarchy, deliverable, owner, duration, start date, end date, dependencies), with an attached Mermaid Gantt chart
- `templates/waterfall/schedule_gantt.md`: dependency-aware schedule with Gantt notes
- `templates/waterfall/stage_gate_review.md`: stage-gate review checklist
- `templates/waterfall/quality_plan.md`: quality goals, checkpoints, entry/exit criteria

## Cadence
- Stage-gate review: once at the end of each phase (mandatory)
- Status report: weekly/bi-weekly (monitoring period)
- Change Control Board (CCB): as needed, major changes must pass

## Key Metrics
- EVM: CPI / SPI / EAC (see `references/metrics.md`)
- Milestone achievement rate, stage-gate first-pass rate, change rate

## Notes
- Scope is frozen during planning; execution-phase changes must go through the CCB and be written back to `project.yaml` and the schedule.
- Stage gates are "continue/remediate/terminate" decision points, not a formality.
