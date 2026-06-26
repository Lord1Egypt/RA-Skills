## Description: <br>
Read, search, and manage Outlook emails and calendar via Microsoft Graph API. Use when the user asks about emails, inbox, Outlook, Microsoft mail, calendar events, or scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mts-blake-lucas](https://clawhub.ai/user/mts-blake-lucas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to let an agent retrieve, search, organize, send, and delete Outlook mail and view or modify Microsoft 365 calendar events through Microsoft Graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent Microsoft Graph permissions allow reading, modifying, deleting, and sending mail and modifying calendar events. <br>
Mitigation: Install only for accounts where that access is acceptable, confirm sends/deletes/calendar changes manually, and revoke the Azure app or tokens when finished. <br>
Risk: OAuth credentials and refresh tokens are stored under ~/.outlook-mcp. <br>
Mitigation: Keep ~/.outlook-mcp private, retain restrictive file permissions, and avoid using the token-printing command. <br>
Risk: Attachment downloads can write files to the local filesystem. <br>
Mitigation: Save attachments only to a trusted directory and inspect files before opening or reusing them. <br>


## Reference(s): <br>
- [Outlook Manual Setup Guide](references/setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mts-blake-lucas/outlook-365) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown instructions with bash commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local shell scripts, jq, curl, Azure CLI, and Microsoft Graph OAuth credentials stored under ~/.outlook-mcp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog identify v1.3.0 behavior) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
