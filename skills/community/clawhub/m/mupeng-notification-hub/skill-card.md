## Description:

Unified notification hub collecting all skill alerts and delivering by priority

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to collect alert events from multiple skills, classify them by priority, reduce duplicate notifications, and route urgent, important, and informational updates to appropriate channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may surface sensitive security, operational, cost, and Instagram DM-related alerts.

Mitigation: Use sanitized summaries for sensitive sources and avoid exposing raw private alert content in shared channels.

Risk: Urgent or important notifications may be sent to Discord.

Mitigation: Configure the Discord destination carefully and verify that the target channel or DM is appropriate before deployment.

Risk: Notification history is stored and broad activation phrases may expose prior alerts.

Mitigation: Limit access to notification history, define retention expectations, and narrow activation phrases in shared or sensitive environments.

## Reference(s):

- [Notification Hub on ClawHub](https://clawhub.ai/mupengi-bot/skills/mupeng-notification-hub)
- [Mupengism GitHub profile](https://github.com/mupeng)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown summaries, JSON event and history examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized alert summaries, notification routing guidance, duplicate-prevention records, and notification history entries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
