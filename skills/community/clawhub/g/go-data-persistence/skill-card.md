## Description: <br>
Data persistence patterns in Go covering raw SQL with sqlx/pgx, ORMs like Ent and GORM, connection pooling, migrations with golang-migrate, and transaction management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Go developers use this skill when implementing database access, designing repository layers, configuring connection pools, managing schema migrations, and coordinating transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration examples can change a real database if applied to the wrong target or without review. <br>
Mitigation: Confirm the target database URL, review both up and down migration files, and ensure backups or recovery plans exist before applying migrations. <br>
Risk: Installing the golang-migrate CLI with an unpinned latest version can introduce unexpected tooling changes. <br>
Mitigation: Pin the golang-migrate CLI version for repeatable local and CI/CD migration workflows. <br>


## Reference(s): <br>
- [Connection Pooling in Go](artifact/references/connection-pooling.md) <br>
- [Database Migrations with golang-migrate](artifact/references/migrations.md) <br>
- [Transaction Management in Go](artifact/references/transactions.md) <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/go-data-persistence) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Go, SQL, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; review database-changing examples before applying them to real systems.] <br>

## Skill Version(s): <br>
2.3.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
