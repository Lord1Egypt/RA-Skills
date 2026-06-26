## Description: <br>
Discover, search, and manage MCP (Model Context Protocol) servers, including server details and MCP client configuration generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yanick112](https://clawhub.ai/user/Yanick112) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to find MCP servers, inspect available server options, and generate MCP client configuration JSON for selected servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated MCP configurations may enable downstream MCP servers with filesystem, network, database, credential, or persistence behavior. <br>
Mitigation: Review selected server package names before use, enable only required servers, pin versions where practical, restrict filesystem roots, and use least-privilege tokens. <br>
Risk: Memory-oriented MCP servers can retain data across sessions. <br>
Mitigation: Confirm retention behavior before enabling memory servers and avoid storing sensitive data unless persistence is intended. <br>


## Reference(s): <br>
- [MCP Server Registry Reference](references/registry.md) <br>
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/) <br>
- [Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers) <br>
- [Awesome MCP Servers](https://github.com/appcypher/awesome-mcp-servers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Plain text, Markdown command examples, and JSON MCP client configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands support optional JSON output for programmatic use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
