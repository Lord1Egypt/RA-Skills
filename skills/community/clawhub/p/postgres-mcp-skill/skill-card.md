## Description:

Postgres MCP helps agents manage and optimize PostgreSQL databases with health checks, index optimization, query plan analysis, schema queries, and SQL execution through postgres-mcp tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[victorzhou123](https://clawhub.ai/user/victorzhou123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to route PostgreSQL administration requests, configure postgres-mcp access, inspect database health, analyze query plans, tune indexes, query schemas, generate SQL, and execute database operations with user confirmation for writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can connect agents to live PostgreSQL databases through credential-bearing configuration.

Mitigation: Use a dedicated least-privilege database role, prefer read-only mode, and avoid placing production credentials directly in command lines or client configuration files.

Risk: The skill may rely on unpinned third-party postgres-mcp packages or container images.

Mitigation: Pin package and image versions and install only from a postgres-mcp source the user trusts.

Risk: SQL writes, DDL, index creation, backend termination, and scheduled automation can change data or disrupt service.

Mitigation: Require explicit review and confirmation before high-impact operations, show the exact SQL or command first, and use transactions or off-peak execution where appropriate.

## Reference(s):

- [Postgres MCP Skill README](artifact/README.md)
- [Postgres MCP](https://github.com/crystaldba/postgres-mcp)
- [Agent Skills Open Standard](https://agentskills.io)
- [Setup Postgres MCP](artifact/reference/setup-postgres-mcp/setup-postgres-mcp.md)
- [PostgreSQL Health Checks](artifact/reference/pg-health/pg-health.md)
- [PostgreSQL Index Tuning](artifact/reference/pg-index-tuning/pg-index-tuning.md)
- [PostgreSQL Query Plan Analysis](artifact/reference/pg-query-plan/pg-query-plan.md)
- [PostgreSQL Schema Queries](artifact/reference/pg-schema/pg-schema.md)
- [PostgreSQL SQL Execution](artifact/reference/pg-execute/pg-execute.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with SQL, shell, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database reports, SQL statements, execution plans, index recommendations, setup snippets, and confirmation prompts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
