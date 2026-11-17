## Description:

Optimizes SQL query performance for KaiwuDB time-series and relational engines through EXPLAIN analysis, query rewrites, pagination guidance, cross-model query guidance, and conditional configuration review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwdb](https://clawhub.ai/user/kwdb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to review slow KWDB or KaiwuDB SQL, interpret EXPLAIN plans, choose safer query rewrites, and prepare DBA-reviewed configuration suggestions when query-only optimization is exhausted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can suggest cluster-wide configuration changes such as SET CLUSTER SETTING, which may affect production performance or resource usage.

Mitigation: Treat configuration output as DBA-reviewed change-management material; require confirmed memory, disk, and CPU context before applying changes and never auto-execute SET CLUSTER SETTING statements.

Risk: The artifact includes schema-changing or index-changing examples for relational tables while its declared scope excludes DDL and schema design.

Mitigation: Use those examples as review guidance only; delegate CREATE INDEX, DROP INDEX, ALTER TABLE, and other schema changes to an appropriate schema-design workflow.

Risk: Confusing KaiwuDB time-series and relational engines can produce invalid or harmful recommendations, especially secondary indexes on time-series tables.

Mitigation: Verify the table engine before recommending indexes or query rewrites, and preserve the artifact guardrail that time-series tables do not support secondary indexes.

## Reference(s):

- [KWDB Performance Optimization: Core Rules](references/key-rules.md)
- [EXPLAIN Output Analysis](references/query-analysis.md)
- [Time-Series Query Optimization](references/timeseries-optimization.md)
- [Pagination Optimization for Time-Series](references/pagination-optimization.md)
- [Relational Query Optimization](references/relational-optimization.md)
- [Cross-Model Query Optimization](references/cross-model-optimization.md)
- [Schema-Level Performance Tuning](references/schema-tuning.md)
- [Index Analysis for Relational Tables](references/index-analysis.md)
- [Storage Configuration Optimization](references/config-optimization.md)
- [Configuration Optimization Output Template](assets/config-output-template.md)
- [Configuration Tuning Examples](assets/example-configs.md)
- [Example Queries for kwdb-performance-review](assets/example-queries.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with SQL code blocks and review tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes original and optimized SQL, anti-pattern analysis, expected EXPLAIN changes, validation SQL, and DBA-review notes for configuration changes.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
