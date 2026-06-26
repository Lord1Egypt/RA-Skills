## Description: <br>
PostgreSQL database management and optimization assistant that supports health checks, index optimization, query plan analysis, schema queries, and SQL execution through postgres-mcp MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[victorzhou123](https://clawhub.ai/user/victorzhou123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to configure postgres-mcp access, inspect PostgreSQL health and schema, analyze slow queries, recommend indexes, and execute SQL with explicit safeguards for write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad live-database access and SQL execution through postgres-mcp. <br>
Mitigation: Use a dedicated least-privilege PostgreSQL account, enable read-only mode by default, and keep production credentials out of command lines and persistent config files. <br>
Risk: Write operations, DDL, index creation, scheduled tasks, and backend cancellation or termination can alter data, schema, performance, or availability. <br>
Mitigation: Require explicit user confirmation, show the exact SQL or operational action before execution, and prefer transactions or off-peak maintenance windows for high-impact changes. <br>
Risk: Unpinned postgres-mcp packages or container images can change behavior across installs. <br>
Mitigation: Pin the postgres-mcp package or image version during installation and review updates before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/victorzhou123/postgres-mcp-skill) <br>
- [README](README.md) <br>
- [setup-postgres-mcp](reference/setup-postgres-mcp/setup-postgres-mcp.md) <br>
- [pg-health](reference/pg-health/pg-health.md) <br>
- [pg-index-tuning](reference/pg-index-tuning/pg-index-tuning.md) <br>
- [pg-query-plan](reference/pg-query-plan/pg-query-plan.md) <br>
- [pg-schema](reference/pg-schema/pg-schema.md) <br>
- [pg-execute](reference/pg-execute/pg-execute.md) <br>
- [postgres-mcp project](https://github.com/crystaldba/postgres-mcp) <br>
- [Agent Skills Open Standard](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL, shell command, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run PostgreSQL operations through available postgres-mcp tools after connection checks and required confirmations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
