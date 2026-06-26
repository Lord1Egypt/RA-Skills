## Description: <br>
Provides PostgreSQL database operation guidance and scripts for connection setup, schema inspection, SQL execution, CSV export, backup and restore workflows, and pgvector similarity queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[callxor](https://clawhub.ai/user/callxor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to connect to PostgreSQL databases, inspect schemas, run SQL, export data, and manage backups for development and operations tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad database credential and raw SQL authority. <br>
Mitigation: Use a least-privileged or read-only database user by default, and require manual approval for UPDATE, DELETE, DDL, restore, and other high-impact operations. <br>
Risk: Credentials may be exposed if environment files or ~/.pgpass are stored or shared insecurely. <br>
Mitigation: Keep .env and ~/.pgpass private, restrict file permissions, and avoid hardcoding passwords in scripts, logs, or prompts. <br>
Risk: Backup and CSV export workflows can create sensitive local files. <br>
Mitigation: Store exports and backups only in trusted directories, protect generated files, and apply a retention policy appropriate for the data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/callxor/postgresql-db) <br>
- [PostgreSQL documentation](https://www.postgresql.org/docs/) <br>
- [pgvector documentation](https://github.com/pgvector/pgvector) <br>
- [psql command reference](https://postgresmeta.com/docs/psql-commands) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline SQL and bash examples, plus shell scripts for query, CSV export, and backup workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PostgreSQL command-line tools and database credentials supplied through environment variables or ~/.pgpass.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
