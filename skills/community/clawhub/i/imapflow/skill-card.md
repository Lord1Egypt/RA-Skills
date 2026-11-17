## Description:

Modern Node.js IMAP client library guidance for email integration, covering authentication, mailbox locking, streaming fetches, async iterators, reconnection strategies, proxy support, and provider-specific configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when building IMAP-backed email features such as connecting to mail providers, fetching and searching messages, managing mailboxes, handling Gmail labels, and monitoring mailboxes with IDLE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad mailbox reads and monitoring of sensitive email content.

Mitigation: Require explicit user confirmation before mailbox reads or IDLE monitoring, and scope operations to the minimum mailbox, query, and message range needed.

Risk: The skill includes mailbox changes such as delete, expunge, move, rename, and flag updates that can be irreversible or disruptive.

Mitigation: Require explicit confirmation before destructive or state-changing mailbox operations, and prefer UID-scoped dry-run previews where practical.

Risk: The skill shows authentication patterns using OAuth tokens and app passwords.

Mitigation: Store credentials in a secrets manager or environment-specific secret store, and avoid hardcoding tokens, app passwords, or proxy credentials in generated code.

## Reference(s):

- [ImapFlow API Reference](references/api_reference.md)
- [IMAP Connection Configurations](references/connection.md)
- [IMAP Search Key Reference](references/searching.md)
- [Proton Mail Bridge](https://proton.me/mail/bridge)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown guidance with JavaScript code examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance for IMAP connection, authentication, search, mailbox management, message fetching, IDLE monitoring, and provider-specific setup.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
