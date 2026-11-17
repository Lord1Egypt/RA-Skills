## Description:

Microsoft Outlook email integration for receiving, sending, searching, and managing mail folders through MorphixAI-mediated access to Microsoft Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-leo](https://clawhub.ai/user/paul-leo)

### License/Terms of Use:


## Use Case:

Employees and agents use this skill to manage Microsoft Outlook mailboxes, including reading, searching, sending, replying to messages, and listing folders after an Outlook account is connected through MorphixAI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned external MorphixAI plugin.

Mitigation: Pin or verify the plugin release before installation and install only from a trusted MorphixAI source.

Risk: The connected Outlook account can expose sensitive mailbox read and send capabilities.

Mitigation: Use the least-privileged Outlook connection available, review recipients and message content before send or reply actions, and know how to revoke the connection.

Risk: The MorphixAI API key can authorize mailbox access through the integration.

Mitigation: Store MORPHIXAI_API_KEY securely, rotate it if exposed, and revoke unused keys.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/paul-leo/skills/outlook-email-2)
- [MorphixAI API Keys](https://morphix.app/api-keys)
- [MorphixAI Connections](https://morphix.app/connections)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, tool calls]

**Output Format:** [Markdown with inline shell commands and YAML-like tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Outlook account; examples cover mailbox read, search, send, reply, and folder operations.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
