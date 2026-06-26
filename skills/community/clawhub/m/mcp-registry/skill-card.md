## Description: <br>
Discover, search, and browse MCP servers from the official MCP Registry and MCPCentral, including server specs and setup configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcpcentral-io](https://clawhub.ai/user/mcpcentral-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to find MCP servers, inspect installation metadata, compare registry and MCPCentral enrichment data, and generate MCP client configuration snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommended MCP servers and generated install commands may point to third-party code, packages, remotes, or token scopes outside this skill's control. <br>
Mitigation: Verify the publisher, repository, package name, remote endpoint, requested permissions, and any token scopes before running generated npx, uvx, or docker commands or adding generated config to an MCP client. <br>
Risk: MCPCentral enrichment data may lag authoritative registry metadata. <br>
Mitigation: Use the official MCP Registry as the authoritative source for version, package, transport, and environment variable metadata, and treat MCPCentral metrics as supplemental. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mcpcentral-io/mcp-registry) <br>
- [Official MCP Registry API](https://registry.modelcontextprotocol.io/v0.1/servers) <br>
- [MCPCentral Servers API](https://mcpcentral.io/api/servers) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public registry data and generated MCP client configuration snippets; no authentication is required for the documented registry endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
