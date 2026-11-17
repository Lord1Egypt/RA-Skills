## Description:

Hologres Query Optimizer helps agents analyze Hologres SQL performance issues, interpret EXPLAIN and EXPLAIN ANALYZE output, and provide query optimization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenbingyu](https://clawhub.ai/user/wenbingyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to diagnose slow Hologres queries, read execution-plan metrics, identify bottleneck operators, and choose targeted SQL, index, statistics, distribution-key, or GUC tuning actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose EXPLAIN ANALYZE, ANALYZE, table-property changes, or persistent database-level GUC set/reset commands against production Hologres systems.

Mitigation: Require explicit approval before running database commands, review target scope and expected impact, and test changes in a non-production environment when practical.

Risk: Installing or using hologres-cli directly in an uncontrolled environment can broaden operational risk for database work.

Mitigation: Install hologres-cli in an isolated pinned environment and use this skill only for Hologres-related analysis and tuning tasks.

## Reference(s):

- [Hologres Query Operators Reference](references/operators.md)
- [Hologres Query Optimization Patterns](references/optimization-patterns.md)
- [Hologres GUC Parameters for Query Tuning](references/guc-parameters.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Hologres CLI commands, SQL statements, execution-plan interpretation, and tuning recommendations for human review before execution.]

## Skill Version(s):

0.2.0 (source: server release evidence and VERSION; package.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
