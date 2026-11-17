## Description:

Database management skill supporting PostgreSQL, MySQL, SQLite, and MongoDB. Query, migrate, backup, and manage databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage PostgreSQL, MySQL/MariaDB, SQLite, and MongoDB databases, including querying, migrations, backups, restores, schema management, and CSV import/export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database credentials and connection settings may be exposed in shared terminals or logs.

Mitigation: Use least-privilege database accounts and avoid entering real credentials in shared terminals or persistent logs.

Risk: Restore, migration, import, and query commands can affect real data.

Mitigation: Confirm the target database before running data-changing commands and test destructive operations outside production first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-database-manager)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with shell command examples and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include database operation results such as success status, affected row counts, and returned rows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
