## Description:

Use when querying Outlit customer data via MCP tools for customer analytics, revenue metrics, activity timelines, cohort analysis, churn risk assessment, SQL queries, and Outlit data exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-paz](https://clawhub.ai/user/leo-paz)

### License/Terms of Use:


## Use Case:

Developers and customer-facing teams use this skill to connect an agent to Outlit MCP tools, inspect customer and user records, analyze revenue and churn, and compose read-only ClickHouse SQL for customer intelligence workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to persist an API key while enabling broad customer-data access.

Mitigation: Install only if Outlit is trusted with the connected organization data, use a narrowly scoped and revocable API key, keep MCP configuration files out of repositories, restrict file permissions, and rotate exposed keys.

Risk: Customer analytics queries can expose sensitive organization data if credentials or outputs are shared too broadly.

Mitigation: Review generated queries and reports before sharing, limit access to authorized users, and prefer filtering at the source with explicit time ranges and limits.

## Reference(s):

- [SQL Reference](references/sql-reference.md)
- [Common Workflows](references/workflows.md)
- [Outlit Dashboard](https://app.outlit.ai)
- [Outlit MCP Endpoint](https://mcp.outlit.ai/mcp)
- [ClawHub Skill Page](https://clawhub.ai/leo-paz/skills/outlit-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, SQL queries, guidance]

**Output Format:** [Markdown guidance with JSON, bash, and SQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce read-only customer analytics queries and MCP client configuration snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
