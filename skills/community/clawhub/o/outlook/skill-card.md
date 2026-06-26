## Description: <br>
Read, search, and manage Outlook emails and calendar via Microsoft Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jotamed](https://clawhub.ai/user/jotamed) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, employees, and personal users can use this skill to let an agent inspect Outlook mail, send or organize messages, and manage calendar events through Microsoft Graph after OAuth setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Outlook mail, send messages, and create, update, or delete calendar events. <br>
Mitigation: Review every send, delete, bulk mail, and calendar-changing action before execution. <br>
Risk: OAuth credentials and refresh tokens are stored under ~/.outlook-mcp, and the token helper can print an access token. <br>
Mitigation: Treat ~/.outlook-mcp as sensitive credential storage, keep file permissions restrictive, and avoid printing tokens unless necessary. <br>
Risk: The security summary reports an attachment download flaw that can write files outside the expected download location. <br>
Mitigation: Avoid downloading suspicious attachments or writing to sensitive directories until download path handling is fixed. <br>


## Reference(s): <br>
- [Outlook Manual Setup Guide](references/setup.md) <br>
- [Outlook ClawHub Release](https://clawhub.ai/jotamed/outlook) <br>
- [Azure Portal](https://portal.azure.com) <br>
- [Microsoft Graph API Endpoint](https://graph.microsoft.com/v1.0/me) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Microsoft Graph OAuth credentials stored under ~/.outlook-mcp and returns mailbox or calendar data from command-line scripts.] <br>

## Skill Version(s): <br>
1.3.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
