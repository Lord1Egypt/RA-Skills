## Description: <br>
Discover, search, and manage Model Context Protocol servers, including retrieving server details and generating MCP client configuration JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to find MCP servers by category or keyword, inspect installation details, and generate starter client configuration for selected servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated MCP configurations can enable downstream servers with sensitive filesystem, database, memory, or API-token access. <br>
Mitigation: Review each selected server before installation, prefer trusted and pinned packages where possible, and grant only the paths, credentials, and services required for the intended task. <br>
Risk: Server lookup and configuration details may become stale as MCP packages and registries change. <br>
Mitigation: Confirm package names, install commands, and server documentation from the referenced MCP sources before deploying generated configurations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/subaru0573/mcp-server-discovery-p) <br>
- [MCP Server Registry Reference](references/registry.md) <br>
- [Model Context Protocol documentation](https://modelcontextprotocol.io/) <br>
- [Official MCP servers repository](https://github.com/modelcontextprotocol/servers) <br>
- [Awesome MCP Servers](https://github.com/appcypher/awesome-mcp-servers) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text and JSON, with shell commands and MCP client configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configuration output may reference downstream MCP servers that require user-scoped filesystem, database, memory, or API-token access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
