## Description:

Applies coarse-grained service architecture for deployment independence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and architects use this skill to define coarse-grained service boundaries, contracts, data ownership, and deployment practices for multi-team systems that need deployment independence without full microservice autonomy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared database changes can create cascading effects across services.

Mitigation: Use database views or replication, and maintain a formal schema deprecation schedule.

Risk: Weak governance can let services become a distributed monolith with tight coupling and added network complexity.

Mitigation: Track coupling metrics and enforce clear ownership of services and data.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-service-based)
- [Claude Night Market archetypes plugin](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Architecture decision records, Service contracts, Runbooks]

**Output Format:** [Markdown guidance and architecture artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content is tailored to the system and its service boundaries; no fixed artifact template is specified.]

## Skill Version(s):

1.10.3 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
