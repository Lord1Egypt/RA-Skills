## Description:

专业解析 MySQL EXPLAIN 与慢查询日志，定位性能瓶颈，并提供索引与 SQL 重写优化建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DBAs, and database performance reviewers use this skill to inspect MySQL SQL, EXPLAIN output, and slow-query logs, then review heuristic index and rewrite suggestions before changing production schemas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated index and SQL rewrite suggestions may be incomplete or suboptimal for a specific production schema.

Mitigation: Review recommendations with a DBA and validate changes using EXPLAIN, staging tests, and workload-aware benchmarks before applying them.

Risk: SQL snippets and slow-query logs can contain sensitive table names, predicates, or business data.

Mitigation: Run the helper locally and minimize or redact sensitive production details when sharing analysis inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/mysql-slow-query-analyzer-kay)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown, JSON, and plain text reports with optional shell commands and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local analysis from user-provided SQL, EXPLAIN output, or slow-query logs; optimization advice is heuristic and should be reviewed before production use.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
