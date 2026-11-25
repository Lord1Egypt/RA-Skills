## Description:

Provides guidance on applying the CQRS and Event Sourcing architecture paradigm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and architects use this skill to assess when CQRS and Event Sourcing fit a system and to plan aggregates, command and event schemas, read projections, consistency expectations, and operational practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Event ordering and replay issues can make operations difficult to diagnose.

Mitigation: Automate replay workflows, route failed events to dead-letter queues, and regularly test resilience with controlled failure drills.

Risk: Eventual consistency can delay read-model updates and confuse users.

Mitigation: Document read-model update service levels and provide immediate feedback from the command side.

Risk: Unplanned event-schema changes can break consumers.

Mitigation: Maintain a schema registry or explicit versioning policy, and gate event versions in CI before they can be emitted.

## Reference(s):

- [Related Night Market archetypes project](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)
- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-cqrs-es)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown]

**Output Format:** [Markdown prose with structured lists and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Architecture planning recommendations; no implementation files are specified.]

## Skill Version(s):

1.10.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
