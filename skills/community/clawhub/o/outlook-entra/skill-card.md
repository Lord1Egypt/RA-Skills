## Description: <br>
Provides read-only Microsoft Outlook access through OAuth 2.0 device code flow and Microsoft Graph for mail, calendar events, contacts, profile data, and attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredguile](https://clawhub.ai/user/fredguile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure an agent to authenticate to a Microsoft Entra application and read Outlook mail, calendar events, contacts, profile data, and attachments through Microsoft Graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can maintain durable access to Microsoft account data through refresh tokens. <br>
Mitigation: Grant only the Graph scopes required for the intended workflow, monitor the Entra app consent, and revoke tokens when the skill is no longer needed. <br>
Risk: OAuth tokens are stored locally and encryption depends on TOKEN_FILE_KEY being configured. <br>
Mitigation: Set TOKEN_FILE_KEY, restrict permissions on the token file, and avoid enabling hourly cron refresh unless persistent access is required. <br>
Risk: Downloaded Outlook attachments may introduce unsafe files into the local environment. <br>
Mitigation: Download attachments only to a dedicated safe directory and inspect or scan files before opening or processing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fredguile/outlook-entra) <br>
- [Microsoft OAuth 2.0 device code flow](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code) <br>
- [Microsoft Graph Mail API](https://learn.microsoft.com/en-us/graph/api/user-list-messages) <br>
- [Microsoft Graph Calendar API](https://learn.microsoft.com/en-us/graph/api/user-list-events) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts return plain text or Markdown-formatted Outlook data and downloaded attachment files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Microsoft Entra app configuration and local OAuth token storage; read-only Graph scopes are documented for mail, calendar, and contacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
