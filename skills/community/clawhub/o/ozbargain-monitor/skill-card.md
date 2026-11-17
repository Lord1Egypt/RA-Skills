## Description:

Manage OzBargain daily-deal automation in OpenClaw via cron. Use when creating/updating schedules, customizing topic priorities, enabling no-noise filtering, manual-triggering catch-up runs, routing delivery to chat groups, or troubleshooting failed delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laofangxose](https://clawhub.ai/user/laofangxose)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and operate recurring OzBargain deal monitoring in OpenClaw, including scheduling, topic priority tuning, deduplication, delivery routing, manual catch-up runs, and delivery troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring cron jobs can repeatedly send deal summaries to an unintended chat or group if the destination or schedule is configured incorrectly.

Mitigation: Confirm the cron expression, timezone, channel, and destination before enabling or editing the job.

Risk: Troubleshooting probes can send a live message to the configured destination.

Mitigation: Verify the target chat or group before sending any probe message.

Risk: The skill keeps a local dedupe file of sent OzBargain links.

Mitigation: Use a user-specific state path and review local retention expectations before deployment.

## Reference(s):

- [Prompt template](references/prompt-template.txt)
- [ClawHub skill page](https://clawhub.ai/laofangxose/skills/ozbargain-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw and user-provided cron schedule, delivery destination, topic priorities, language, and dedupe state path.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
