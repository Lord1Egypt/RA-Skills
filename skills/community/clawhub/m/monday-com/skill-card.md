## Description:

Manage monday.com boards, items, columns, groups, updates, and workflows via MCP server or GraphQL API fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[regevguym](https://clawhub.ai/user/regevguym)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, and developers use this skill to create, query, and update monday.com project, CRM, workflow, board, item, column, group, update, webhook, and file resources through an agent. It is suited for task tracking, project status summaries, CRM pipeline setup, sprint planning, reporting, and monday.com AI workflow support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup uses an unpinned package install pattern, so the executed server can change between installations.

Mitigation: Pin the MCP package version before operational use and update it through normal review.

Risk: The monday.com API token can grant broad access to business data and workspace actions.

Mitigation: Use a dedicated, least-privilege token and store it only in an approved secrets mechanism.

Risk: Destructive changes, file uploads, webhook destinations, and workspace-level changes can modify or expose monday.com data.

Mitigation: Require explicit user confirmation before those operations and verify the target board, item, file, endpoint, or workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/regevguym/skills/monday-com)
- [monday.com developer docs](https://developer.monday.com)
- [monday.com API reference](https://developer.monday.com/api-reference)
- [monday.com MCP server](https://github.com/mondaycom/mcp)
- [GraphQL API Examples](references/graphql-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline JSON, GraphQL, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include direct monday.com board, item, dashboard, file, webhook, or update URLs when operations create or locate resources.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
