## Description:

Read and send email via IMAP/SMTP, including checking unread messages, fetching content, searching mailboxes, marking messages read or unread, downloading attachments, and sending emails with attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welderjustin](https://clawhub.ai/user/welderjustin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to connect an agent to a configured IMAP/SMTP mailbox for reading, searching, managing, and sending email through standard mail servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles full mailbox credentials and can access real mailbox content.

Mitigation: Use provider app passwords or scoped credentials where available, keep .env out of version control, and review the skill before connecting a real mailbox.

Risk: Outbound SMTP support can send email and attachments from the configured account.

Mitigation: Avoid sending sensitive attachments, confirm recipients and content before use, and restrict attachment reads with narrow ALLOWED_READ_DIRS values.

Risk: Disabling certificate verification weakens IMAP or SMTP transport security.

Mitigation: Keep IMAP_REJECT_UNAUTHORIZED and SMTP_REJECT_UNAUTHORIZED enabled unless there is a deliberate, reviewed need for self-signed certificates.

Risk: Attachment download and file attachment features depend on local file boundary configuration.

Mitigation: Set ALLOWED_WRITE_DIRS and ALLOWED_READ_DIRS to narrow directories controlled by the user.

## Reference(s):

- [Gmail App Passwords](https://myaccount.google.com/apppasswords)
- [ClawHub Skill Page](https://clawhub.ai/welderjustin/skills/imap-smtp-email-disabled)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read mailbox content, download attachments, and send outbound email when configured with mailbox credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
