## Description:

Build, harden, and debug production MCP servers with the TypeScript SDK. Use when writing or reviewing an MCP server - transports, tool schemas, errors, OAuth, token bloat, SDK migrations, MCP Apps, Registry. Assumes a server already exists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building or reviewing an existing MCP server use this reference to make implementation decisions and improve its transports, tool schemas, authentication, error handling, and deployment security.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands and package suggestions may introduce vulnerabilities or unintended changes when applied to a project.

Mitigation: Pin and review packages before running commands, and inspect proposed codemod changes before applying them.

Risk: An optional tunnel can expose a development MCP server beyond its intended audience.

Mitigation: Expose only a protected test server through the tunnel.

Risk: Payment examples may extend beyond the intended integration scope.

Mitigation: Keep payment integration within the scope intended for the application.

## Reference(s):

- [ClawHub release](https://clawhub.ai/tenequm/skills/mcp-best-practices)
- [Project homepage](https://github.com/tenequm/skills/tree/main/skills/mcp-best-practices)
- [MCP specification](https://modelcontextprotocol.io/specification/latest)
- [TypeScript SDK documentation](https://ts.sdk.modelcontextprotocol.io/)
- [MCP Registry](https://modelcontextprotocol.io/registry/about)
- [Transport patterns](references/transport-patterns.md)
- [Tool schema guide](references/tool-schema-guide.md)
- [Security and authentication](references/security-auth.md)
- [Error handling](references/error-handling.md)
- [MCP specification 2026-07-28](references/spec-2026-07-28.md)
- [SDK v2 migration](references/v2-migration.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions, Shell commands]

**Output Format:** [Markdown with TypeScript and shell code blocks, decision tables, and examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advice is version-sensitive and varies with the MCP specification revision, SDK version, transport, and client behavior.]

## Skill Version(s):

1.3.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
