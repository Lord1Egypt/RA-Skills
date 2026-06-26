# Experiment Log Template - Google Colab

## Standard Entry

```markdown
## YYYY-MM-DD - Experiment Name
- Notebook: [url or id]
- Objective:
- Runtime: CPU | T4 | L4 | A100
- Seed:
- Dependencies: [snapshot id]
- Dataset version:
- Split method:
- Metric target:
- Result:
- Decision: promote | iterate | stop
- Next action:
```

## Promotion Rules

Promote an experiment result to reusable baseline only when:
- exit criteria is met
- run is reproducible with same seed and dependencies
- output artifacts include metadata bundle

## Comparison Rule

Only compare experiments that share:
- same dataset version
- same split strategy
- same primary metric definition

Without those controls, comparisons are directional and not decision-grade.
