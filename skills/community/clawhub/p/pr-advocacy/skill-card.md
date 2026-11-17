## Description:

Actively monitors pull request status, reviewer feedback, and CI results so an agent can respond to review feedback, update tracking state, and drive reviews toward merge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill to monitor active pull requests, assess review and CI status, respond to maintainer feedback, and keep PR tracking records current.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to make repository changes, change branches, commit work, or push review fixes without clear approval.

Mitigation: Constrain use to specific repositories and pull requests, and require user approval before commits, pushes, or PR comments.

Risk: Persistent tracking or memory updates may write PR state to locations the user did not approve.

Mitigation: Store tracking state only in a user-approved skill-specific location and disable automatic updates to core memory, skills, or workflows.

Risk: Continuous PR monitoring may act on unintended pull requests or stale context.

Mitigation: Scope monitoring to explicit PR numbers, review status before each action, and confirm destructive or externally visible changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linux2010/skills/pr-advocacy)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with inline bash snippets and response templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide repository edits, commits, tracking-list updates, and PR review comments.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
