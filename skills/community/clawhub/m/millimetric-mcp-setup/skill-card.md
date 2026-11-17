## Description:

Connect AI agents (Claude Code, Claude Desktop, Cursor, MCP Inspector, OpenClaw) to the Millimetric MCP server so they can natively call track_event, query_events, get_stats, top_sources, and compare_projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soybelli](https://clawhub.ai/user/soybelli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect MCP-capable agents to Millimetric analytics endpoints for reading analytics data, tracking events when permitted, and verifying client configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP client configuration can expose bearer tokens if committed or shared.

Mitigation: Keep configuration files containing Millimetric keys out of source control and rotate any key that may have been exposed.

Risk: Using write-capable or account-wide keys gives an agent broader analytics access than many read-only workflows require.

Mitigation: Default to read-only keys and use write-capable or account-wide keys only when the workflow specifically needs those scopes.

Risk: Running MCP Inspector through an unpinned package can add local execution and supply-chain risk.

Mitigation: Pin or isolate the inspector package and run it only on a trusted machine.

## Reference(s):

- [Millimetric MCP endpoint](https://api.millimetric.ai/mcp)
- [Millimetric account MCP endpoint](https://api.millimetric.ai/mcp/account)
- [ClawHub skill page](https://clawhub.ai/soybelli/skills/millimetric-mcp-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown setup guidance with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Millimetric key and curl for CLI verification examples.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
