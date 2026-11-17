## Description:

Comprehensive guide for Go database access - parameterized queries, struct scanning, NULLable columns, transactions, isolation levels, SELECT FOR UPDATE, connection pool, batch processing, context propagation, and migration tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when writing, reviewing, or debugging Go code that interacts with PostgreSQL, MariaDB, MySQL, or SQLite. It helps agents produce and review database access code that uses explicit SQL, parameterized queries, context propagation, transactions, connection pooling, testing patterns, and migration-tool guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may edit Go repository files and guide database-access implementation.

Mitigation: Review generated code before running it against real databases.

Risk: Database tools connected to production or schema, migration, or index changes can affect live systems.

Mitigation: Require explicit approval before connecting SQL tools to production or applying schema, migration, or index changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-database)
- [Publisher profile](https://clawhub.ai/user/samber)
- [Homepage](https://github.com/samber/cc-skills-golang)
- [database/sql tutorial](https://go.dev/doc/database/)
- [sqlx](https://github.com/jmoiron/sqlx)
- [pgx](https://github.com/jackc/pgx)
- [golang-migrate](https://github.com/golang-migrate/migrate)
- [Flyway](https://flywaydb.org/)
- [Atlas](https://atlasgo.io/)
- [Struct Scanning](references/scanning.md)
- [Transactions](references/transactions.md)
- [Testing Database Code](references/testing.md)
- [Database Performance](references/performance.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Go code examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scoped to Go source files; requires the go binary when commands are run.]

## Skill Version(s):

1.3.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
