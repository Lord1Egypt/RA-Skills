## Description:

Designs, analyzes, optimizes, and evolves database schemas for schema creation, SQL/NoSQL selection, schema review, index strategy, migrations, and EXPLAIN interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felix-antonio-sl](https://clawhub.ai/user/felix-antonio-sl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design or review database schemas, choose SQL or NoSQL engines, plan indexes, generate migrations with rollback, and interpret EXPLAIN plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated migrations may include destructive SQL such as DROP TABLE or DROP COLUMN.

Mitigation: Treat migrations as drafts, review all SQL before applying it, make logical backups, and use least-privileged database roles.

Risk: Generated SQL may be injectable or have weak rollback safeguards when built from untrusted schema JSON.

Mitigation: Avoid running migrations from untrusted schema JSON and manually validate rollback plans before execution.

## Reference(s):

- [database-designer reference](references/database-design-reference.md)
- [Database Selection Decision Tree](references/database_selection_decision_tree.md)
- [Index Strategy Patterns](references/index_strategy_patterns.md)
- [Database Normalization Guide](references/normalization_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL, Mermaid ERD, Prisma schema, JSON Schema, JSON, and shell command blocks as applicable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emits one primary artifact per response unless the user asks for multiple formats; companion scripts can print results to stdout or write requested output files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
