## Description:

Use Model Context Protocol servers to access external tools and data sources, enabling AI agents to discover and execute tools from configured MCP servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunarpulse](https://clawhub.ai/user/lunarpulse)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to connect trusted MCP servers to agents, list available external tools, and call selected tools with schema-validated arguments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can discover and invoke broad capabilities from configured external MCP servers.

Mitigation: Install only for trusted or admin agents, connect only to MCP servers you control or explicitly trust, and restrict which agents can use the mcp tool.

Risk: Connected tools may expose sensitive data access or write operations such as database changes.

Mitigation: Use read-only or least-privilege credentials where possible and require human confirmation for database writes or sensitive data access.

Risk: Diagnostic logs and reports may contain server names, URLs, or operational details.

Mitigation: Review and redact diagnostic output before sharing it publicly or with support.

## Reference(s):

- [Plugin README](README.md)
- [API Reference](docs/API.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Usage Examples](docs/EXAMPLES.md)
- [Real Working Example: kr-legal-search](docs/REAL_EXAMPLE_KR_LEGAL.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and text or JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool behavior depends on the configured MCP servers and the schemas those servers expose.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact package.json and openclaw.plugin.json report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
