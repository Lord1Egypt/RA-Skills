## Description:

Design KWDB schemas and generate DDL for relational, time-series, and mixed workloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwdb](https://clawhub.ai/user/kwdb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to design KWDB schemas and produce executable DDL for relational, time-series, and mixed workloads. It helps classify workload type, gather requirements, choose types, plan keys and indexes, and provide validation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL can include destructive or administrative statements such as DROP, CASCADE, RETENTIONS, GRANT, REVOKE, and CREATE or DROP USER.

Mitigation: Manually review generated SQL against the target KWDB environment before execution, especially for destructive or administrative changes.

Risk: Schema or DDL guidance may be inappropriate if the target database engine or workload type is misidentified.

Mitigation: Confirm the database engine, classify the workload as relational, time-series, or mixed, and validate generated DDL with SHOW CREATE TABLE, SHOW COLUMNS, and SHOW INDEX before relying on it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kwdb/skills/kwdb-schema-design)
- [Core Rules and Decision Tree](references/key-rules.md)
- [Requirement Disambiguation Questions](references/disambiguation.md)
- [Skill Scope and Boundaries](references/_scope.md)
- [Table DDL Reference](references/table-ddl-ref.md)
- [Data Type Reference](references/type-ref.md)
- [Index DDL Reference](references/index-ddl-ref.md)
- [Constraint Reference](references/constraint-ref.md)
- [Partitioning Reference](references/partitioning-ref.md)
- [Time-Series Retention Reference](references/retention-ref.md)
- [View Reference](references/view-ref.md)
- [Output Templates](assets/output-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with SQL and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, schema design tables, executable KWDB DDL, and validation commands.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
