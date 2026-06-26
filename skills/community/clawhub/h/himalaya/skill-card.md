## Description: <br>
Himalaya is a CLI email skill for managing IMAP/SMTP mailboxes from the terminal, including listing, reading, writing, replying, forwarding, searching, organizing, multi-account workflows, and MML message composition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lamelas](https://clawhub.ai/user/lamelas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure Himalaya and manage mailbox workflows from the terminal, including listing, reading, composing, replying, forwarding, searching, organizing, and exporting email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change a configured mailbox through Himalaya. <br>
Mitigation: Require explicit approval before sending, forwarding, reply-all, deleting, moving, exporting full messages, or downloading attachments. <br>
Risk: Email credentials may be exposed if stored as raw passwords in configuration files. <br>
Mitigation: Prefer app passwords, OAuth, `pass`, or a system keyring, and protect the Himalaya configuration file permissions. <br>


## Reference(s): <br>
- [Himalaya project homepage](https://github.com/pimalaya/himalaya) <br>
- [ClawHub skill page](https://clawhub.ai/lamelas/himalaya) <br>
- [Configuration reference](references/configuration.md) <br>
- [Message composition reference](references/message-composition.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and TOML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local `himalaya` CLI and a configured email account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
