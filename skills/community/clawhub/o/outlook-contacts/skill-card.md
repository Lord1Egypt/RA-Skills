## Description:

Read and write the signed-in user's Microsoft 365 / Outlook.com personal contacts through Microsoft Graph without mail, file, or directory access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoxh](https://clawhub.ai/user/guoxh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up a contacts-scoped Microsoft Graph device-code login, then list, search, create, update, or delete personal Outlook contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Microsoft access and refresh tokens locally under ~/.outlook-contacts/.

Mitigation: Treat tokens.json as sensitive, keep local file permissions private, and use token.sh clear when finished.

Risk: Contacts.ReadWrite and offline_access grant persistent contact read/write capability to the configured Microsoft app.

Mitigation: Install only if you are comfortable granting those scopes, review the device-code consent, and clear or revoke tokens when access is no longer needed.

Risk: The security summary notes unused calendar helper code.

Mitigation: Review and remove the unused event helper code before broad deployment.

Risk: Write operations can modify or delete personal contact data.

Mitigation: Use the documented dry-run behavior to inspect proposed changes and require explicit apply or typed confirmation before destructive actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoxh/skills/outlook-contacts)
- [Microsoft identity platform endpoint](https://login.microsoftonline.com)
- [Microsoft Graph API endpoint](https://graph.microsoft.com)
- [Microsoft Graph User.Read scope](https://graph.microsoft.com/User.Read)
- [Microsoft Graph Contacts.ReadWrite scope](https://graph.microsoft.com/Contacts.ReadWrite)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; script output may be summary tables, JSON, raw JSON, or simple text lines.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, jq, curl, python3, Microsoft Graph network access, and local token/config files under ~/.outlook-contacts/.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
