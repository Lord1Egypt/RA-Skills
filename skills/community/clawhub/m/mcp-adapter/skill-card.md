## Description:

MCP Adapter helps agents discover and execute tools from configured Model Context Protocol servers to access external tools and data sources such as legal databases, APIs, database connectors, and weather services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunarpulse](https://clawhub.ai/user/lunarpulse)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to let agents list and call tools exposed by configured MCP servers, then synthesize the returned data for user-facing workflows. It is most relevant when an agent needs controlled access to external services such as legal search, databases, APIs, or weather tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents receive broad access to tools exposed by configured external MCP servers.

Mitigation: Install only trusted MCP servers, restrict which agents can access the mcp tool, and require explicit confirmation before writes, deletes, purchases, messages, or other consequential actions.

Risk: Configured MCP servers may expose production data sources or administrative actions through generic query/action interfaces.

Mitigation: Use read-only or least-privilege service accounts and avoid exposing production databases or administrative tools unless the deployment has appropriate controls.

Risk: Transport and dependency posture may be unsuitable for production if endpoints or dependencies are not maintained.

Mitigation: Prefer HTTPS endpoints for production deployments and update flagged dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lunarpulse/skills/mcp-adapter)
- [README](README.md)
- [API Reference](docs/API.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Usage Examples](docs/EXAMPLES.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- [Real Working Example: kr-legal-search](docs/REAL_EXAMPLE_KR_LEGAL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool-call examples and shell or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured MCP tool calls and JSON responses depending on the configured servers.]

## Skill Version(s):

0.1.0 (source: release metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
