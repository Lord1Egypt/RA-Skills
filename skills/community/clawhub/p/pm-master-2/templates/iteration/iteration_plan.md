# Iteration Plan · {{ project.name }}

> Defines this iteration's goal, scope, milestones, and resource investment as the iteration execution baseline.

## Basic Information
- **Iteration Number**: {{ iteration.num }}
- **Iteration Goal**: {{ iteration.goal }}

## Scope
> Requirements and items included for delivery in this iteration.

{{#each iteration.scope}}
- {{this}}
{{/each}}

## Milestones
> Key time nodes and verifiable outputs within the iteration.

{{#each iteration.milestones}}
- {{this}}
{{/each}}

## Resources
> Committed personnel, environments, and other necessary resources.

{{#each iteration.resources}}
- {{this}}
{{/each}}

> Tip: When scope and resources are mismatched, prioritize trimming scope to protect the milestones.
