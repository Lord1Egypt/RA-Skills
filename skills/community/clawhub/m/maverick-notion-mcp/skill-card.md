## Description:

Search, read, and update Notion pages, databases, blocks, comments, and workspace content via Notion's hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

External Notion users and developers can use the skill to search and read workspace content, and to update pages, databases, blocks, or comments when they clearly authorize the specific change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Writes can change content visible in the connected Notion workspace.

Mitigation: Confirm the user's intent and the specific target before making each change.

Risk: OAuth credentials persist and stale credentials supplied during setup can overwrite a rotated refresh token.

Mitigation: Protect stored credentials and rerun setup only with freshly issued OAuth credentials.

Risk: The integration retains access until its Notion grant is revoked.

Mitigation: Revoke the integration in Notion when it is no longer needed.

## Reference(s):

- [Notion MCP overview](https://developers.notion.com/guides/mcp/overview)
- [Notion MCP server](https://mcp.notion.com/mcp)
- [mcporter configuration documentation](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md)

## Skill Output:

**Output Type(s):** [Text, API Calls]

**Output Format:** [Natural-language responses and Notion MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can modify Notion workspace content when the user clearly authorizes the specific action.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
