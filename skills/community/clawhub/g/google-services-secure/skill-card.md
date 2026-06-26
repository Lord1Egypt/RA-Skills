## Description: <br>
Helps agents configure OAuth-backed Google Workspace API access for Gmail, Drive, Calendar, Sheets, Docs, and Contacts with setup validation and security-oriented usage guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nelmaz](https://clawhub.ai/user/nelmaz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to set up Google Cloud credentials, run OAuth authentication, validate configuration, and generate Google Workspace API commands for productivity workflows. It is most relevant for controlled environments where operators can review OAuth scopes and write-capable API calls before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents enterprise security controls that may not be enforced by the included shell scripts. <br>
Mitigation: Treat the controls as operator guidance, validate behavior in the target environment, and review commands before granting production access. <br>
Risk: OAuth tokens can be persisted in $HOME/.google-oauth-token, creating sensitive long-lived account access. <br>
Mitigation: Protect the token file, avoid shared environments, rotate or revoke tokens when no longer needed, and use least-privilege OAuth scopes. <br>
Risk: Examples include write-capable Google API calls for email, files, calendars, sheets, and contacts. <br>
Mitigation: Require manual confirmation for write operations and keep GOOGLE_PERMISSION_MODE set to readonly unless a controlled workflow needs broader access. <br>
Risk: Credential setup examples may encourage storing secrets in shell startup files. <br>
Mitigation: Use a managed secret store or ephemeral environment injection instead of persistent shell profiles where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nelmaz/google-services-secure) <br>
- [Security guide](references/security.md) <br>
- [Gmail API reference](https://developers.google.com/gmail/api/reference/rest/) <br>
- [Google Drive API reference](https://developers.google.com/drive/api/reference/rest/v3/) <br>
- [Google Calendar API reference](https://developers.google.com/calendar/api/v3/reference/) <br>
- [Google Sheets API reference](https://developers.google.com/sheets/api/reference/rest/) <br>
- [Google People API reference](https://developers.google.com/people/api/rest/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash, curl, JSON, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google API and OAuth credentials supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
