## Description:

Microsoft Outlook mailbox and calendar management for 21Vianet Microsoft 365, using Microsoft Graph China endpoints to read, search, send, organize, and delete mail and manage calendar events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lurking9527](https://clawhub.ai/user/lurking9527)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and delegated agents use this skill to manage a 21Vianet Microsoft 365 Outlook mailbox and calendar. It supports inspecting and searching messages, sending or replying to mail, organizing folders, creating or updating events, and checking free/busy status.

### Deployment Geography for Use:

China (21Vianet Microsoft 365 tenants)

## Known Risks and Mitigations:

Risk: The skill requests delegated Microsoft permissions that can read, send, modify, and delete mailbox and calendar content.

Mitigation: Install only for trusted use cases, use a dedicated least-privilege app registration where possible, review destructive or outbound actions before execution, and revoke Microsoft app consent when the skill is no longer needed.

Risk: Microsoft access credentials are stored in local plaintext files under ~/.outlook-microsoft without enforced private permissions.

Mitigation: Protect the credential directory with restrictive permissions or a secure credential store, avoid providing a client secret for device-code flow unless required, and rotate or revoke credentials if the files may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lurking9527/skills/outlook-microsoft)
- [Microsoft Outlook Skill setup guide](references/setup.md)
- [Azure China portal](https://portal.azure.cn/)
- [Microsoft device login for China](https://microsoft.com/deviceloginchina)
- [Microsoft Graph China endpoint](https://microsoftgraph.chinacloudapi.cn)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JSON command arguments and returns single-stream command output.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
