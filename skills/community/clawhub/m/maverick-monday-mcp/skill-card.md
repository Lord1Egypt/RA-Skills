## Description:

Search, read, and update Monday.com boards, workspaces, items, updates, and columns through Monday.com’s hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to retrieve Monday.com workspace data and, when clearly requested, create or modify boards, items, updates, and column values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized actions can create, update, archive, or delete Monday.com workspace data.

Mitigation: Require clear user intent before changes; inspect the target board, columns, or item state before acting.

Risk: The hosted MCP server’s available tools and schemas can change.

Mitigation: Review the live tool catalog and schemas before relying on a tool or submitting changes.

Risk: The bearer token grants access to Monday.com data available to its account.

Mitigation: Use least-privilege account access, protect the token, and revoke it when it is no longer needed.

## Reference(s):

- [Monday.com hosted MCP server](https://mcp.monday.com/mcp)
- [mcporter dependency](https://github.com/openclaw/mcporter)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text summaries and structured Monday.com data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify Monday.com workspace data when the user clearly requests it.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
