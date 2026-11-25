## Description:

Implements hub-and-spoke lazy loading to minimize token usage in large skills

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this guidance to split large, multi-workflow skills into modules and load only the material relevant to a task, while managing context budgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unrelated examples and partially inspected content, which may make the skill's behavior harder to assess.

Mitigation: Hold off on installation until the publisher explains the unrelated examples and the partially inspected content has been reviewed.

Risk: Package or logging examples could send information to an unapproved destination or expose sensitive output.

Mitigation: Before using those examples, confirm the destination is approved and check that outputs contain no sensitive information.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-leyline-progressive-loading)
- [Project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides modular loading patterns and selection guidance; examples may include code and commands.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence; artifact frontmatter lists 1.10.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
