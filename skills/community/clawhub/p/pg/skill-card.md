## Description:

Tunes, designs, and operates PostgreSQL workflows including slow-query triage, indexing, schema design, migrations, vacuum, locks, replication, backups, security, and managed Postgres guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DBAs, and platform engineers use this skill to design, tune, troubleshoot, migrate, and operate PostgreSQL databases, including production incident response and managed-service constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local PostgreSQL memory may contain sensitive database context such as infrastructure details, schema shape, incidents, or preferences.

Mitigation: Treat ~/Clawic/data/pg/ as sensitive local state, avoid storing credentials or hostnames there, and confirm any writes to config or memory.

Risk: Production-derived statistics or database context could expose sensitive information if copied into lower-trust environments.

Mitigation: Sanitize production-derived data and statistics before reuse, apply access controls, and avoid copying production pg_statistic data unless the environment is trusted.

Risk: Operational guidance can affect production availability when applied to live DDL, destructive SQL, vacuum, locks, replication, or restore workflows.

Mitigation: Review generated commands before execution, rehearse risky changes on production-scale copies, and prefer the skill's documented least-destructive paths and timeout safeguards.

## Reference(s):

- [ClawHub PostgreSQL Skill Page](https://clawhub.ai/ivangdavila/skills/pg)
- [Clawic PostgreSQL Skill Page](https://clawic.com/skills/pg)
- [PostgreSQL Skill Definition](artifact/SKILL.md)
- [Setup and Local Memory](artifact/setup.md)
- [Security Guide](artifact/security.md)
- [Migrations Guide](artifact/migrations.md)
- [Slow Query Guide](artifact/slow-queries.md)
- [Backup and Restore Guide](artifact/backup-restore.md)
- [Managed Postgres Guide](artifact/managed-postgres.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with SQL, psql, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local PostgreSQL preferences and memory from ~/Clawic/data/pg/ when present.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
