## Description:

Integrates Microsoft 365 with agents through an MCP server for Outlook mail, calendar events, OneDrive files, To-Do tasks, Teams chats, and user profile workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makhatib](https://clawhub.ai/user/makhatib)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this MCP server to let an agent read, create, search, and send Microsoft 365 mail, calendar, file, task, Teams, and user data through Microsoft Graph. It is intended for controlled Microsoft 365 tenants where administrators can scope and monitor the Entra application permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Microsoft Graph application permissions can allow an agent to read or modify sensitive organization data beyond a single user.

Mitigation: Install only in a controlled tenant, reduce Graph permissions to the minimum required scopes, restrict target users, and avoid tenant-wide application access where delegated or read-only permissions are sufficient.

Risk: Tools that send email, create calendar events, create tasks, or send Teams messages can change organizational data or communicate externally.

Mitigation: Require operator approval for send and create actions, log tool use, and review recipients, attendees, chat IDs, and message bodies before execution.

Risk: The MCP server depends on a client secret for Microsoft Graph access.

Mitigation: Protect the client secret, rotate it regularly, avoid committing environment files, and use pinned dependencies or a lockfile before production deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/makhatib/skills/mcp-microsoft365)
- [Azure Portal](https://portal.azure.com)
- [Author website](https://malkhatib.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [MCP text responses, usually JSON for tool results, plus Markdown setup instructions with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool results may include Microsoft 365 content and metadata; file reads are limited to text content returned up to 50000 characters.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, MCP server metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
