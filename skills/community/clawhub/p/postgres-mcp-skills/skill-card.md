## Description:

Postgres MCP helps agents manage and optimize PostgreSQL databases through postgres-mcp workflows for setup, health checks, index tuning, query-plan analysis, schema inspection, and SQL execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[victorzhou123](https://clawhub.ai/user/victorzhou123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to connect an agent to postgres-mcp, inspect PostgreSQL health and schema, analyze slow queries, recommend indexes, and execute SQL with user confirmation for write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup examples can expose PostgreSQL credentials in command arguments or shared configuration files.

Mitigation: Keep database passwords out of command arguments and shared config files; use secrets management or protected local configuration where available.

Risk: The skill can guide installation and execution of third-party postgres-mcp components.

Mitigation: Use a pinned and verified postgres-mcp image or package before connecting it to a database.

Risk: SQL execution, index changes, and administrative actions can modify or disrupt a database.

Mitigation: Use a dedicated least-privilege database role, prefer read-only mode for production, and require explicit user confirmation before writes, session termination, or recurring health checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/victorzhou123/skills/postgres-mcp-skills)
- [postgres-mcp project](https://github.com/crystaldba/postgres-mcp)
- [Postgres MCP README](artifact/README.md)
- [Setup postgres-mcp](artifact/reference/setup-postgres-mcp/setup-postgres-mcp.md)
- [PostgreSQL health checks](artifact/reference/pg-health/pg-health.md)
- [PostgreSQL index tuning](artifact/reference/pg-index-tuning/pg-index-tuning.md)
- [PostgreSQL query-plan analysis](artifact/reference/pg-query-plan/pg-query-plan.md)
- [PostgreSQL schema inspection](artifact/reference/pg-schema/pg-schema.md)
- [PostgreSQL SQL execution](artifact/reference/pg-execute/pg-execute.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline SQL, JSON, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database health summaries, schema summaries, query-plan analysis, index recommendations, SQL statements, MCP setup commands, and client configuration snippets.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
