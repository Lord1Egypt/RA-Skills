# Macro–Micro Mapping · {{ project.name }}

> Align macro milestones with micro iterations to ensure short-term delivery continuously supports long-term goals.

## Macro–Micro Alignment Diagram

```mermaid
flowchart LR
{{#each map}}
    {{ mid(this.macro_milestone) }}["{{ mlabel(this.macro_milestone) }}"] -->|{{ mlabel(this.alignment_status) }}| {{ mid(this.micro_iteration) }}["{{ mlabel(this.micro_iteration) }}"]
{{/each}}
```

## Mapping Table (Macro ↔ Micro)
| Macro Milestone | Micro Iteration | Alignment Status |
|-----------|---------|----------|
{{#each map}}
| {{this.macro_milestone}} | {{this.micro_iteration}} | {{this.alignment_status}} |
{{/each}}

> Tip: Alignment status suggested values — Aligned / Deviating / Disconnected; a deviation should trigger a governance review.
