## Description:

Enforces token quota management at session start with conservation and compression checks. Use at the start of every session or before large context loads

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill at session start and before large context loads to check available quota, set a context budget, review whether to delegate or compress work, and log usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quota limits described in the workflow may not match the active agent platform's limits.

Mitigation: Check the active platform's current usage information before setting a task budget.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-conserve-token-conservation)
- [Project homepage listed in ClawHub metadata](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown checklist and session guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
