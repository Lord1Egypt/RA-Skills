## Description: <br>
Use Model Context Protocol servers to access external tools and data sources, enabling AI agents to discover and execute tools from configured MCP servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunarpulse](https://clawhub.ai/user/lunarpulse) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to connect agents to configured MCP servers, discover available tools, and call external services such as legal databases, APIs, database connectors, and weather services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured MCP servers may expose broad external tools, including database or API actions, without built-in per-tool approval controls. <br>
Mitigation: Install only with trusted MCP servers, use local or authenticated HTTPS endpoints, apply least-privilege credentials, and require external human approval for writes, account changes, publishing, deletion, and administrative actions. <br>
Risk: Diagnostics or shared configuration can reveal sensitive server URLs, API keys, credentials, or tool outputs. <br>
Mitigation: Keep secrets in environment variables or secure stores and redact logs, configuration, and diagnostic output before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lunarpulse/openclaw-mcp-plugin) <br>
- [README](README.md) <br>
- [API Reference](docs/API.md) <br>
- [Configuration Guide](docs/CONFIGURATION.md) <br>
- [Usage Examples](docs/EXAMPLES.md) <br>
- [Real Korean Legal MCP Example](docs/REAL_EXAMPLE_KR_LEGAL.md) <br>
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to list configured MCP tools, validate tool parameters, call selected tools, parse responses, and present synthesized results.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
