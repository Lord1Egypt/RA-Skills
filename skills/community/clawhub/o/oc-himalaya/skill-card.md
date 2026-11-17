## Description:

Himalaya CLI for IMAP/SMTP mail: list, read, search, compose, reply, forward, copy, move, delete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the Himalaya CLI through an agent to manage IMAP/SMTP mail, including reading and searching messages, composing and sending replies, and organizing folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mail account credentials could be exposed if raw passwords are stored in configuration or copied into chat or logs.

Mitigation: Use a password manager or system keyring for authentication, and keep secrets out of chat and logs.

Risk: Mail actions can send messages or change and delete mailbox contents.

Mitigation: Check the selected account, recipients, message content, and exact message IDs before sending or changing mail.

## Reference(s):

- [Himalaya project](https://github.com/pimalaya/himalaya)
- [Configuration reference](artifact/references/configuration.md)
- [Message composition with MML](artifact/references/message-composition.md)
- [ClawHub skill page](https://clawhub.ai/hillstreet-ph/skills/oc-himalaya)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, Email messages]

**Output Format:** [Shell commands and configuration guidance, with email content as plain text or MML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, send, move, copy, flag, or delete mail through the configured account]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
