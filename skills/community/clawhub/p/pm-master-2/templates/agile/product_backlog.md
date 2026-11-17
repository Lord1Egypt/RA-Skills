# Product Backlog · {{ project.name }}

> The requirement pool is prioritized; the estimation unit may be Story Points. This document is the product's Single Source of Truth for requirements.

## Usage Notes
- Priority guidance: P0 (must-have) > P1 (important) > P2 (normal) > P3 (tentative).
- Status guidance: To Refine / Ready / In Development / Done.
- Epics are used for horizontal grouping, facilitating roadmap planning.

## Backlog List
| ID | Title | Epic | Priority | Estimate | Status |
|----|------|------|--------|------|------|
{{#each backlog}}
| {{this.id}} | {{this.title}} | {{this.epic}} | {{this.priority}} | {{this.estimate}} | {{this.status}} |
{{/each}}

> Tip: Use `sprint_plan.md` to pull high-priority items into the Sprint commitment scope.
