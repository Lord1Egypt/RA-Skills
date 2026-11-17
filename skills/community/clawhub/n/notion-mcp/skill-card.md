## Description:

Helps agents search and manage Notion workspace content through MCP using a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers working with a Notion workspace use this skill to search and retrieve content, create or update pages and databases, and configure approved automations through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notion access may expose workspace content or change pages and databases.

Mitigation: Check the active connection and target resource, use only needed scopes, and obtain confirmation before writes or new connections.

Risk: Hosted functions, triggers, destinations, and replay can persist or forward workspace data.

Mitigation: Confirm the action, destination URL, data fields, and persistence behavior before enabling automation or replay.

Risk: API keys and local event handlers can expose credentials or execute unintended commands.

Mitigation: Prefer the managed CLI login; protect any API key and use event watch --exec only with a handler script you supplied and reviewed.

## Reference(s):

- [ClawHub Notion MCP release](https://clawhub.ai/byungkyu/skills/notion-mcp)
- [Maton homepage](https://maton.ai)
- [Notion MCP overview](https://developers.notion.com/guides/mcp)
- [Notion MCP supported tools](https://developers.notion.com/guides/mcp/mcp-supported-tools)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Notion trigger reference](references/notion/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance]

**Output Format:** [Markdown guidance with command examples and structured Notion results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions operate within the authorized Notion connection; writes require user confirmation.]

## Skill Version(s):

1.2.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
