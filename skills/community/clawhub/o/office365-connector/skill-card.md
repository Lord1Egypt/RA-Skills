## Description: <br>
Office 365 / Outlook connector for email, calendar, and contacts using resilient OAuth authentication and multi-account Microsoft 365 identity support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tirandagan](https://clawhub.ai/user/tirandagan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, employees, consultants, and automation users use this skill to connect OpenClaw workflows to Microsoft 365 email, calendar, and contacts across one or more accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can request broad delegated Microsoft 365 access for email, calendar, contacts, sending mail, and offline refresh tokens. <br>
Mitigation: Install only when broad Microsoft 365 automation is needed, configure the Azure app with least privilege, and revoke app consent when the skill is no longer used. <br>
Risk: Client secrets, account configuration, and refresh tokens can expose Microsoft account access if copied or stored insecurely. <br>
Mitigation: Do not paste secrets or token output into shared terminals or chats, avoid `node auth.js token`, and protect `~/.openclaw/auth/` and related configuration files. <br>


## Reference(s): <br>
- [Microsoft Graph Azure App Registration Setup Guide](references/setup-guide.md) <br>
- [Microsoft Graph Permissions Reference](references/permissions.md) <br>
- [Office 365 Multi-Account Guide](MULTI-ACCOUNT.md) <br>
- [Microsoft Graph API Documentation](https://learn.microsoft.com/en-us/graph/api/overview) <br>
- [Microsoft Graph Authentication Concepts](https://learn.microsoft.com/en-us/graph/auth/auth-concepts) <br>
- [Microsoft Graph Throttling Guidance](https://learn.microsoft.com/en-us/graph/throttling) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Plain text terminal output, local JSON configuration, and Microsoft Graph API operations from Node.js scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses per-account selection with an optional --account flag and stores account tokens locally.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and CHANGELOG.md, released 2026-02-09) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
