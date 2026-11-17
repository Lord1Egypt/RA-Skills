## Description:

Production-grade Microsoft 365 MCP server with delegated OAuth, multi-account support, pagination, rate limiting, and 47 tools covering email, calendar, contacts, OneDrive, Teams, tasks, and users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sam2kb](https://clawhub.ai/user/sam2kb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to let an AI client read and manage Microsoft 365 email, calendars, contacts, OneDrive files, Teams chats, tasks, and user information through delegated access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Microsoft 365 content may enter the AI client's context.

Mitigation: Use M365_MCP_READ_ONLY=true when only read access is needed and limit delegated permissions to the required data.

Risk: Send, reply, move, create, update, cancel, decline, and delete tools can change real Microsoft 365 data.

Mitigation: Require explicit user approval for tools that send or modify data, or enable M365_MCP_READ_ONLY=true to disable mutating tools.

Risk: Local OAuth refresh and access tokens are stored as plaintext JSON.

Mitigation: Protect the token directory and revoke Microsoft consent if a token or device is compromised.

## Reference(s):

- [Project README](https://github.com/sam2kb/m365-mcp#readme)
- [ClawHub skill release](https://clawhub.ai/sam2kb/skills/m365-mcp)

## Skill Output:

**Output Type(s):** [API Calls, Text]

**Output Format:** [MCP tool calls and Microsoft 365 data or action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegated account access; enabled write tools can change Microsoft 365 data.]

## Skill Version(s):

1.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
