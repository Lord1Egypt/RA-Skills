## Description:

Hexagonal ports-and-adapters architecture

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to decide when ports-and-adapters architecture fits and to plan domain ports, edge adapters, use cases, contract tests, and dependency rules. It also helps teams avoid unnecessary abstraction for small utilities and prototypes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Too many ports can increase maintenance overhead.

Mitigation: Group related operations into cohesive, higher-level ports, often around domain aggregates.

Risk: Ports can leak transport details and couple the domain to infrastructure.

Mitigation: Keep port interfaces domain-centered and use domain-focused data transfer objects instead of transport-specific fields.

Risk: Adapters can drift out of sync with the external systems they represent.

Mitigation: Regularly validate adapters against their contracts and check that changes such as database migrations still meet the persistence port's expectations.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-hexagonal)
- [Project page from skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown prose with lists and architecture terminology]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
