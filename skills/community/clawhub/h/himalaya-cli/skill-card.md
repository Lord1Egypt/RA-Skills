## Description: <br>
Himalaya CLI helps agents manage email from the terminal over IMAP/SMTP, including listing, reading, writing, replying, forwarding, searching, organizing, and composing messages with MML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cohenyehonatan](https://clawhub.ai/user/cohenyehonatan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and terminal-oriented email users use this skill to configure Himalaya and guide email workflows from configured accounts. It supports command guidance for reading, searching, composing, sending, organizing, exporting, and downloading mailbox content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and using the skill can let an agent operate a configured mailbox, including sending, moving, copying, flagging, exporting, downloading, or deleting mail. <br>
Mitigation: Require explicit user review before actions that send mail, use reply-all, forward messages, attach local files, export content, download attachments, move or copy messages, change flags, or delete anything. <br>
Risk: Email credentials may be exposed if stored as plaintext configuration values. <br>
Mitigation: Prefer app-specific credentials, OAuth, pass, or a system keyring instead of plaintext passwords. <br>
Risk: Attachment and export commands can read from or write to local files and directories. <br>
Mitigation: Review local file paths and destination directories before running attachment, export, or send commands. <br>


## Reference(s): <br>
- [Himalaya Configuration Reference](references/configuration.md) <br>
- [Message Composition with MML](references/message-composition.md) <br>
- [Himalaya project homepage](https://github.com/pimalaya/himalaya) <br>
- [ClawHub skill page](https://clawhub.ai/cohenyehonatan/himalaya-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and TOML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-output command suggestions for Himalaya operations; proposed commands can affect configured email accounts.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
