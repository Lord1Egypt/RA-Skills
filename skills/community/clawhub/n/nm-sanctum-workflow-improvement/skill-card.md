## Description:

Evaluates and improves skills, agents, commands, and hooks after a workflow slice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after a command or short work session that felt slow, confusing, repetitive, or fragile. It helps them review workflow assets, plan bounded improvements, validate changes, and record lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that workflow observations may be directed to an external GitHub repository without a clear approval step.

Mitigation: Review the issue contents and destination, and require approval before creating external issues.

Risk: The security assessment says analysis of the issue creation module was incomplete, so its full behavior has not been established.

Mitigation: Inspect the complete issue creation behavior and destination settings before using that module.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-sanctum-workflow-improvement)
- [Project homepage listed in ClawHub metadata](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)
- [Auto issue creation module](artifact/modules/auto-issue-creation.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with workflow steps, recommendations, issue templates, metrics, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed changes to workflow assets and GitHub issue content.]

## Skill Version(s):

1.10.3 (source: skill frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
