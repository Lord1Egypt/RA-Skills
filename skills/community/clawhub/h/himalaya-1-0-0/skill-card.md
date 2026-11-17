## Description:

CLI to manage emails via IMAP/SMTP. Use `himalaya` to list, read, write, reply, forward, search, and organize emails from the terminal. Supports multiple accounts and message composition with MML (MIME Meta Language).

This skill is ready for commercial/non-commercial use.

## Publisher:

[guogithubname](https://clawhub.ai/user/guogithubname)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and email power users use this skill to manage mailbox workflows from an agent-operated terminal with Himalaya, including listing, reading, searching, composing, replying, forwarding, moving, copying, deleting, and downloading email content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable an agent to access sensitive email account data and mailbox contents.

Mitigation: Install only when agent access to the email account is intended, and use scoped accounts where possible.

Risk: Email sending, deletion, raw MIME export, and attachment download actions can disclose data or change mailbox state.

Mitigation: Require explicit confirmation before sending mail, deleting messages, exporting raw MIME, or downloading attachments.

Risk: Storing raw IMAP, SMTP, or OAuth credentials in configuration files can expose account secrets.

Mitigation: Prefer pass, system keyring, or another secret manager instead of raw passwords or tokens in config files.

## Reference(s):

- [Himalaya project homepage](https://github.com/pimalaya/himalaya)
- [Himalaya Configuration Reference](references/configuration.md)
- [Message Composition with MML](references/message-composition.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and TOML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account-specific Himalaya commands, email workflow guidance, and configuration examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
