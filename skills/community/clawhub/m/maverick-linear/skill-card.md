## Description:

Maverick Linear MCPorter lets an agent read and write Linear workspace data through Linear's hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent inspect, search, create, update, and delete Linear workspace records through the connected Linear OAuth account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and write Linear workspace data using the connected OAuth account.

Mitigation: Review the OAuth grant scope and require explicit user confirmation before creating, updating, or deleting Linear records.

Risk: Tool arguments and results transit Linear's hosted MCP server.

Mitigation: Avoid sending unrelated secrets, credentials, or unrelated personal data through Linear tool calls.

Risk: Re-running setup with stale OAuth values can overwrite newer local credential state.

Mitigation: Only rerun setup with freshly minted OAuth credentials or after the user intentionally re-authorizes the Linear integration.

## Reference(s):

- [Linear MCP documentation](https://linear.app/docs/mcp)
- [Linear hosted MCP endpoint](https://mcp.linear.app/mcp)
- [ClawHub skill page](https://clawhub.ai/maverick/skills/maverick-linear)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON-capable tool output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The live tool catalog and schemas are discovered from Linear's MCP server; write capability depends on the connected OAuth account.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
