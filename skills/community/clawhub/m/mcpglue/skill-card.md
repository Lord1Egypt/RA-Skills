## Description: <br>
MCPGlue helps agents connect to external Model Context Protocol servers over standard transports so they can list tools, call tools, access resources, and handle streamed responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxr-666](https://clawhub.ai/user/lxr-666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect OpenClaw agents to MCP servers for database access, GitHub operations, file system workflows, and custom API integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks this release suspicious because MCP calls can expose broad workspace or account access through powerful tokens and raw tool execution. <br>
Mitigation: Install only if you trust the publisher, use dedicated and revocable MCP credentials, keep tokens out of chat, and review write or delete operations before allowing the agent to run them. <br>
Risk: Tool results and side effects depend on the external MCP server selected at runtime. <br>
Mitigation: Use trusted MCP servers, prefer least-privilege credentials and parameters, and inspect tool calls before execution. <br>


## Reference(s): <br>
- [Model Context Protocol documentation](https://modelcontextprotocol.io) <br>
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) <br>
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js for MCP server execution; runtime behavior depends on the selected MCP server and tool parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
