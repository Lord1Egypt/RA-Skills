## Description:

Read and send email via IMAP/SMTP, including checking unread messages, fetching content, searching mailboxes, marking messages read or unread, and sending email with attachments across multiple accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arry8](https://clawhub.ai/user/arry8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to let an agent interact with configured IMAP and SMTP mailboxes for reading, searching, status changes, attachment handling, and outbound email. It is intended for mailbox automation where users can supply their own provider settings and credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires mailbox credentials and can read, send, and modify email state.

Mitigation: Use dedicated app passwords or authorization codes, scope accounts narrowly, and review command intent before mailbox operations.

Risk: The published artifact includes insecure defaults and credential-handling concerns that could expose mailbox access.

Mitigation: Enable certificate verification, replace bundled account settings, and avoid running setup where terminal output is logged until the password-printing fallback is fixed.

Risk: Attachment and message-body file operations can touch local files if directory allowlists are broad.

Mitigation: Restrict ALLOWED_READ_DIRS and ALLOWED_WRITE_DIRS to the minimum required directories before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arry8/skills/imap-smtp-email-fixed)
- [Google App Passwords](https://myaccount.google.com/apppasswords)
- [Yahoo account security](https://login.yahoo.com/account/security)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read mailbox content, send email, modify message state, and read or write local files within configured allowlists.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
