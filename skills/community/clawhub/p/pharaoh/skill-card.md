## Description:

Codebase knowledge graph with 8 development workflow skills. Query architecture, dependencies, blast radius and dead code via MCP. Requires GitHub App installation (read-only repo access) and OAuth authentication. Connects to external MCP server at mcp.pharaoh.so.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xuxdesign](https://clawhub.ai/user/0xuxdesign)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Pharaoh to query a connected codebase's architecture, dependencies, blast radius, and unused code, and to guide planning, implementation, debugging, refactoring, and review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer may overwrite existing Pharaoh skill files and add a Pharaoh MCP entry to OpenClaw configuration.

Mitigation: Back up customized Pharaoh skills, review the installer's changes, and pin the exact npm release before installing.

Risk: Selected repository source is cloned remotely for analysis, and structural metadata is stored by the remote Pharaoh service.

Mitigation: Limit GitHub App access to intended repositories and proceed only if remote analysis and metadata storage fit your requirements.

## Reference(s):

- [Pharaoh documentation](https://pharaoh.so/docs)
- [Pharaoh MCP package on npm](https://www.npmjs.com/package/@pharaoh-so/mcp)
- [Pharaoh GitHub App](https://github.com/apps/pharaoh-so)
- [Pharaoh MCP server](https://mcp.pharaoh.so)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Text or Markdown; may include code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Varies by workflow and codebase query.]

## Skill Version(s):

0.3.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
