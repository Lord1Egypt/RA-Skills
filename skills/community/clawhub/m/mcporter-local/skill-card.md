## Description:

Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuliyuan2026](https://clawhub.ai/user/wuliyuan2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate MCP servers and tools from a local mcporter CLI workflow, including inspection, tool calls, authentication, configuration, daemon control, and code generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to contact MCP servers, modify mcporter config or auth state, start daemons, and run local stdio commands.

Mitigation: Require explicit approval before auth, config, daemon, URL, or --stdio commands are run, and review the target server or command before execution.

Risk: The release installs the mcporter npm package without a pinned version.

Mitigation: Pin and review a specific mcporter package version before deployment.

## Reference(s):

- [McPorter homepage](http://mcporter.dev)
- [ClawHub skill page](https://clawhub.ai/wuliyuan2026/skills/mcporter-local)
- [ClawHub publisher profile](https://clawhub.ai/user/wuliyuan2026)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend JSON output for machine-readable mcporter command results.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
