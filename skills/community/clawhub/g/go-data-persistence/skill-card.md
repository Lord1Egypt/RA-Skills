## Description:

Data persistence patterns in Go covering raw SQL with sqlx/pgx, ORMs like Ent and GORM, connection pooling, migrations with golang-migrate, and transaction management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design Go database access layers, configure database pools, manage schema migrations, and apply transaction patterns for application persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is reference material and may include examples that look production-ready.

Mitigation: Treat examples as design guidance, then adapt and review them against the target application's correctness, reliability, and operational requirements before use.

Risk: Transaction examples may be unsafe for payments, balances, inventory, credits, or other high-impact state changes if copied without review.

Mitigation: Review or replace transaction logic for financial integrity, rollback behavior, cleanup paths, isolation level, and concurrency behavior before using it in high-impact workflows.

Risk: Shell examples may install tools using floating versions.

Mitigation: Pin CLI and dependency versions before installing or adding tools to project automation.

## Reference(s):

- [Connection Pooling in Go](references/connection-pooling.md)
- [Database Migrations with golang-migrate](references/migrations.md)
- [Transaction Management in Go](references/transactions.md)
- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/go-data-persistence)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Go, SQL, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.3.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
