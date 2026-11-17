## Description:

Mcp Hello World is a minimal MCP server example for calling add and hello_world tools from OpenClaw.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[crystaria](https://clawhub.ai/user/crystaria)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and MCP learners use this skill to run a small stdio MCP server, test simple tool calls, and use the example as a starting point for custom MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a Node.js MCP demo with npm dependencies.

Mitigation: Review package-lock.json, install from the official npm registry or another trusted reviewed source, and update vulnerable dependencies before deployment.

Risk: The documentation and tool messages are Chinese-first.

Mitigation: Review expected tool outputs and translate or adapt documentation for the target user group before rollout.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/crystaria/skills/mcp-hello-world)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text MCP tool responses and Markdown documentation with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The MCP server exposes add and hello_world tools over stdio and requires Node.js.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md changelog, released 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
