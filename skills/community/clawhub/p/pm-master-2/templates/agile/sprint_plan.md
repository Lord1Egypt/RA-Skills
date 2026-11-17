# Sprint Plan · {{ project.name }}

> State this Sprint's goal, commitment scope, and task breakdown as the team's execution contract for the period.

## Basic Information
- **Sprint Number**: {{ sprint.num }}
- **Sprint Goal**: {{ sprint.goal }}

## Commitment Scope
> Key scope points committed for delivery this Sprint; must be demonstrable and verifiable.

{{#each sprint.commitment}}
- {{this}}
{{/each}}

## Task Breakdown
| ID | Title | Owner | Estimate |
|----|------|--------|------|
{{#each sprint.tasks}}
| {{this.id}} | {{this.title}} | {{this.owner}} | {{this.estimate}} |
{{/each}}

> Tip: The commitment scope should cover the goal; the sum of task estimates is the baseline effort for this Sprint.
