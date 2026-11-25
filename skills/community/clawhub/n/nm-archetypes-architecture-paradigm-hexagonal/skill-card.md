## Description:

Hexagonal ports-and-adapters architecture

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software architects use this skill to decide when to apply ports-and-adapters architecture and to plan domain ports, adapters, contract tests, and dependency boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Too many ports can increase maintenance overhead.

Mitigation: Group related operations into cohesive, higher-level ports around domain aggregates.

Risk: Ports that expose transport details can make the domain dependent on infrastructure concerns.

Mitigation: Use domain-centered data types in port interfaces instead of transport-specific details.

Risk: Adapters can drift from the external systems or schemas they represent.

Mitigation: Regularly validate adapters against their port contracts and current external schemas.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-hexagonal)
- [Archetypes project page](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance and architecture design artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
