## Description:

Discover, search, and manage MCP (Model Context Protocol) servers for finding server information, generating MCP client configurations, and working with the MCP ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanick112](https://clawhub.ai/user/yanick112)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to discover MCP servers, inspect known server details, search by category or keyword, and generate MCP client configuration snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated MCP configurations can later run third-party server packages with access to local files, credentials, databases, browser automation, or external services.

Mitigation: Review each generated server entry before use, verify publishers, pin package versions, restrict filesystem paths and credentials, and use least-privilege accounts for data services.

Risk: Memory and browser automation servers may persist sensitive context or interact with web pages beyond the user's immediate prompt.

Mitigation: Enable those servers only when needed and trusted, and keep their permissions and stored data scoped to the intended task.

## Reference(s):

- [MCP Server Registry Reference](references/registry.md)
- [Model Context Protocol documentation](https://modelcontextprotocol.io/)
- [Official MCP servers repository](https://github.com/modelcontextprotocol/servers)
- [Awesome MCP Servers](https://github.com/appcypher/awesome-mcp-servers)
- [ClawHub skill page](https://clawhub.ai/yanick112/skills/mcp-server-discovery)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports JSON output for list, search, and information commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
