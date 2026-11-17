# Sprint Retrospective · {{ project.name }}

> Periodic retrospective: capture lessons, surface problems, and follow through on improvement action items.

- **Sprint Number**: {{ sprint.num }}

## What Went Well (Keep)
> Practices worth keeping this period.

{{#each retro.good}}
- {{this}}
{{/each}}

## To Improve (Improve)
> Problems and improvement opportunities surfaced this period.

{{#each retro.improve}}
- {{this}}
{{/each}}

## Action Items
| Action | Owner | Due |
|------|--------|------|
{{#each retro.actions}}
| {{this.item}} | {{this.owner}} | {{this.due}} |
{{/each}}

> Tip: Action items must be tracked to closure at the next Sprint planning meeting.
