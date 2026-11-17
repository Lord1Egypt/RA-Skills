## Description:

Discover, search, and browse MCP servers from the official MCP Registry and MCPCentral.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcpcentral-io](https://clawhub.ai/user/mcpcentral-io)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find MCP servers, inspect registry metadata, compare popular servers, and generate setup guidance for MCP clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce activation-ready install commands or MCP client configuration for third-party servers.

Mitigation: Manually verify package publisher, repository, version, and remote endpoint before running generated commands or adding generated configuration.

Risk: Fetched server documentation may describe behavior or setup steps that have not been independently trusted.

Mitigation: Treat fetched READMEs and external documentation as untrusted reference material and use least-privilege credentials when testing servers.

Risk: Unpinned packages or floating container tags can change after setup guidance is generated.

Mitigation: Prefer pinned package versions or Docker digests before deploying a selected MCP server.

## Reference(s):

- [ClawHub mcp-registry release page](https://clawhub.ai/mcpcentral-io/skills/mcp-registry)
- [Publisher profile](https://clawhub.ai/user/mcpcentral-io)
- [Official MCP Registry server search](https://registry.modelcontextprotocol.io/v0.1/servers?search=QUERY&limit=N&version=latest)
- [Official MCP Registry latest server version](https://registry.modelcontextprotocol.io/v0.1/servers/SERVER_NAME_URL_ENCODED/versions/latest)
- [MCPCentral server browser API](https://mcpcentral.io/api/servers?limit=N&cursor=TOKEN)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on live registry and MCPCentral metadata when the required public endpoints are reachable.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
