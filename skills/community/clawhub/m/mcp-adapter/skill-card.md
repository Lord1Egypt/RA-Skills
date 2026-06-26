## Description: <br>
Use Model Context Protocol servers to let agents discover and execute tools from configured external services such as legal databases, APIs, database connectors, and weather services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunarpulse](https://clawhub.ai/user/lunarpulse) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to connect OpenClaw agents to configured MCP servers, inspect available tools, validate tool parameters, and call external services through a single interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured MCP tools may access or change sensitive systems. <br>
Mitigation: Use only trusted MCP servers, prefer HTTPS, apply read-only or least-privilege credentials, and restrict the mcp tool to trusted agents. <br>
Risk: Some MCP tools may write, delete, publish, or query sensitive records. <br>
Mitigation: Require separate approval before enabling or calling tools with write, delete, publish, or sensitive-query capabilities. <br>
Risk: Diagnostic reports or tool outputs may contain sensitive information from connected systems. <br>
Mitigation: Review diagnostic reports and returned tool data before sharing them outside the trusted operating context. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/lunarpulse/mcp-adapter) <br>
- [API Reference](docs/API.md) <br>
- [Configuration Guide](docs/CONFIGURATION.md) <br>
- [Usage Examples](docs/EXAMPLES.md) <br>
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) <br>
- [Real Working Example: kr-legal-search](docs/REAL_EXAMPLE_KR_LEGAL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, configuration, guidance] <br>
**Output Format:** [JSON or text returned through the mcp tool, with Markdown guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the configured MCP servers and each server's advertised tool schemas.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
