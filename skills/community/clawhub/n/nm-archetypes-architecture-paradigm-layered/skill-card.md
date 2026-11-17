## Description:

Layered n-tier architecture for moderate systems that need presentation, domain, and persistence layers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and architects use this skill to decide when a layered design fits a moderate system and to plan layer responsibilities, dependency direction, and architecture checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Strict layer boundaries can add pass-through code and latency for features that cross several layers.

Mitigation: Use a façade to provide a more direct interface where appropriate.

Risk: Bypassing layer rules can erode the intended architecture.

Mitigation: Make architectural violations fail automated checks or treat them as critical code review issues.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-layered)
- [Project information](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
