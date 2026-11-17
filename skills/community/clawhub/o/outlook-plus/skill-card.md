## Description:

Read, search, and manage Outlook emails and calendar via Microsoft Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cristiandan](https://clawhub.ai/user/cristiandan)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers can use this skill to let an agent inspect Outlook inboxes, search messages, send or organize email, and read or manage calendar events after Microsoft account authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, modify, delete, archive, forward, reply to, and send Outlook email, and can read or modify calendar events.

Mitigation: Install only when those Microsoft Graph permissions are acceptable for the target account, and review agent-proposed send, delete, move, and calendar write actions before execution.

Risk: Setup stores client IDs, client secrets, and OAuth access and refresh tokens under ~/.outlook-mcp.

Mitigation: Protect the ~/.outlook-mcp directory, keep credential files private, and rotate or revoke Microsoft app credentials if the local machine or files may be exposed.

Risk: The token helper can print access tokens when explicitly confirmed.

Mitigation: Use token printing only for controlled debugging, avoid logging token output, and treat copied tokens as sensitive credentials.

Risk: Setup guidance may print a curl-to-sudo Azure CLI installation command.

Mitigation: Prefer official package-manager Azure CLI installation instructions before running setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cristiandan/skills/outlook-plus)
- [Publisher profile](https://clawhub.ai/user/cristiandan)
- [Outlook manual setup guide](references/setup.md)
- [Azure CLI installation documentation](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Azure Portal](https://portal.azure.com)
- [Microsoft Graph API endpoint](https://graph.microsoft.com/v1.0/me/mailFolders/inbox)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Azure CLI and jq; uses Microsoft Graph permissions for mail, sending, calendar access, offline refresh, and profile reads; stores OAuth credentials under ~/.outlook-mcp.]

## Skill Version(s):

1.9.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
