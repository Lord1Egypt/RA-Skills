# OKRs

Universal OKRs from spec-ocas-journal.md apply to all runs.

```yaml
skill_okrs:
  - name: itinerary_feasibility
    metric: fraction of itinerary days passing logistics feasibility checks
    direction: maximize
    target: 0.95
    evaluation_window: 30_runs
  - name: constraint_compliance
    metric: fraction of recommendations satisfying all stated constraints
    direction: maximize
    target: 1.0
    evaluation_window: 30_runs
  - name: availability_honesty
    metric: fraction of uncertain availability items flagged appropriately
    direction: maximize
    target: 1.0
    evaluation_window: 30_runs
```
