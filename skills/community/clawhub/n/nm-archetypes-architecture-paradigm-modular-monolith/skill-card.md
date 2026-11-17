## Description:

Modular monolith with enforced internal boundaries. Use for service-level autonomy without a distributed system

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software architects use this skill to define bounded modules, document their contracts, and enforce internal dependency boundaries in a monolithic codebase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Module boundaries can erode into tightly coupled code.

Mitigation: Make forbidden dependencies fail automated checks and review boundary changes consistently.

Risk: Shared database hotspots can create contention and coupling between modules.

Mitigation: Assign schema ownership and consider restricted views or data replication where appropriate.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-modular-monolith)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown architectural guidance and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides recommendations and example deliverables; implementation depends on the project's language and architecture.]

## Skill Version(s):

1.10.3 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
