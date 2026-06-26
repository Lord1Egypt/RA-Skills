## Description: <br>
CLI to manage emails via IMAP/SMTP. Use `himalaya` to list, read, write, reply, forward, search, and organize emails from the terminal. Supports multiple accounts and message composition with MML (MIME Meta Language). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guogithubname](https://clawhub.ai/user/guogithubname) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage configured email accounts from a terminal through the Himalaya CLI, including listing, reading, composing, replying, forwarding, organizing messages, and handling attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to operate a real email account, including sending, deleting, forwarding, reply-all, and bulk mailbox changes. <br>
Mitigation: Require explicit user confirmation before any send, delete, forward, reply-all, or bulk mailbox operation. <br>
Risk: Email account credentials may be exposed if stored directly in configuration files. <br>
Mitigation: Use app-specific credentials stored in `pass`, a system keyring, or another secret manager instead of plaintext config values. <br>


## Reference(s): <br>
- [Himalaya project homepage](https://github.com/pimalaya/himalaya) <br>
- [ClawHub skill page](https://clawhub.ai/guogithubname/himalaya-1-0-0) <br>
- [Himalaya Configuration Reference](references/configuration.md) <br>
- [Message Composition with MML](references/message-composition.md) <br>
- [Install Himalaya (brew)](brew:himalaya) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON] <br>
**Output Format:** [Markdown with inline bash, TOML, and email template examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include Himalaya commands that read, send, move, copy, delete, or export email through a configured account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
