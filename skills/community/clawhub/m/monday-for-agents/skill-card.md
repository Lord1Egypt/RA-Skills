## Description:

Set up a monday.com account for an OpenClaw agent and work with monday.com boards, items, and updates via the GraphQL API or MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure an OpenClaw agent for monday.com and perform board, item, update, and troubleshooting workflows through GraphQL or MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A monday.com API token may be exposed if placed directly in plaintext configuration files.

Mitigation: Use the platform secret or environment mechanism, avoid committing tokens, and use a least-privilege monday.com account.

Risk: The local MCP setup uses an unpinned package that would receive the monday.com API token.

Mitigation: Prefer the hosted OAuth MCP option, or pin and review the local MCP package before use.

Risk: Board IDs stored in TOOLS.md can reveal workspace-specific internal metadata.

Mitigation: Treat board IDs as internal data and avoid publishing or sharing TOOLS.md outside the intended workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/netanel-abergel/skills/monday-for-agents)
- [monday.com GraphQL API](https://developer.monday.com/api-reference)
- [monday.com MCP Server Docs](https://mcp.monday.com)
- [monday.com Agent Signup](https://monday.com/agents-signup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, JSON, and GraphQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MONDAY_API_TOKEN for direct API usage; hosted MCP option uses OAuth.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
