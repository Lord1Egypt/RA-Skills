## Description: <br>
MCP (Model Context Protocol) utilities and helpers. Tools for connecting, configuring, and managing MCP servers with OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikikari](https://clawhub.ai/user/kikikari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure MCP servers, discover available tools, sync MCP settings with OpenClaw-compatible systems, and invoke MCP tools from code or the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MCP server setup can require sensitive API keys in local configuration or command-line usage. <br>
Mitigation: Review generated configuration, avoid committing API keys, and keep secrets out of shell history. <br>
Risk: Queries and tool inputs sent through remote MCP servers may be visible to those providers. <br>
Mitigation: Connect only approved MCP servers and avoid sending sensitive data unless the provider and use case are approved. <br>
Risk: Synchronizing MCP configuration can change which tools an agent can access. <br>
Mitigation: Back up existing configuration and review server additions before deployment. <br>


## Reference(s): <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>
- [OpenClaw MCP Guide](../docs/websearch-mcp/WEBSEARCH_MCP_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, JSON configuration, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include external MCP server endpoints and API key handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
