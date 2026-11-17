## Description:

Microsoft 365 integration for Outlook, Calendar, Contacts, and OneDrive via Microsoft Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robert-janssen](https://clawhub.ai/user/robert-janssen)

### License/Terms of Use:

ISC

## Use Case:

Developers and agents use this skill to authenticate with Microsoft 365 through Microsoft device code flow and interact with Outlook mail, calendars, contacts, and OneDrive files through Microsoft Graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Microsoft 365 permissions can allow sending mail and modifying calendars, contacts, and OneDrive files.

Mitigation: Use a dedicated low-privilege Microsoft app or account and review the requested grant before approving access.

Risk: Reusable OAuth tokens and Microsoft 365 environment configuration are stored locally.

Mitigation: Protect ~/.openclaw/credentials/ms365.tokens.<account>.json and ms365.env with owner-only permissions, and revoke the Microsoft app grant if token exposure is suspected.

Risk: The security evidence notes inconsistent documentation about token storage.

Mitigation: Confirm the actual credential paths before installation and avoid sharing local credential files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/robert-janssen/skills/microsoft365)
- [Publisher Profile](https://clawhub.ai/user/robert-janssen)
- [Azure App Registrations](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps)
- [Microsoft Device Login](https://microsoft.com/devicelogin)
- [Microsoft Graph API](https://graph.microsoft.com/v1.0)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls]

**Output Format:** [Interactive CLI text output with Microsoft Graph API responses and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Microsoft client and tenant environment configuration.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
