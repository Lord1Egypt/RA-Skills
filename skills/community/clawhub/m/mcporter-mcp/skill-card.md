## Description:

Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratiknarola](https://clawhub.ai/user/pratiknarola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate MCP servers from an agent workflow: listing servers, inspecting schemas, authenticating, editing configuration, running daemons, calling tools, and generating CLI or TypeScript interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to authenticate, edit mcporter configuration, run daemon commands, use stdio commands, and call authenticated or remote MCP tools.

Mitigation: Install only if the mcporter npm package is trusted, review commands before execution, and pay special attention to auth, config, daemon, stdio, and remote-server calls.

## Reference(s):

- [MCPorter homepage](http://mcporter.dev)
- [ClawHub skill page](https://clawhub.ai/pratiknarola/skills/mcporter-mcp)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend JSON output for machine-readable mcporter results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
