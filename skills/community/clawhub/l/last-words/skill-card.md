## Description:

Auto-deliver final messages to loved ones after 30 days of inactivity for users who want to record a final message, configure email delivery, manage voice messages, or check configuration status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dilboy](https://clawhub.ai/user/dilboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure a local final-message workflow that stores text or audio messages, monitors inactivity, sends warnings, and delivers the configured message by email after the inactivity threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores final messages, audio paths, recipient details, and SMTP credentials locally.

Mitigation: Use a dedicated app password or authorization code, prefer environment-based configuration over chat or command arguments, and protect the local OpenClaw data directory.

Risk: The scheduled inactivity check can send email automatically, including a final message and optional audio attachment.

Mitigation: Test with non-sensitive content first, confirm the recipient address, and review scheduled job configuration before enabling routine checks.

Risk: Debug mode can bypass the normal 30-day inactivity wait and send immediately.

Mitigation: Use debug mode only for controlled testing and disable it after verification.

Risk: Warning messages may be sent to the configured contact address.

Mitigation: Verify warning delivery behavior with test addresses before configuring real recipients.

Risk: Reset behavior is expected to remove stored messages and configuration, but sensitive remnants would be harmful.

Mitigation: After reset, check status and local storage to confirm messages, audio, and credentials were removed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dilboy/skills/last-words)
- [QQ Mail](https://mail.qq.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent guidance can lead to local data storage, scheduled checks, audio handling, and outbound email when the user runs the provided commands.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
