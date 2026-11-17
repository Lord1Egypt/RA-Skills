## Description:

MCPGlue is an OpenClaw MCP bridge framework that connects agents to external services through Model Context Protocol server processes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxr-666](https://clawhub.ai/user/lxr-666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to list and call tools exposed by trusted MCP servers, supporting workflows such as database access, GitHub API operations, file system interactions, and custom API integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch user-specified local MCP server commands that run with the local user's privileges.

Mitigation: Use the skill only with MCP servers and command arguments that have already been reviewed and trusted.

Risk: The documentation overstates capabilities and gives inconsistent installation instructions.

Mitigation: Align the documentation with the Python implementation and verify dependency installation steps before release.

Risk: Unpinned MCP dependencies can change behavior across installations.

Mitigation: Pin runtime dependencies and review updates before treating the skill as a low-friction install.

## Reference(s):

- [MCP official documentation](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [ClawHub skill page](https://clawhub.ai/lxr-666/skills/mcpglue)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP tool results are emitted as text from the invoked server process.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
