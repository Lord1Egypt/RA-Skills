## Description:

Maintains an IMAP IDLE connection to monitor new email and send real-time Feishu notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apple133junjiang-a11y](https://clawhub.ai/user/apple133junjiang-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run an IMAP IDLE email listener that records new-mail notifications and forwards sender, subject, and short body-preview details to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive mailbox content and credentials with incomplete disclosure and weak containment.

Mitigation: Use it only with approved mailboxes, avoid hardcoding real secrets in the script, and restrict permissions on generated logs and notification JSON.

Risk: Email excerpts may be forwarded to Feishu.

Mitigation: Confirm that forwarding sender details, subjects, and body previews to Feishu is acceptable, or disable body previews and limit monitored senders or folders.

Risk: The security verdict is suspicious.

Mitigation: Review the skill before installing and scan it before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apple133junjiang-a11y/skills/imap-idle-sender)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets and JSON notification records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write mail notification JSON and log files, and may send Feishu card notifications containing email metadata and short message previews.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
