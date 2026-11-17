## Description:

Microsoft Outlook/Live.com email client via Microsoft Graph API. List, search, read, send, and reply to emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhiramee08b021](https://clawhub.ai/user/abhiramee08b021)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to configure and operate an Outlook/Live.com email CLI for listing, searching, reading, sending, and replying to mail through Microsoft Graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package describes an Outlook CLI but does not include the actual program users are told to run with mailbox credentials and send/reply authority.

Mitigation: Review before installing, confirm the executable source and dependencies, verify requested Microsoft Graph scopes, and understand token storage and revocation before granting mailbox access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abhiramee08b021/skills/outlook-email)
- [Azure Portal](https://portal.azure.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, the requests package, Azure AD app registration, and Microsoft account authentication.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
