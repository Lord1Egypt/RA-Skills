## Description:

Manages MySQL databases through the mysql CLI or Python mysql-connector for query execution, schema changes, backup and restore, performance analysis, and user permission tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasydongo](https://clawhub.ai/user/jasydongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to inspect MySQL databases, run SQL queries, manage schemas, create or restore backups, tune performance, and review user permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled shell scripts may expose MySQL passwords or execute unintended local commands when passed untrusted connection, query, password, database, or file-path values.

Mitigation: Use the skill only in controlled environments; prefer protected MySQL option files or mysql_config_editor and review all generated commands before execution.

Risk: Restore, schema, permission, and query operations can change or destroy database state.

Mitigation: Use least-privileged database accounts, create backups before destructive operations, and require explicit confirmation before restores or permission changes.

Risk: Guidance may include executable SQL or shell snippets that are not appropriate for a production database as written.

Mitigation: Test commands against non-production databases first and adapt host, database, user, and SQL values before running them on real systems.

## Reference(s):

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Schema Analysis Reference](references/schema-analysis.md)
- [Performance Tuning Reference](references/performance-tuning.md)
- [ClawHub Skill Page](https://clawhub.ai/jasydongo/skills/mysqladm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable MySQL CLI commands, SQL statements, and script invocations that require operator review before use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
