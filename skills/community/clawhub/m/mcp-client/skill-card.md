## Description: <br>
Model Context Protocol (MCP) client - connect to tools, data sources and services <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nantes](https://clawhub.ai/user/nantes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to connect an agent to MCP servers, inspect available tools, resources, and prompts, call server-exposed tools, and read server-provided resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted MCP servers can expose tools, resources, or prompts that mislead an agent or access sensitive data. <br>
Mitigation: Use trusted HTTPS server URLs, inspect exposed tools and resources before calling them, and treat server-provided prompts or resources as untrusted unless you control the server. <br>
Risk: API keys used for MCP access can grant broader access than intended. <br>
Mitigation: Use least-privilege API keys and rotate or revoke credentials when access is no longer needed. <br>
Risk: file:// resource URIs can expose files from the MCP server. <br>
Mitigation: Only read file:// resources from servers you control or trust, and review available resources before reading them. <br>


## Reference(s): <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; MCP client commands print JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and the requests library; supports remote MCP server URLs and optional bearer API keys.] <br>

## Skill Version(s): <br>
1.0.3 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
