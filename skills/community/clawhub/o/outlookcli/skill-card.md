## Description: <br>
Manage personal Microsoft account email, calendar, contacts, and OneDrive tasks through the m365-cli command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrhah](https://clawhub.ai/user/mrhah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate a personal Outlook.com, Hotmail, or Live account, including mail, calendar, contacts, and OneDrive workflows. It is intended for personal Microsoft accounts, not work or school accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent broad persistent access to personal Microsoft mail, calendar, contacts, and OneDrive data. <br>
Mitigation: Review the Microsoft consent screen, avoid broader scopes than needed, and run m365 logout when persistent access is no longer wanted. <br>
Risk: The skill can send, forward, delete, move, upload, download, share, invite, or force-read content. <br>
Mitigation: Require explicit user confirmation before any send, forward, delete, move, upload, download, share, invite, or --force command. <br>
Risk: Email bodies, attachments, files, and contact data may contain sensitive personal information. <br>
Mitigation: Prefer metadata and summaries in agent output, and only expose full content when the user requests the specific item. <br>


## Reference(s): <br>
- [Command Reference](references/commands.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mrhah/outlookcli) <br>
- [m365-cli npm Package](https://www.npmjs.com/package/m365-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-output conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands often request --json output and can operate on mail, calendar, contacts, and OneDrive resources.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
