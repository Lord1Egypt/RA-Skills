## Description:

Layered n-tier architecture. Use for moderate systems needing presentation, domain, and persistence layers

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to decide when a layered architecture fits and to plan layer boundaries, dependency rules, and enforcement practices for a moderate-sized system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Strict layering can create pass-through code and add latency when features span several layers.

Mitigation: Use a façade to provide a more direct interface where appropriate.

Risk: Bypassing layer rules can weaken architectural boundaries.

Mitigation: Use automated architecture checks and treat violations as build failures or critical code review issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-layered)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown]

**Output Format:** [Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Architecture recommendations and planning deliverables such as layer definitions, dependency diagrams, and enforcement criteria.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
