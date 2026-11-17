## Description:

Read, search, manage, and send email through standard IMAP and SMTP servers, including mailbox actions and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lroccoon](https://clawhub.ai/user/lroccoon)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can connect a configured mailbox so an agent can check, search, fetch, move, mark, download attachments from, and send email through IMAP/SMTP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses mailbox credentials from environment variables or a local .env file.

Mitigation: Use a dedicated app password or restricted mailbox account, keep .env out of version control, and set file permissions to 0600.

Risk: TLS certificate validation can be disabled for IMAP or SMTP connections.

Mitigation: Keep certificate validation enabled except in a controlled test environment.

Risk: Attachment downloads have scanner-noted gaps around filename sanitization and overwrite protection.

Mitigation: Avoid downloading untrusted attachments until filename sanitization and no-overwrite protections are added; download only expected files into a controlled directory.

Risk: The skill can send, move, and mark messages when configured with real mailbox credentials.

Mitigation: Use least-privilege mailbox credentials and review recipient, mailbox, and UID targets before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lroccoon/skills/imap-smtp-email-plus)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI scripts return JSON and may write downloaded attachments as files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMAP/SMTP host, account, password, TLS, and mailbox settings through environment variables or a local .env file.]

## Skill Version(s):

1.0.0 (source: target metadata, server release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
