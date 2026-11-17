## Description:

Microsoft Outlook via OAuth 2.0 device code flow and Microsoft Graph API with read-only Mail.Read, Calendars.Read, and Contacts.Read access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredguile](https://clawhub.ai/user/fredguile)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and employees use this skill to authenticate with Microsoft Entra and query Outlook mail, calendar events, contacts, attachments, search results, and profile data through Microsoft Graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and refreshes Microsoft account tokens locally.

Mitigation: Use strong token protection, restrict token file permissions, and install only when local token storage is acceptable.

Risk: The documented hourly cron job can keep access refreshed in the background.

Mitigation: Remove or avoid the cron job unless continuous refresh is truly needed.

Risk: Custom OAuth or Microsoft Graph endpoint configuration can redirect authentication or data requests.

Mitigation: Use only verified Microsoft OAuth and Graph URLs.

Risk: Unpinned Python dependencies can change behavior after installation.

Mitigation: Pin dependencies before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fredguile/skills/outlook-entra)
- [Microsoft OAuth 2.0 device code flow](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code)
- [Microsoft Graph Mail API](https://learn.microsoft.com/en-us/graph/api/user-list-messages)
- [Microsoft Graph Calendar API](https://learn.microsoft.com/en-us/graph/api/user-list-events)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime scripts print text or Markdown and can write downloaded attachment files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Microsoft Entra configuration and locally stored OAuth tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
