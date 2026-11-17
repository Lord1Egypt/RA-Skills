## Description:

PostgreSQL 数据库管理技能。通过自然语言查询、管理 PostgreSQL 数据库，支持复杂查询、性能分析、JSON 操作、全文搜索等高级功能。当用户提到 PostgreSQL、Postgres、复杂查询、性能优化时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and database administrators use this skill to request PostgreSQL query help, performance analysis, JSONB operations, full-text search guidance, and backup or restore command examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL or restore commands may modify production data, indexes, schemas, or database state.

Mitigation: Review the target database, environment, rollback plan, backup provenance, and command intent before running UPDATE, CREATE INDEX, pg_restore, or similar operations.

Risk: Database connection examples can expose credentials if real passwords are placed into shared prompts, shell history, or logs.

Mitigation: Use local environment variables or secret management, avoid sharing real credentials, and redact connection strings before pasting them into agent conversations.

Risk: Package installation commands can change the host system.

Mitigation: Review sudo or package-manager commands before execution and install PostgreSQL client tooling only in intended environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryanlee-gemini/skills/postgres-skill)
- [PostgreSQL official documentation](https://www.postgresql.org/docs/)
- [PostgreSQL performance optimization](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [PostgreSQL JSON types](https://www.postgresql.org/docs/current/datatype-json.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database-impacting SQL or shell commands that require user review before execution.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
