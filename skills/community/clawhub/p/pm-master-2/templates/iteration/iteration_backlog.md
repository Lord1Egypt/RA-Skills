# Iteration Backlog · {{ project.name }}

> The list of work items within this iteration's scope, including owner, estimate, and status, for daily tracking.

- **Iteration Number**: {{ iteration.num }}

## Work Item List
| ID | Title | Owner | Estimate | Status |
|----|------|--------|------|------|
{{#each backlog}}
| {{this.id}} | {{this.title}} | {{this.owner}} | {{this.estimate}} | {{this.status}} |
{{/each}}

> Tip: Suggested status values: Not Started / In Progress / Blocked / Done.
