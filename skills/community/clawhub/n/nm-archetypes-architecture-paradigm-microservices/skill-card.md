## Description:

Applies microservices for independent deployment and per-service scaling

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software architects use this guidance to assess when microservices fit their organization and to plan service boundaries, data ownership, platform capabilities, and resilience practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Microservices add operational overhead and distributed system complexity.

Mitigation: Invest in platform teams and shared tooling to support service teams.

Risk: Maintaining consistency across independently owned service data can be difficult.

Mitigation: Use saga workflows, make message handling idempotent, and run reconciliation jobs for eventual consistency.

Risk: Services split too finely can add communication overhead that outweighs their benefits.

Mitigation: Give each service a meaningful business capability and monitor change coupling to identify services that should be merged.

## Reference(s):

- [ClawHub release](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-microservices)
- [Skill homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown prose and lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Architecture assessment and adoption guidance; no executable output is specified.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
