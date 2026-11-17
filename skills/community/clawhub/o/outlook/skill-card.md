## Description:

Read, search, and manage Outlook email and calendar data via Microsoft Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jotamed](https://clawhub.ai/user/jotamed)

### License/Terms of Use:


## Use Case:

Employees, external users, developers, and agents use this skill to inspect Outlook inboxes, search and manage messages, send or reply to mail, and view or update calendar events through Microsoft Graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests durable read/write/send access to Outlook mail and read/write access to calendar data.

Mitigation: Install only when that access is acceptable, use the narrowest suitable Microsoft account, and revoke the app registration or tokens when no longer needed.

Risk: Mail, calendar, folder, draft, send, delete, and bulk operations can mutate or disclose user data.

Mitigation: Require explicit confirmation before send, delete, bulk, folder, or calendar mutation commands.

Risk: The token command can print an access token and tokens are persisted for refresh.

Mitigation: Avoid token-printing commands in logged sessions and protect files under ~/.outlook-mcp with user-only permissions.

Risk: Attachment downloads can overwrite local files at the selected output path.

Mitigation: Download attachments only into a safe empty directory and inspect files before opening or moving them.

## Reference(s):

- [Outlook Manual Setup Guide](references/setup.md)
- [ClawHub Skill Page](https://clawhub.ai/jotamed/skills/outlook)
- [Azure Portal](https://portal.azure.com)
- [Microsoft Graph API](https://graph.microsoft.com/v1.0/me)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read or mutate Outlook mail and calendar data after OAuth setup.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
