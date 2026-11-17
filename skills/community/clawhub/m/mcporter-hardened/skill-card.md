## Description:

Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate MCP servers and tools through the mcporter CLI, including server discovery, authentication, configuration, direct tool calls, daemon management, and CLI or TypeScript generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the mcporter npm CLI package, which is not pinned in the install metadata.

Mitigation: Pin or separately review the mcporter package before installation, and install only when the package and connected MCP servers are trusted.

Risk: mcporter can invoke powerful MCP operations, including destructive remote actions, when the user directs it.

Mitigation: Confirm the server, tool, and target before destructive operations such as delete, remove, revoke, or terminate.

Risk: MCP tool responses may contain sensitive data that could be exposed if redirected or piped to network commands.

Mitigation: Keep mcporter output local, avoid piping it to network-transmitting commands, and prefer local processing with structured JSON output when needed.

Risk: Secrets passed in mcporter call arguments or JSON payloads may be logged, stored in shell history, or exposed to third-party MCP servers.

Mitigation: Use mcporter authentication or local server configuration for credentials instead of including API keys, tokens, or passwords in call arguments.

## Reference(s):

- [mcporter homepage](http://mcporter.dev)
- [Faberlens mcporter safety report](https://faberlens.ai/explore/mcporter)
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/mcporter-hardened)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use JSON-formatted CLI output when --output json is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
