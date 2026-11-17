## Description:

Provides PostgreSQL database operation guidance for connection management, schema inspection, CRUD queries, backup and restore, CSV export and import, performance checks, and pgvector similarity queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[callxor](https://clawhub.ai/user/callxor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to generate PostgreSQL commands, SQL examples, backup and export workflows, and operational troubleshooting guidance for environments where database access has already been authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use database credentials and execute user-supplied SQL against PostgreSQL instances.

Mitigation: Use least-privilege database roles, require explicit authorization before running SQL, and avoid granting write or administrative privileges unless the task requires them.

Risk: Backup and CSV export workflows can write sensitive database contents to local files.

Mitigation: Review destination paths before execution, store exports and backups in approved locations, and apply retention and access controls for production data.

Risk: Helper scripts load credentials from local environment sources such as .env or DB_PASSWORD.

Mitigation: Prefer .pgpass or externally supplied environment variables, keep credentials out of source files and logs, and run scripts only from trusted directories.

## Reference(s):

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [psql Command Reference](https://postgresmeta.com/docs/psql-commands)
- [ClawHub Skill Page](https://clawhub.ai/callxor/skills/postgresql-db)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline SQL and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that read database credentials, execute SQL, and write backup or export files.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
