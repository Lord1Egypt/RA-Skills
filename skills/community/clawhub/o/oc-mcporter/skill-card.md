## Description:

List, configure, authenticate, call, and inspect MCP servers/tools with mcporter over HTTP or stdio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to discover MCP servers and tools, manage server configuration and authentication, call tools over HTTP or stdio, and generate or inspect CLI and TypeScript interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples use external MCP servers and local paths, which may not fit every environment.

Mitigation: Before running an example, review its server endpoint, command, and local paths for your needs.

Risk: The security scan was partial because two referenced paths were missing, so its evidence is incomplete.

Mitigation: Review the complete release files and rerun the security scan when the missing paths are available.

## Reference(s):

- [Mcporter homepage](http://mcporter.dev)
- [Mcporter ClawHub release](https://clawhub.ai/hillstreet-ph/skills/oc-mcporter)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON]

**Output Format:** [Markdown guidance with shell command examples and optional JSON or TypeScript output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and generated interfaces depend on the selected MCP server and tool.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
