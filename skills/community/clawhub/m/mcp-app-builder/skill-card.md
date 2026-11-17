## Description:

Build new MCP Apps (MCP servers with React UI output) using @modelcontextprotocol/ext-apps and the MCP SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollaugo](https://clawhub.ai/user/hollaugo)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to scaffold MCP Apps that expose MCP tools with React-based visual UIs. It provides workflow guidance, required dependency versions, server patterns, UI patterns, and a ready-to-copy template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated MCP app servers may be exposed too broadly if they bind beyond localhost or use unrestricted CORS.

Mitigation: Bind generated servers to loopback by default, restrict CORS to trusted origins, and review network exposure before running outside local development.

Risk: Public tunnels can expose MCP tools and sensitive data if used without access controls.

Mitigation: Avoid public tunnels for sensitive workflows unless authentication, per-tool authorization, and dependency audits are in place.

## Reference(s):

- [MCP App Specification](references/mcp-app-spec.md)
- [MCP App Builder on ClawHub](https://clawhub.ai/hollaugo/skills/mcp-app-builder)
- [Prompt Circle ClawHub Profile](https://clawhub.ai/user/hollaugo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, React, JSON, YAML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify project files for MCP servers, React UI bundles, package configuration, and build scripts.]

## Skill Version(s):

0.1.0 (source: server release metadata and template package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
