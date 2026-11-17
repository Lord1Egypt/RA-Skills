# Sprint Burndown Chart · {{ project.name }}

> Compare actual remaining work against the ideal burndown line to assess Sprint progress health.

- **Sprint Number**: {{ sprint.num }}

## Burndown Data
| Date/Day | Remaining Work | Ideal Burndown |
|---------|-----------|----------|
{{#each burndown}}
| {{this.day}} | {{this.remaining}} | {{this.ideal}} |
{{/each}}

## Burndown Chart

```mermaid
xychart-beta
    title "Sprint {{ sprint.num }} Burndown Chart"
    x-axis "Day" [{{ join(burndown, ", ", "day") }}]
    y-axis "Remaining Work" 0 --> {{ burndown.[0].remaining }}
    line [{{ join(burndown, ", ", "remaining") }}]
    line [{{ join(burndown, ", ", "ideal") }}]
```

> Interpretation: if the actual line stays consistently above the ideal line → progress is lagging; if it tracks close to or below → progress is healthy.

> Tip: the estimation unit must be consistent with the Sprint plan (e.g. story points or person-days).
