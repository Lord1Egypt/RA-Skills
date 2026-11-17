## Description:

Discover, search, inspect, and generate client configuration for MCP servers across common categories such as filesystem, development, database, web, search, and memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find MCP servers, review server details, and generate starter MCP client configuration for selected servers. It is useful when setting up MCP clients or comparing available server options by category or keyword.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated MCP configurations can later auto-run unpinned third-party server packages with broad access.

Mitigation: Review generated configurations before installing, pin package versions, remove automatic -y installs where possible, and grant MCP servers only the directories, tokens, databases, and memory retention they need.

Risk: Some MCP server configurations require credentials such as GITHUB_TOKEN.

Mitigation: Use least-privileged credentials, store secrets outside shared configuration files, and verify each server's requested access before enabling it.

## Reference(s):

- [MCP Server Registry Reference](references/registry.md)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Official MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [Awesome MCP Servers](https://github.com/appcypher/awesome-mcp-servers)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands support JSON output for programmatic use.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
