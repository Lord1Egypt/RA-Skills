## Description: <br>
Microsoft Outlook/Live.com email and calendar client via Microsoft Graph API. List, search, read, send emails. View and create calendar events. Supports device code auth for servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongrebeccahhh-boop](https://clawhub.ai/user/dongrebeccahhh-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to manage Outlook or Live.com mail and calendar workflows from an agent-controlled CLI, including listing, searching, reading, sending, replying, and creating calendar events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests sensitive Microsoft email and calendar access, and the package does not include the declared ./outlook CLI program. <br>
Mitigation: Verify the actual CLI implementation from a trusted source before installing or authenticating; do not enter Microsoft credentials, client secrets, or device-code authentication until that review is complete. <br>
Risk: OAuth tokens are stored locally at ~/.config/outlook-cli/token.json. <br>
Mitigation: Protect the token file with restrictive permissions, do not share or commit it, and revoke Microsoft app access immediately if the token is exposed. <br>
Risk: The documented workflow can send email, reply to messages, and create calendar events. <br>
Mitigation: Require explicit confirmation before sending mail, replying, or creating calendar events, and grant only the minimum Microsoft Graph permissions needed. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/dongrebeccahhh-boop/outlook-email-skill-fixed) <br>
- [Publisher Profile](https://clawhub.ai/user/dongrebeccahhh-boop) <br>
- [Microsoft Azure Portal](https://portal.azure.com) <br>
- [Microsoft Device Login](https://microsoft.com/devicelogin) <br>
- [Microsoft Account App Access](https://account.microsoft.com/privacy/app-access) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, the requests package, Microsoft Graph network access, and Azure AD app registration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
