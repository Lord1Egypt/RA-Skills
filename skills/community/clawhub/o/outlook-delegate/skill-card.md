## Description: <br>
Read, search, and manage Outlook emails and calendar through Microsoft Graph API delegate access, including sending as self, as the mailbox owner, or on behalf of the owner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[87Marc](https://clawhub.ai/user/87Marc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Microsoft 365 operators use this skill to let an assistant account manage another user's Outlook mailbox and calendar through delegated permissions. It supports reading, searching, drafting, sending, replying, forwarding, moving, archiving, deleting, and calendar event management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send messages as another user or on behalf of another user. <br>
Mitigation: Prefer Send on Behalf when transparency matters, choose only one Exchange sending permission, and require human approval before sending messages. <br>
Risk: The skill can modify or delete mailbox and calendar data. <br>
Mitigation: Grant only the Microsoft 365 permissions needed for the workflow and require human approval before deleting, moving, or changing items. <br>
Risk: OAuth access tokens can be exposed if token-printing commands are used carelessly. <br>
Mitigation: Avoid the access-token print command unless explicitly needed, protect the local credential directory, and rotate or revoke credentials when access is no longer required. <br>


## Reference(s): <br>
- [Delegate setup guide](references/setup.md) <br>
- [Outlook Delegate ClawHub page](https://clawhub.ai/87Marc/outlook-delegate) <br>
- [Original Outlook ClawHub skill](https://clawhub.ai/jotamed/outlook) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may call Microsoft Graph and return mailbox, calendar, token, or status data.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
