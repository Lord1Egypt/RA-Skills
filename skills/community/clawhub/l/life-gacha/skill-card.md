## Description:

A daily gacha skill -- draw a random activity each morning, check in at night, and get a weekly summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoruikun0531](https://clawhub.ai/user/luoruikun0531)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill to add a lightweight daily activity ritual: draw one or more configured activities, record an evening check-in, and generate a weekly markdown summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores daily activity notes locally, which may include personal reflections or routine information.

Mitigation: Confirm the local data directory is acceptable before use, and avoid entering sensitive information in daily check-ins.

Risk: The skill sets up recurring daily and weekly reminders or scheduled tasks.

Mitigation: Approve scheduling only when the draw, check-in, and review cadence is desired, and review or remove scheduled tasks if the routine changes.

Risk: The default card pool may not match a user's preferences, availability, or safety constraints.

Mitigation: Review and customize config.yaml during onboarding before relying on automated daily draws.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational text and markdown journal entries, with shell command invocations for draw, check-in, and review actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local journal files under the skill data directory and can update config.yaml during onboarding.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
