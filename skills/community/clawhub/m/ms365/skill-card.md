## Description:

Access and manage Microsoft 365 email, calendar, OneDrive files, To Do tasks, and contacts through Microsoft Graph API tooling with authentication support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cvsloane](https://clawhub.ai/user/cvsloane)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to let an agent authenticate with Microsoft 365, inspect account data, and perform common productivity actions such as reading email, managing calendar events, browsing OneDrive files, and creating tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can request broad Microsoft 365 account access across email, calendar, files, tasks, and contacts.

Mitigation: Use a least-privilege Microsoft app registration and prefer read-only mode unless write access is required.

Risk: The skill runs an npm dependency at runtime, and the security summary flags the dependency as unpinned.

Mitigation: Pin or preinstall @softeria/ms-365-mcp-server from a trusted version before deployment.

Risk: Write-capable actions can send email, post messages, delete data, or create and update events and tasks.

Mitigation: Require explicit user confirmation before executing write or destructive Microsoft 365 actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cvsloane/skills/ms365)
- [@softeria/ms-365-mcp-server npm package](https://www.npmjs.com/package/@softeria/ms-365-mcp-server)
- [Softeria ms-365-mcp-server repository](https://github.com/Softeria/ms-365-mcp-server)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-formatted command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Microsoft 365 account data returned by the CLI or MCP server, depending on the requested operation and granted permissions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
