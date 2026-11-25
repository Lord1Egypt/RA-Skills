## Description:

Applies coarse-grained service architecture for deployment independence

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and architecture teams use this skill to assess when a service-based architecture fits and to plan service boundaries, contracts, data ownership, and deployment practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changes to a shared database can have cascading effects across services.

Mitigation: Assign explicit ownership to schemas or tables and manage changes with views, replication, or a schema deprecation schedule.

Risk: Weak governance can let service boundaries degrade into a distributed monolith with extra network complexity.

Mitigation: Track coupling and enforce clear ownership of services and data, with stable contracts between services.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-service-based)
- [Archetypes project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown prose with structured recommendations and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
