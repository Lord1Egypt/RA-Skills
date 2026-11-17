## Description:

Event-driven async messaging

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and architects use this skill to assess when event-driven design fits and to plan event schemas, messaging topology, failure handling, and observability for asynchronous systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Consumers can become implicitly coupled to undocumented event meanings or fields.

Mitigation: Maintain an event catalog or schema registry and lint event structures.

Risk: Stalled consumers and message failures can be difficult to diagnose without observability.

Mitigation: Use distributed tracing, standardized alerts, and dashboards for consumer lag, throughput, schema failures, and dead-letter queues.

Risk: Event-storming workshops can delay decisions when their scope is not managed.

Mitigation: Time-box modeling sessions and focus first on high-value business contexts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-event-driven)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown architecture guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
