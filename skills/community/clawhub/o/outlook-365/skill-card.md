## Description:

Read, search, and manage Outlook emails and calendar via Microsoft Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mts-blake-lucas](https://clawhub.ai/user/mts-blake-lucas)

### License/Terms of Use:


## Use Case:

Employees and agents use this skill to work with Outlook mail and calendar data, including reading messages, searching mail, sending or drafting email, and viewing or managing events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests read/write access to Outlook mail and calendar, including sending mail and moving or deleting messages.

Mitigation: Install only when that access level is acceptable, review requested Microsoft Graph permissions, and revoke the Azure app when the skill is no longer needed.

Risk: OAuth tokens and client credentials are stored under ~/.outlook-mcp, and the token get command can print an access token.

Mitigation: Protect the credential directory, avoid printing tokens unless necessary, periodically remove stale credentials, and keep file permissions restricted.

Risk: The setup flow includes an Azure CLI installation suggestion that pipes a remote script to sudo bash.

Mitigation: Install Azure CLI through a trusted package manager or verified Microsoft installation path instead of running the curl-to-sudo command.

Risk: Attachment downloads can write files from mailbox attachment names.

Mitigation: Download attachments only from trusted messages and choose an explicit safe output path.

## Reference(s):

- [Outlook Manual Setup Guide](references/setup.md)
- [ClawHub Skill Page](https://clawhub.ai/mts-blake-lucas/skills/outlook-365)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include mailbox, message, attachment, folder, and calendar event data returned through Microsoft Graph operations.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
