## Description: <br>
Comprehensive guide for Go database access: parameterized queries, struct scanning, NULLable columns, transactions, isolation levels, SELECT FOR UPDATE, connection pool, batch processing, context propagation, and migration tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when writing, reviewing, or debugging Go code that interacts with PostgreSQL, MariaDB, MySQL, or SQLite. It guides safe database access patterns, transaction handling, testing, performance review, and migration-tool selection while avoiding schema generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or edited Go database code may be incorrect for a repository's schema, workload, or production constraints. <br>
Mitigation: Review generated code before applying it and validate behavior with unit and integration tests against non-production databases. <br>
Risk: Database integration tests or exploratory commands could affect live data if pointed at production services. <br>
Mitigation: Keep integration tests and agent-run database tooling scoped to test databases, fixtures, or disposable containers. <br>
Risk: Schema, index, or migration suggestions can cause performance, locking, or data integrity problems if applied blindly. <br>
Mitigation: Use the skill's guidance to avoid generating schemas directly, route migration SQL through human review, and measure index or query changes before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-database) <br>
- [Publisher profile](https://clawhub.ai/user/samber) <br>
- [Project homepage](https://github.com/samber/cc-skills-golang) <br>
- [Database Performance](references/performance.md) <br>
- [Struct Scanning and NULLable Columns](references/scanning.md) <br>
- [Testing Database Code](references/testing.md) <br>
- [Transactions, Isolation Levels, and Locking](references/transactions.md) <br>
- [Go database/sql tutorial](https://go.dev/doc/database/) <br>
- [sqlx](https://github.com/jmoiron/sqlx) <br>
- [pgx](https://github.com/jackc/pgx) <br>
- [golang-migrate](https://github.com/golang-migrate/migrate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Go code examples, SQL snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to inspect repository patterns, edit files, run Go tooling, and launch scoped sub-agents.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
