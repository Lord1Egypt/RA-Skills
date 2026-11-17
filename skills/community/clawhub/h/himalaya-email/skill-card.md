## Description:

CLI to manage emails via IMAP/SMTP. Use `himalaya` to list, read, write, reply, forward, search, and organize emails from the terminal. Supports multiple accounts and message composition with MML (MIME Meta Language).

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a configured Himalaya email account from an agent-assisted terminal workflow, including reading, searching, composing, sending, moving, and deleting messages. It is useful when email operations need repeatable CLI commands, configuration examples, and message composition guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help compose, reply to, forward, and send email from a configured account.

Mitigation: Review the selected account, recipients, subject, body, and attachments before allowing any send operation.

Risk: The skill can help move, copy, flag, or delete messages using folder-relative message IDs.

Mitigation: Re-list the current folder and confirm message IDs before allowing move, copy, flag, or delete operations.

Risk: Email configuration may expose credentials if raw passwords are stored directly in the config file.

Mitigation: Prefer pass, system keyring, or app-password command lookups, and avoid storing raw passwords in configuration files.

## Reference(s):

- [Himalaya Configuration Reference](references/configuration.md)
- [Message Composition with MML](references/message-composition.md)
- [Himalaya project homepage](https://github.com/pimalaya/himalaya)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and TOML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Himalaya CLI commands, account configuration snippets, and message composition examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
