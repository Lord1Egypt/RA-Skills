## Description: <br>
A PostgreSQL administration and optimization skill that routes database health checks, index tuning, query-plan analysis, schema inspection, SQL execution, and postgres-mcp setup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[victorzhou123](https://clawhub.ai/user/victorzhou123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to administer PostgreSQL databases through postgres-mcp: set up the MCP service, inspect health and schema, analyze query plans, tune indexes, and run SQL with confirmation and read-only safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose or change PostgreSQL data when configured with powerful database credentials. <br>
Mitigation: Use a dedicated least-privileged or read-only database account, avoid superuser credentials, and protect connection strings. <br>
Risk: Write operations, DDL, backend termination, statistics resets, or scheduled monitoring actions can affect production databases. <br>
Mitigation: Manually review and approve every high-impact operation, prefer transactions or read-only mode where appropriate, and run risky changes during controlled maintenance windows. <br>
Risk: The skill depends on an external postgres-mcp package or image and may expose an SSE endpoint. <br>
Mitigation: Pin or review the postgres-mcp package or image before deployment, and keep SSE endpoints local or access-controlled. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/victorzhou123/postgres-mcp-skills) <br>
- [postgres-mcp](https://github.com/crystaldba/postgres-mcp) <br>
- [Agent Skills open standard](https://agentskills.io) <br>
- [setup-postgres-mcp reference](reference/setup-postgres-mcp/setup-postgres-mcp.md) <br>
- [pg-health reference](reference/pg-health/pg-health.md) <br>
- [pg-index-tuning reference](reference/pg-index-tuning/pg-index-tuning.md) <br>
- [pg-query-plan reference](reference/pg-query-plan/pg-query-plan.md) <br>
- [pg-schema reference](reference/pg-schema/pg-schema.md) <br>
- [pg-execute reference](reference/pg-execute/pg-execute.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with SQL snippets, shell commands, configuration steps, and tabular database findings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request user confirmation before write or DDL operations and depends on configured postgres-mcp tools.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
