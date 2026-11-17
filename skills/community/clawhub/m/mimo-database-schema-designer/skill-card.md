## Description:

A Chinese-language skill for designing production-ready database schemas from requirements through ER diagrams, DDL, indexing, multitenancy, sharding, migrations, and review for MySQL, PostgreSQL, MongoDB, Redis, and Milvus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this Chinese-language skill to translate product requirements into database models, ER diagrams, table definitions, DDL, index strategies, migration plans, and design review checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated DDL, migration, rollback, partitioning, or security choices may be incorrect or unsuitable for a production database.

Mitigation: Review generated database designs and scripts before applying them to a real database, especially migration, rollback, partitioning, and security-sensitive decisions.

Risk: Schema guidance for sensitive fields, audit logging, and permissions may omit project-specific compliance or access-control requirements.

Mitigation: Confirm encryption, authorization, audit logging, soft deletion, and retention requirements with the application's security and compliance owners before release.

## Reference(s):

- [数据库模式设计 - 详细参考](artifact/references/details.md)
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/mimo-database-schema-designer)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Chinese Markdown with Mermaid ER diagrams, SQL DDL, tables, and migration script templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese prose; DDL and field names in English; generated designs require review before database changes are applied.]

## Skill Version(s):

1.4.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
