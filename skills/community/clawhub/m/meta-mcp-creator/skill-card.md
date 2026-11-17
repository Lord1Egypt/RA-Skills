## Description:

Use the MCPHero Meta-MCP server inside AI clients such as Claude Desktop and Cursor to create, deploy, and manage MCP servers through the wizard pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arterialist](https://clawhub.ai/user/arterialist)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect the MCPHero Meta-MCP server to MCP-compatible clients and walk through the wizard flow for creating, deploying, and registering hosted MCP servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may send requirements, environment-variable secrets, generated code, and deployed tool behavior to an external hosted service.

Mitigation: Review MCPHero's trust, privacy, retention, and secret-handling practices before installing, and avoid production or long-lived credentials unless they are required.

Risk: Generated or regenerated MCP server code may be used against sensitive systems.

Mitigation: Review generated code before relying on deployed tools, especially for internal APIs or production systems.

Risk: MCP client configuration files may contain bearer tokens in Authorization headers.

Mitigation: Protect client configuration files and use least-privilege, revocable credentials.

## Reference(s):

- [MCPHero](https://mcphero.app)
- [Meta-MCP endpoint](https://api.mcphero.app/mcp/meta/mcp)
- [ClawHub skill page](https://clawhub.ai/arterialist/skills/meta-mcp-creator)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Code, Markdown]

**Output Format:** [Markdown with JSON configuration examples and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP client configuration snippets, wizard tool sequencing, polling guidance, and bearer-token setup guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
