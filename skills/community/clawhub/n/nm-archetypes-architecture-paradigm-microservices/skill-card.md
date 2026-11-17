## Description:

Applies microservices for independent deployment and per-service scaling

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and engineering teams use this skill to assess whether microservices fit their organization and system, then plan service boundaries, platform foundations, and adoption criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Microservices add operational overhead and depend on mature DevOps and SRE practices.

Mitigation: Invest in dedicated platform support and shared tooling for service teams.

Risk: Distributed data ownership can make consistency across services difficult.

Mitigation: Use patterns such as Sagas, make message handling idempotent, and run reconciliation jobs for eventual consistency.

Risk: Overly small services can add communication overhead that outweighs the benefits of distribution.

Mitigation: Give each service a meaningful functional boundary and monitor change coupling to find candidates for merging.

## Reference(s):

- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Architecture guidance, Markdown]

**Output Format:** [Markdown guidance with adoption steps, examples, risks, and exit criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides decision guidance and planning checklists.]

## Skill Version(s):

1.10.3 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
