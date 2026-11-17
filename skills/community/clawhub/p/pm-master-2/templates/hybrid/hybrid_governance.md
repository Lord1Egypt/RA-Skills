# Hybrid Governance Map · {{ project.name }}

> In a hybrid delivery model, clarify the methodology, gates, and decision-makers for each part to avoid blurred accountability.

## Governance Map

```mermaid
flowchart TD
{{#each governance.parts}}
    {{ mid(this.name) }}["{{ mlabel(this.name) }}\nMethod: {{ mlabel(this.methodology) }}\nGate: {{ mlabel(this.gate) }}\nDecision: {{ mlabel(this.decision_owner) }}"]
{{/each}}
```

## Governance Map (Parts & Methodology)
| Part | Methodology | Gate / Gating | Decision Owner |
|------|--------|-----------|--------|
{{#each governance.parts}}
| {{this.name}} | {{this.methodology}} | {{this.gate}} | {{this.decision_owner}} |
{{/each}}

## Governance Principles
> Unified governance principles that run across all parts.

{{#each governance.principles}}
- {{this}}
{{/each}}

> Tip: The Gate is a mandatory review point for stage transitions; you may not enter the next stage without passing the gate.
