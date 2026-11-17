## Description:

Monitors OpenClaw GitHub releases, summarizes and translates release notes into Chinese, and formats notifications for Telegram and Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[00010110](https://clawhub.ai/user/00010110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check OpenClaw release updates, compare versions, translate release notes into Chinese, and prepare update notifications for Telegram or Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notifications may be sent to an unintended Telegram chat or Feishu target if IDs are reused without review.

Mitigation: Confirm Telegram chat ID and Feishu target ownership before enabling automated schedules.

Risk: Automated schedules can distribute unreviewed translated release notes.

Mitigation: Review formatted messages before enabling unattended push workflows.

## Reference(s):

- [OpenClaw latest release API](https://api.github.com/repos/openclaw/openclaw/releases/latest)
- [OpenClaw releases](https://github.com/openclaw/openclaw/releases)
- [Push templates](artifact/references/push-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and notification templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Telegram message length guidance and schedule examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
