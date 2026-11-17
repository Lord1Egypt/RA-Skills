# Dependency Map · {{ project.name }}

> Maps out dependencies and blockers between components/teams to identify delivery risks early.

## Dependency Diagram

```mermaid
flowchart LR
{{#each dependencies}}
    {{ mid(this.from) }}["{{ mlabel(this.from) }}"] -->|{{ mlabel(this.type) }}| {{ mid(this.to) }}["{{ mlabel(this.to) }}"]
{{/each}}
```

## Dependency List
| ID | From | To | Type | Status | Blocker |
|----|------|------|------|------|----------|
{{#each dependencies}}
| {{this.id}} | {{this.from}} | {{this.to}} | {{this.type}} | {{this.status}} | {{this.blocker}} |
{{/each}}

## Notes
- **Type**: Interface / Data / Resource / Decision, etc.
- **Status**: Planning / In Progress / Completed / Obsolete.
- **Blocker**: Yes / No.

> Tip: Any blocking dependency must have a mitigation and an owner assigned, and be brought into risk tracking.
