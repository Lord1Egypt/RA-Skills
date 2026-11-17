## Description:

Read and send email via IMAP/SMTP, including checking unread messages, fetching content, searching mailboxes, marking messages read or unread, downloading attachments, and sending email through common providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apple133junjiang-a11y](https://clawhub.ai/user/apple133junjiang-a11y)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to let an agent operate a configured IMAP/SMTP mailbox: inspect and search messages, change read state, download selected attachments, and send email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored mailbox credentials can expose an email account if the .env file or environment is shared.

Mitigation: Use a dedicated app password or limited mailbox account, protect or avoid the .env file, and rotate credentials after testing.

Risk: Disabling TLS certificate verification can make mailbox traffic vulnerable outside controlled tests.

Mitigation: Keep IMAP_REJECT_UNAUTHORIZED and SMTP_REJECT_UNAUTHORIZED enabled unless testing in a controlled environment.

Risk: Outbound email and attachments can be sent from the configured account.

Mitigation: Confirm every recipient, message body, and attachment before running SMTP send commands.

Risk: Downloaded attachments can create unsafe or overwritten local files.

Mitigation: Sanitize attachment filenames, choose a controlled output directory, and prevent overwrites before downloading attachments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apple133junjiang-a11y/skills/imap-smtp-email-chinese)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI scripts return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can read mailbox data, change message flags, download attachments, and send email when invoked with configured credentials.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
