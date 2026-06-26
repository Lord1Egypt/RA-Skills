## Description: <br>
Build, secure, and optimize production MCP servers with the TypeScript SDK, covering transports, tool and schema design, error handling, security and OAuth, performance, known SDK bugs, content and structuredContent delivery, v2 migration, MCP Apps, extensions, and the Registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill when building or reviewing production MCP servers and tools. It helps them choose transports, design schemas and tool outputs, handle errors, plan security and OAuth, and migrate across MCP TypeScript SDK versions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example snippets are reference material and may be incomplete for production security needs. <br>
Mitigation: Before using snippets in production, add explicit origin allowlists, authentication, per-tool authorization, user consent for sensitive actions, and careful credential handling. <br>
Risk: The skill discusses paid services, OAuth tokens, sensitive credentials, and cryptographic behavior that can affect production MCP deployments. <br>
Mitigation: Treat the guidance as design input and review credential scope, token audience, authorization boundaries, and deployment controls before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/mcp-best-practices) <br>
- [MCP specification](https://spec.modelcontextprotocol.io) <br>
- [MCP Registry](https://modelcontextprotocol.io/registry/about) <br>
- [Transport Patterns](references/transport-patterns.md) <br>
- [Tool Schema Guide](references/tool-schema-guide.md) <br>
- [Security and Authorization](references/security-auth.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [V2 Migration Guide](references/v2-migration.md) <br>
- [MCP Apps](references/mcp-apps.md) <br>
- [Extensions and Registry](references/extensions-registry.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript examples, shell commands, tables, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; outputs are advisory text and examples for MCP server implementation and review.] <br>

## Skill Version(s): <br>
0.6.0 (source: frontmatter, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
