## Description:

Bridge OpenClaw to GroupMe for scheduled messages, announcements, reminders, and automated group messaging workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bgoodwinstudio](https://clawhub.ai/user/bgoodwinstudio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team operators use this skill to configure an OpenClaw agent to send on-demand or scheduled GroupMe bot messages for reminders, announcements, alerts, and recurring team workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A GroupMe token or bot credential could be exposed through loose secrets-file permissions, command lines, logs, or unsafe interpolation.

Mitigation: Use a dedicated low-privilege GroupMe bot token, restrict the secrets file permissions, avoid placing tokens in command lines or logs, and fix the secrets loading and Python interpolation issues before cron use.

Risk: Scheduled or automated outbound messages can send incorrect, premature, or unauthorized announcements to a GroupMe group.

Mitigation: Review message text, target bot configuration, and cron schedules before enabling automation, especially for alerts and recurring operational reminders.

## Reference(s):

- [ClawHub GroupMe skill](https://clawhub.ai/bgoodwinstudio/skills/groupme)
- [GroupMe developer bots](https://dev.groupme.com/bots)
- [GroupMe bot creation](https://dev.groupme.com/bots/new)
- [GroupMe image service](https://dev.groupme.com/docs/image_service)
- [GroupMe API v3](https://api.groupme.com/v3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples; optional shell helper sends JSON payloads to the GroupMe Bot API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, python3, GROUPME_ACCESS_TOKEN, and GROUPME_BOT_ID; GROUPME_GROUP_ID is optional for group discovery.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter reports 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
