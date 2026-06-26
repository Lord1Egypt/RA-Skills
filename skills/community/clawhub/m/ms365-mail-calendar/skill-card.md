## Description: <br>
Microsoft 365 Email & Calendar CLI via Microsoft Graph API. Supports multiple accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[droba07](https://clawhub.ai/user/droba07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent authenticate to Microsoft 365, inspect inbox and search results, read messages, send mail after confirmation, and list or create calendar events for one or more accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Microsoft Graph permissions to read mail, send mail, read and write calendar data, and read basic profile identity. <br>
Mitigation: Install it only where those permissions are acceptable, and confirm before any mail-sending or calendar-changing command. <br>
Risk: The skill stores refreshable Microsoft OAuth tokens on disk. <br>
Mitigation: Use it only on a trusted machine, protect the local credential directory, and delete token files or revoke the Microsoft app when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/droba07/ms365-mail-calendar) <br>
- [Microsoft Graph API endpoint](https://graph.microsoft.com/v1.0) <br>
- [Publisher profile](https://clawhub.ai/user/droba07) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions and terminal text from the Node CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and MICROSOFT_CLIENT_ID; Microsoft tokens are stored per account under ~/.openclaw/credentials/.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
