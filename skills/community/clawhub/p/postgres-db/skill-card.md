## Description:

PostgreSQL Database helps agents run SQL queries, inspect schemas, manage backups and restores, and review database performance signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[limoxt](https://clawhub.ai/user/limoxt)

### License/Terms of Use:


## Use Case:

Developers and database operators use this skill to execute PostgreSQL queries, export schema details, and manage database backups or restores from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use PostgreSQL credentials to run high-impact database operations.

Mitigation: Use least-privileged database accounts and avoid production databases unless the operation is explicitly intended.

Risk: Mutating SQL and restore commands can change or remove database objects and data.

Mitigation: Review every non-read-only query and restore command before execution, and verify backups before destructive operations.

Risk: Backups, schema exports, and query results may contain sensitive information.

Mitigation: Store generated files in approved locations, restrict access, and handle exported data according to the database's sensitivity.

## Reference(s):

- [PostgreSQL command reference](references/postgres_commands.md)
- [ClawHub skill page](https://clawhub.ai/limoxt/skills/postgres-db)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown, JSON, CSV, shell command output, and generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce database query results, schema exports, backup files, restore status, and configuration guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
