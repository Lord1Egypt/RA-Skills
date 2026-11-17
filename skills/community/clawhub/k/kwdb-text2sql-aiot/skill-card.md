## Description:

Convert natural language queries to KWDB SQL for time series data, relational data, and cross-model analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwdb](https://clawhub.ai/user/kwdb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn natural-language KWDB database requests into KWDB-specific SQL for IoT time-series, relational, and cross-model workflows. It can guide schema discovery through an authorized MCP connection and formats generated SQL with assumptions and validation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL can be incorrect if the database, table, or column schema is unavailable or stale.

Mitigation: Use MCP schema discovery or user-confirmed schema before relying on generated SQL, and keep assumptions visible in the response.

Risk: Write, DDL, DROP, DELETE, UPDATE, or ALTER statements can modify or remove data if executed without review.

Mitigation: Require explicit user approval and review generated SQL before execution through an authorized KWDB MCP account.

Risk: Schema discovery can expose sensitive database, table, or column names.

Mitigation: Connect only to authorized KWDB environments and avoid broad discovery when schema metadata is sensitive.

## Reference(s):

- [KWDB Text2SQL AIoT ClawHub Page](https://clawhub.ai/kwdb/skills/kwdb-text2sql-aiot)
- [KWDB Publisher Profile](https://clawhub.ai/user/kwdb)
- [Output Template](artifact/assets/output-template.md)
- [Query Scenarios](artifact/references/scenarios.md)
- [KWDB MCP Server Integration](artifact/references/mcp-integration.md)
- [Time Series DDL Reference](artifact/references/ts-ddl.md)
- [Time Series Downsampling Reference](artifact/references/ts-downsampling.md)
- [Time Series Interpolation Reference](artifact/references/ts-interpolation.md)
- [Latest Value Query Reference](artifact/references/ts-latest-value.md)
- [Window and Event Query Reference](artifact/references/ts-window-events.md)
- [Relational Query Reference](artifact/references/relational.md)
- [Cross-Model Query Reference](artifact/references/cross-model.md)
- [Time Series Function Reference](artifact/references/ts-functions.md)
- [Relational Function Reference](artifact/references/relational-functions.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with SQL code blocks, assumptions, field mappings, validation checklists, and optional execution-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated SQL may depend on MCP-discovered schema or user-provided schema; assumptions should be marked when schema is not verified.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
