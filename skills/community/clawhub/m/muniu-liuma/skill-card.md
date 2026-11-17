## Description:

Src is a Chinese-oriented SDD (specification-driven development) toolbox that helps agents choose, install, and distribute five step skills for spec writing, architecture design, task planning, implementation guidance, and audit tracing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timeaground](https://clawhub.ai/user/timeaground)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product engineers use this skill as an SDD workflow toolbox index to select the right step skill, understand each skill's required inputs, and distribute the bundled skills into supported agent environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Child skills may read project files to gather architecture context or audit implementation evidence.

Mitigation: Install and run the toolbox only in workspaces where reading project documents and code is acceptable.

Risk: Security evidence notes that spec-writer can use WebFetch while declaring no network access.

Mitigation: Verify or correct the network declaration before deployment, and require user intent before fetching web content.

Risk: Broad trigger phrases can select a step skill when the user's current SDD stage is unclear.

Mitigation: Confirm the available upstream artifact and current workflow stage before invoking a child skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timeaground/skills/muniu-liuma)
- [Toolbox overview](artifact/SKILL.md)
- [spec-writer skill](artifact/skills/spec-writer/SKILL.md)
- [arch-designer skill](artifact/skills/arch-designer/SKILL.md)
- [task-planner skill](artifact/skills/task-planner/SKILL.md)
- [impl-guide skill](artifact/skills/impl-guide/SKILL.md)
- [audit-trace skill](artifact/skills/audit-trace/SKILL.md)
- [Test skeleton specification](artifact/TEST-SKELETON-SPEC.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance, with child skills also supporting structured JSON or CSV outputs when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Child skill outputs may include CONTEXT-CHECK markers, test skeletons, architecture decision records, task lists, or audit status reports.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
