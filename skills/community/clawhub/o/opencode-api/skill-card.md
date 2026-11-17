## Description:

Connects an agent to an OpenCode HTTP server for code review, code analysis, and coding tasks, with references for agents, SDK endpoints, configuration, permissions, providers, MCP, LSP, and server deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlin53882](https://clawhub.ai/user/jlin53882)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to delegate code review, file analysis, multi-turn coding tasks, and OpenCode API operations to a trusted local or approved OpenCode server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an agent to an untrusted or exposed OpenCode server can route code, prompts, and actions through infrastructure outside the user's intended trust boundary.

Mitigation: Use only a trusted OpenCode server, keep it bound to 127.0.0.1 unless authentication, TLS or a private network, and firewall controls are in place.

Risk: Auto-start behavior can launch OpenCode when the user expected a passive client-only workflow.

Mitigation: Disable auto-start when the agent should not launch OpenCode automatically.

Risk: Private repository code, credentials, or other confidential data can be sent to the configured server or model provider during review and coding workflows.

Mitigation: Do not send secrets or confidential private-repo code unless the OpenCode server and model provider are approved for that data.

Risk: MCP servers and plugin packages can extend tool behavior and package execution beyond the base skill.

Mitigation: Pin, review, and approve MCP and plugin packages before enabling them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlin53882/skills/opencode-api)
- [OpenCode HTTP API reference](references/api-reference.md)
- [SDK complete API](references/sdk.md)
- [Server deployment](references/server.md)
- [Agents system](references/agents.md)
- [Permissions](references/permissions.md)
- [Providers](references/providers.md)
- [MCP](references/mcp.md)
- [Plugins](references/plugins.md)
- [Code review prompt](references/code-review-prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, shell, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce OpenCode HTTP API calls and client-script usage guidance for a configured server.]

## Skill Version(s):

2.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
