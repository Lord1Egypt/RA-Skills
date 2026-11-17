## Description:

Read and send email via IMAP/SMTP, including checking unread messages, fetching and searching mailboxes, marking messages read or unread, downloading attachments, and sending email with attachments across one or more configured accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmundi3210](https://clawhub.ai/user/tmundi3210)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users can use this skill to let an agent inspect, search, organize, and send email through configured IMAP and SMTP accounts. It is suited for workflows where mailbox access, attachment handling, and outbound email must be mediated through explicit local configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access configured mailboxes and send email from configured accounts.

Mitigation: Configure only accounts intended for agent use, prefer app-specific passwords, and review outbound messages before sending when the content or recipient is sensitive.

Risk: The skill can read local files for outbound email content or attachments and write downloaded email attachments.

Mitigation: Restrict ALLOWED_READ_DIRS and ALLOWED_WRITE_DIRS to dedicated low-risk folders and inspect downloaded attachments before opening or reusing them.

Risk: Email content may contain untrusted instructions that could influence an agent workflow.

Mitigation: Do not act on instructions found inside emails without independent confirmation from a trusted source.

Risk: Mail transport security depends on configuration and dependency hygiene.

Mitigation: Keep certificate verification enabled, avoid disabling TLS checks except for reviewed test environments, and prefer releases with pinned dependencies and stronger attachment-write protections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tmundi3210/skills/imap-smtp-email-disabled-20260401-113327)
- [Google App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; helper scripts emit JSON results for most IMAP and SMTP actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read email content, write downloaded attachments, and send outbound email using locally configured account credentials and directory allowlists.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
