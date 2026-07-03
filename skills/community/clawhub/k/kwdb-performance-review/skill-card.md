## Description: <br>
Optimize SQL query performance for KaiwuDB time-series and relational engines across EXPLAIN analysis, time-series optimization, pagination, and cross-model queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kwdb](https://clawhub.ai/user/kwdb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to review KWDB slow queries, parse EXPLAIN output, identify engine-specific anti-patterns, and draft query or configuration tuning guidance for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cluster-wide tuning or schema-changing SQL suggestions can alter production database behavior. <br>
Mitigation: Require DBA or operator review of impact, rollback, monitoring, and change controls before applying SET CLUSTER SETTING, CREATE INDEX, or DROP INDEX output. <br>
Risk: Resource-sensitive recommendations may degrade performance if memory, disk, or CPU assumptions are wrong. <br>
Mitigation: Confirm current resource availability and validate proposed query or configuration changes with EXPLAIN or targeted SHOW CLUSTER SETTING checks before execution. <br>


## Reference(s): <br>
- [KWDB Performance Review on ClawHub](https://clawhub.ai/kwdb/kwdb-performance-review) <br>
- [KWDB Performance Optimization: Core Rules](artifact/references/key-rules.md) <br>
- [EXPLAIN Output Analysis](artifact/references/query-analysis.md) <br>
- [Time-Series Query Optimization](artifact/references/timeseries-optimization.md) <br>
- [Pagination Optimization for Time-Series](artifact/references/pagination-optimization.md) <br>
- [Relational Query Optimization](artifact/references/relational-optimization.md) <br>
- [Cross-Model Query Optimization](artifact/references/cross-model-optimization.md) <br>
- [Storage Configuration Optimization](artifact/references/config-optimization.md) <br>
- [Index Analysis for Relational Tables](artifact/references/index-analysis.md) <br>
- [Schema-Level Performance Tuning](artifact/references/schema-tuning.md) <br>
- [Configuration Output Template](artifact/assets/config-output-template.md) <br>
- [Example Queries](artifact/assets/example-queries.md) <br>
- [Configuration Tuning Examples](artifact/assets/example-configs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Configuration guidance] <br>
**Output Format:** [Markdown with SQL code blocks and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include EXPLAIN validation queries and SET CLUSTER SETTING statements for human review; it should not execute database changes automatically.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
