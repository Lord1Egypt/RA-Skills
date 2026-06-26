## Description: <br>
PostgreSQL Database helps agents run SQL queries, export database schemas, and manage PostgreSQL backup and restore workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limoxt](https://clawhub.ai/user/limoxt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and database operators use this skill to inspect PostgreSQL databases, run SQL, export schema details, and prepare or restore backups through agent-guided commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute arbitrary SQL, including write, schema, DELETE, and DROP operations. <br>
Mitigation: Use a least-privilege PostgreSQL user, review every generated SQL statement, and require manual confirmation before write or destructive queries are executed. <br>
Risk: Restore operations can remove existing database objects because the restore helper uses cleanup behavior. <br>
Mitigation: Test restores in a separate database first and require manual confirmation before restore operations against shared or production databases. <br>
Risk: Database credentials may be supplied through PostgreSQL environment variables. <br>
Mitigation: Provide only scoped credentials and avoid production or superuser credentials unless explicitly required and approved. <br>


## Reference(s): <br>
- [PostgreSQL common command reference](references/postgres_commands.md) <br>
- [ClawHub release page](https://clawhub.ai/limoxt/postgres-db) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with SQL snippets, shell commands, and script outputs in table, JSON, CSV, or Markdown form.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce schema export files or database backup files when the bundled scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
