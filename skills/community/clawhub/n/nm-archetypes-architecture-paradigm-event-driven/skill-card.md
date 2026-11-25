## Description:

Event-driven async messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and architects use this skill to assess when event-driven architecture fits and plan asynchronous systems, including event schemas, messaging topology, failure handling, and observability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Consumers may become coupled through undocumented event meanings or fields.

Mitigation: Maintain an event catalog or schema registry and validate event structures.

Risk: Failures across asynchronous consumers can be difficult to diagnose.

Mitigation: Use distributed tracing and standardized alerts, and monitor consumer lag, throughput, schema failures, and dead-letter queue depth.

Risk: Event modeling can become prolonged without clear scope.

Mitigation: Time-box modeling sessions and start with high-value business contexts.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-event-driven)
- [Homepage listed in release metadata](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown]

**Output Format:** [Markdown guidance and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides architecture decision guidance, adoption steps, risks, and operational exit criteria; does not itself implement the architecture.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
