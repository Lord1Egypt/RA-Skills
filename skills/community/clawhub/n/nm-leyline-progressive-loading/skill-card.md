## Description:

Implements hub-and-spoke lazy loading to minimize token usage in large skills

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design modular agent skills that load only the guidance relevant to the current task and available token budget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious because it contains many unrelated capabilities and some referenced content was only partially inspected.

Mitigation: Review the unrelated module content, risky publishing and logging guidance, and partially inspected references before installation or use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-leyline-progressive-loading)
- [Plugin details linked in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code examples and module-loading instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selects relevant modules on demand based on task context and token budget.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
