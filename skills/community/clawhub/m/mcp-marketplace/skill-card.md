## Description:

Install, configure, and manage MCP servers across OpenClaw, Claude Desktop, Claude Code, and Cursor, including discovery across curated ClawHub entries plus npm and Smithery registries, configuration generation, health checks, updates, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iiizzzyyy](https://clawhub.ai/user/iiizzzyyy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover, install, configure, verify, update, and troubleshoot MCP servers for supported MCP clients. It helps generate configuration snippets and command guidance while keeping authentication values as environment-variable references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated install, update, health-check, Docker, and shell-profile commands can make high-impact changes to the user's environment.

Mitigation: Review each generated command before execution and avoid sudo or global installs unless they are necessary and trusted.

Risk: Unpinned packages or unverified container images may change between runs or pull unexpected code.

Mitigation: Prefer pinned package versions and verified images before installing or updating MCP servers.

Risk: Docker-based MCP servers can introduce host-level risk, especially when privileged mounts or Docker socket access are enabled.

Mitigation: Do not enable Docker socket access or broad host mounts unless the user explicitly accepts the risk and understands the impact.

Risk: Health checks and server launches may expose environment variables to servers that are not trusted.

Mitigation: Run health checks only for servers the user trusts with the relevant environment variables and credentials.

## Reference(s):

- [MCP Marketplace Skill Page](https://clawhub.ai/iiizzzyyy/skills/mcp-marketplace)
- [OAuth Flow Patterns for MCP Servers](references/oauth-patterns.md)
- [MCP Transport Patterns](references/transport-patterns.md)
- [MCP Troubleshooting Guide](references/troubleshooting.md)
- [Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers)
- [Smithery](https://smithery.ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON configuration snippets and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated MCP client configuration entries, install or update commands, compatibility notes, health-check results, and troubleshooting steps.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
