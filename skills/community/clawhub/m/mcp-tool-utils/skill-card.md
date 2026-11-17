## Description:

MCP (Model Context Protocol) utilities and helpers for connecting, configuring, and managing MCP servers with OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and manage MCP servers, discover available tools, synchronize OpenClaw-compatible MCP configuration, and run health or latency checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP server examples may involve external providers and API keys.

Mitigation: Use trusted MCP providers, keep API keys in environment variables or a secret manager, and avoid committing configuration files containing credentials.

Risk: API keys embedded in URLs or logs can be exposed accidentally.

Mitigation: Rotate any key accidentally exposed in a URL or logs and prefer configuration patterns that keep secrets out of command history and repository files.

## Reference(s):

- [MCP Tool Utils on ClawHub](https://clawhub.ai/kikikari/skills/mcp-tool-utils)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [OpenClaw MCP Guide](../docs/websearch-mcp/WEBSEARCH_MCP_GUIDE.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with shell, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers MCP server setup, discovery, configuration sync, tool invocation, health checks, and helper utilities.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
