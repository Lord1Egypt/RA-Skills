## Description:

Personal email via a configured IMAP/SMTP server for sending, receiving, searching, organizing, scheduling, and receiving push notifications without a third-party email platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polumish](https://clawhub.ai/user/polumish)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an agent interact with a configured mailbox: inspect and search messages, manage folders, rules, and contacts, send or schedule email, and receive IMAP IDLE webhook notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local API can perform broad mailbox actions, including reading, moving, deleting, and sending email.

Mitigation: Run the service under a dedicated unprivileged account and protect access with authentication, a protected socket, or equivalent local controls before enabling it.

Risk: Webhook notifications can forward full message contents when IMAP IDLE is configured.

Mitigation: Set the webhook only to a trusted endpoint and treat webhook traffic as sensitive mailbox data.

Risk: Saving attachments from untrusted messages can write attacker-controlled files to disk.

Mitigation: Avoid saving attachments from untrusted mail until filenames are sanitized and the destination directory is constrained.

Risk: Unpinned runtime dependencies can change install behavior across environments.

Mitigation: Pin dependencies for reproducible installation and review dependency updates before deployment.

## Reference(s):

- [Full API reference](references/api.md)
- [Systemd service setup](references/systemd.md)
- [ClawHub skill listing](https://clawhub.ai/polumish/skills/imap-mail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, configuration guidance]

**Output Format:** [Markdown with inline shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include mailbox summaries, message metadata, command invocations, and API request or response examples.]

## Skill Version(s):

1.5.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
