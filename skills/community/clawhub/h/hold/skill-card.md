## Description:

Pauses an agent after an unanticipated plan failure, reports the failure and its effects, and asks the user to choose a recovery path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aradmanamnaoon](https://clawhub.ai/user/aradmanamnaoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to stop after an unanticipated failure, review what changed, and choose whether to fix and restart, continue cautiously, or abort.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pausing for a decision can delay automated workflows after an unanticipated failure.

Mitigation: Plan for human review and an escalation path before using the skill in time-sensitive workflows.

Risk: Continuing despite an unanticipated failure can compound incorrect results or side effects.

Mitigation: Review the reported error and side effects, then continue only after the user explicitly selects that option.

## Reference(s):

- [Hold on ClawHub](https://clawhub.ai/aradmanamnaoon/skills/hold)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown report in a code block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the exact error, current state, and three recovery choices; waits for the user's selection.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
