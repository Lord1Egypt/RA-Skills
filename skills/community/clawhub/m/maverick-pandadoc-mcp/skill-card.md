## Description:

Read and write PandaDoc workspace data via PandaDoc's official hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover PandaDoc's live MCP tool catalog, inspect PandaDoc workspace data, and make explicitly confirmed changes through the connected PandaDoc OAuth account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected PandaDoc OAuth grant lets the agent read or write PandaDoc data within that account's permissions.

Mitigation: Begin with read-only inspection and require explicit user confirmation before write-capable calls or workflow changes.

Risk: Tool arguments and results are sent to PandaDoc's hosted MCP server.

Mitigation: Avoid sending unrelated sensitive content through tool arguments and keep requests limited to the user's PandaDoc task.

Risk: OAuth credentials are stored locally and can become stale or be revoked.

Mitigation: Keep credentials current, avoid reseeding stale tokens, and revoke or reauthorize the PandaDoc grant when access is no longer valid.

## Reference(s):

- [PandaDoc MCP documentation](https://developers.pandadoc.com/docs/getting-started-with-mcp)
- [PandaDoc MCP capability guide](https://developers.pandadoc.com/docs/what-you-can-do-with-pandadoc-mcp)
- [PandaDoc OAuth protected-resource metadata](https://mcp.pandadoc.com/.well-known/oauth-protected-resource/v1/mcp)
- [PandaDoc OAuth authorization-server metadata](https://mcp.pandadoc.com/.well-known/oauth-authorization-server)
- [mcporter configuration documentation](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md)
- [ClawHub skill page](https://clawhub.ai/maverick/skills/maverick-pandadoc-mcp)
- [Publisher profile](https://clawhub.ai/user/maverick)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown instructions with shell command examples and optional JSON tool output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PandaDoc's live MCP catalog as the tool source of truth; results may include PandaDoc workspace records visible to the connected OAuth account.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
