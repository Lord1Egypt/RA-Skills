## Description: <br>
Microsoft Outlook mail and calendar management skill for the 21Vianet Microsoft 365 environment, supporting mail viewing, sending, search, organization, deletion, calendar event management, and free/busy checks through Microsoft Graph China endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lurking9527](https://clawhub.ai/user/lurking9527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents use this skill to operate a 21Vianet Microsoft 365 mailbox and calendar, including reading and searching messages, sending or replying to mail, creating and deleting calendar events, and checking availability. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify mailbox and calendar data. <br>
Mitigation: Use a dedicated Azure app and mailbox or calendar that the operator is comfortable allowing an agent to modify, and restrict Microsoft Graph permissions where possible. <br>
Risk: OAuth credentials and client configuration are stored locally. <br>
Mitigation: Protect ~/.outlook-microsoft and any .env file with user-only permissions, never commit those files, and revoke tokens or rotate the client secret if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lurking9527/outlook-microsoft) <br>
- [Microsoft Outlook Skill setup guide](references/setup.md) <br>
- [Azure China portal](https://portal.azure.cn/) <br>
- [Microsoft Graph China endpoint](https://microsoftgraph.chinacloudapi.cn) <br>
- [Microsoft China device login](https://microsoft.com/deviceloginchina) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command inputs or outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus OUTLOOK_CLIENT_ID and OUTLOOK_TENANT_ID environment configuration; uses OAuth token state outside the skill output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
