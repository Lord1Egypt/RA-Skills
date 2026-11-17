## Description:

Build, test, and deploy MCP (Model Context Protocol) tools for developer workflows, including TypeScript and Python MCP server scaffolding, tool registration, transport configuration, and testing patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold MCP servers and add database, file-management, API, transport, and local testing patterns for agent-facing tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The examples can create MCP tools with broad filesystem, network, and database access without strong safety boundaries.

Mitigation: Restrict filesystem tools to explicit workspaces, allowlist API destinations, use least-privilege database credentials, and require user confirmation before enabling write or broad data-access tools.

Risk: Generated scaffolds may depend on unpinned or loosely pinned packages.

Mitigation: Pin package versions before production use and review dependency updates as part of release hardening.

Risk: Unvalidated scaffold names or copied tool definitions can introduce fragile or unsafe server behavior.

Mitigation: Validate scaffold names, review generated tool schemas, and test MCP servers locally before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/mcp-dev-toolkit)
- [API Integration MCP Tool Patterns](references/api-tools.md)
- [Database MCP Tool Patterns](references/database-tools.md)
- [File Management MCP Tool Patterns](references/file-tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scaffolded Python or TypeScript MCP server files and tool-pattern examples when applied by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
