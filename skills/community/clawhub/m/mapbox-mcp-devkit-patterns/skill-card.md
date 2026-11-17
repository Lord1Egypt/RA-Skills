## Description:

Integration patterns for using Mapbox MCP DevKit Server in AI coding assistants, including setup, style management, token management, validation workflows, and documentation access through MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and use Mapbox MCP DevKit Server with AI coding assistants. It supports development-time workflows for Mapbox style iteration, scoped token creation, GeoJSON and expression validation, and Mapbox documentation lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an AI assistant development-time access to Mapbox account operations.

Mitigation: Install only when that access is acceptable; prefer the hosted OAuth setup and create narrowly scoped tokens for each environment.

Risk: Token handling and broad account permissions can expose credentials or grant more access than needed.

Mitigation: Pin any npx bridge package, avoid committing MCP configs that contain secrets, never paste real tokens into shared config files, add URL restrictions, and rotate tokens regularly.

## Reference(s):

- [Setup & Installation](references/setup.md)
- [Core Workflows](references/workflows.md)
- [Design Patterns](references/design-patterns.md)
- [Troubleshooting](references/troubleshooting.md)
- [Mapbox MCP DevKit Server](https://github.com/mapbox/mcp-devkit-server)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Mapbox Style Specification](https://docs.mapbox.com/style-spec/)
- [Mapbox API Documentation](https://docs.mapbox.com/api/)
- [Mapbox Token Scopes Reference](https://docs.mapbox.com/api/accounts/tokens/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend Mapbox MCP DevKit tool calls for development-time account operations such as style, token, validation, and documentation workflows.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
