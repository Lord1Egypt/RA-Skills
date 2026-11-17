## Description:

Operate Notion workspace content through Notion MCP using the UXC CLI, including search, fetch, user and team lookup, page and database creation and updates, and comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to authenticate to Notion MCP, inspect available tools, search and fetch Notion content, and perform confirmed write operations with read-first safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OAuth callback URL may contain sensitive authorization data if pasted into persistent chat or logs.

Mitigation: Prefer a direct interactive OAuth flow when available, avoid storing callback URLs in persistent logs, and complete the exchange promptly through UXC.

Risk: The skill may request read and write access to a Notion workspace and leave a reusable UXC binding or linked command in place.

Mitigation: Request write scope only when writes are needed, require explicit user confirmation before write operations, and review or remove the UXC binding after use when persistence is not desired.

## Reference(s):

- [OAuth And Binding](references/oauth-and-binding.md)
- [Usage Patterns](references/usage-patterns.md)
- [Error Handling](references/error-handling.md)
- [Notion MCP endpoint](https://mcp.notion.com/mcp)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/notion-mcp-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JSON-envelope parsing and requires explicit confirmation before create, update, move, or delete-style Notion operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
