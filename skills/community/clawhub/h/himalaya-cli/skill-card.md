## Description:

CLI to manage emails via IMAP/SMTP. Use `himalaya` to list, read, write, reply, forward, search, and organize emails from the terminal. Supports multiple accounts and message composition with MML (MIME Meta Language).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cohenyehonatan](https://clawhub.ai/user/cohenyehonatan)

### License/Terms of Use:


## Use Case:

Developers and email power users use this skill to let an agent operate the Himalaya CLI for reading, searching, composing, sending, organizing, and debugging email workflows from the terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email credentials may be exposed if plaintext configuration values are used.

Mitigation: Use pass, system keyring, OAuth token commands, or another secret manager instead of plaintext auth.raw values.

Risk: Destructive email actions can affect the wrong message because Himalaya message IDs are folder-relative.

Mitigation: Re-list the current folder and confirm message IDs, folders, and commands before move, copy, delete, or flag operations.

Risk: Composed messages can be sent to unintended recipients or with unintended attachments.

Mitigation: Verify recipients, headers, message body, and attachment paths before sending.

Risk: Downloaded attachments may come from untrusted messages.

Mitigation: Download attachments only from trusted messages and inspect them before opening or executing.

## Reference(s):

- [Himalaya Configuration Reference](artifact/references/configuration.md)
- [Message Composition with MML](artifact/references/message-composition.md)
- [Himalaya project homepage](https://github.com/pimalaya/himalaya)
- [ClawHub skill page](https://clawhub.ai/cohenyehonatan/skills/himalaya-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON output flags for Himalaya commands when structured email listings are useful.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
