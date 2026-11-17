## Description:

OpenClaw Gateway's built-in scheduler helps agents create one-time reminders, recurring tasks, and background automations with optional delivery to chat channels or webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyclincoln](https://clawhub.ai/user/zyclincoln)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to configure scheduled reminders, recurring background agent tasks, and delivery of task results to chat channels or webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled jobs are persistent automation and may deliver task summaries to chat channels or webhooks.

Mitigation: Review each job prompt, delivery destination, and retention setting before installation; only send sensitive summaries to trusted and secured destinations.

## Reference(s):

- [OpenClaw Cron Jobs Documentation](https://docs.openclaw.ai/automation/cron-jobs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw cron command patterns and job configuration examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
