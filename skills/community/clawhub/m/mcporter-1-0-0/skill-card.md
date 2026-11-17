## Description:

Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mskmz](https://clawhub.ai/user/mskmz)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to operate MCP servers and tools from the mcporter CLI, including listing schemas, calling tools, managing auth and config, running a daemon, and generating CLI or TypeScript client artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can call arbitrary remote or stdio MCP servers and may run local commands through stdio launch strings.

Mitigation: Use trusted MCP endpoints, inspect every --stdio command before execution, and run mcporter in a sandboxed or least-privileged environment.

Risk: The skill can alter authentication and configuration and can invoke create, update, or delete tool calls.

Mitigation: Avoid sending secrets to untrusted servers and require explicit confirmation before state-changing tool calls or auth/config changes.

Risk: The install metadata references an unpinned npm package.

Mitigation: Prefer a reviewed pinned mcporter version for controlled deployments.

## Reference(s):

- [mcporter homepage](http://mcporter.dev)
- [ClawHub skill page](https://clawhub.ai/mskmz/skills/mcporter-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce mcporter command invocations, configuration guidance, and CLI or TypeScript client/type generation instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
