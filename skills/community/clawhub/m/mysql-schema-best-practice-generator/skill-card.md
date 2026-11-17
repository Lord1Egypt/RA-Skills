## Description:

基于MySQL 8.0 的数据库建表最佳实践规范生成与审校，输出规范化DDL、索引策略与校验清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatonionlee](https://clawhub.ai/user/fatonionlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to generate or review MySQL 8.0 schema DDL, index and constraint strategies, migration notes, validation checklists, and risk warnings for application tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may attempt to add or change MCP formatter configuration without clear validation or user approval.

Mitigation: Prevent automatic MCP server registration, require explicit approval for configuration changes, and allowlist only trusted formatter tools.

Risk: Generated DDL, index choices, or review fixes may not match the production workload or migration constraints.

Mitigation: Have a database engineer review generated SQL, test migrations in a non-production environment, and validate rollback steps before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fatonionlee/skills/mysql-schema-best-practice-generator)
- [Source skill instructions](artifact/SKILL.md)
- [Checklist template](artifact/template/checklist_template.json)
- [DDL snippets template](artifact/template/ddl_snippets.sql)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Structured JSON-like responses with SQL DDL, checklists, rationale, migration notes, issues, fixes, and risk warnings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are oriented to MySQL 8.0 schema generation and DDL review.]

## Skill Version(s):

0.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
