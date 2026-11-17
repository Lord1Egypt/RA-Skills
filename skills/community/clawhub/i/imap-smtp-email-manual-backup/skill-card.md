## Description:

Read, search, fetch, and manage emails via IMAP, and send emails via SMTP with configurable server and authentication settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vthoram](https://clawhub.ai/user/vthoram)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can configure an email account so an agent can read, search, fetch, and manage mailbox contents, download attachments, and send SMTP messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured mailbox access can expose private email and authorize outbound sending.

Mitigation: Use a revocable app password or similarly constrained credentials, restrict .env file permissions, configure only the intended account, and invoke the skill only for explicit email tasks.

Risk: Attachment downloads can write files using filenames supplied by email content.

Mitigation: Avoid downloading untrusted attachments until filename handling is fixed, use a controlled output directory, and inspect downloaded files before opening them.

Risk: Server security evidence reports a suspicious verdict and vulnerable mail dependencies.

Mitigation: Update the mail dependencies and review the security scan guidance before using the skill with sensitive accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vthoram/skills/imap-smtp-email-manual-backup)
- [Publisher profile](https://clawhub.ai/user/vthoram)
- [Skill instructions](artifact/SKILL.md)
- [Package metadata](artifact/package.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command output and concise text or Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include email headers, message snippets, full message text or HTML, attachment file paths, send status, and mailbox state changes.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
