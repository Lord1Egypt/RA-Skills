## Description:

Guides agents to bind scheduled or background OpenClaw work to an explicit user-visible delivery path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonicrang](https://clawhub.ai/user/sonicrang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a task needs a reminder, scheduled check, background completion update, or recurring notification that must reach the user after the current turn.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron-based reminders or recurring checks can continue running until removed.

Mitigation: Review each created cron job, especially recurring checks, and remove jobs that are no longer needed.

Risk: Validation may inspect or modify local OpenClaw cron configuration and send test notifications.

Mitigation: Review cron store changes and confirm test notifications target the intended chat or destination.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sonicrang/skills/openclaw-msg-delivery-guide)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with example OpenClaw cron commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local OpenClaw cron configuration when scheduled delivery must be verified.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
