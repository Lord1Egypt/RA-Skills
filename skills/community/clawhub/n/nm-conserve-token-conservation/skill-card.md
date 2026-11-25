## Description:

Enforces token quota management at session start with conservation and compression checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can apply the checklist at session start or before large context loads to review quotas, plan context use, consider delegation, and compress or log work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quota checks and workflow steps may not fit every session or available usage source.

Mitigation: Check that the guidance fits the current task and available status information; the skill itself says to skip simple queries and cases already handled by context optimization.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-conserve-token-conservation)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown checklist and session guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are tailored to the current session and task.]

## Skill Version(s):

1.10.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
