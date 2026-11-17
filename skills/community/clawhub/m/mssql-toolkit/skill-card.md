## Description:

Query and explore Microsoft SQL Server databases using sqlcmd. Schema inspection, ad-hoc T-SQL queries, data analysis. Works with any MSSQL/SQL Server instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fchrulk](https://clawhub.ai/user/fchrulk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to inspect Microsoft SQL Server schemas, run ad-hoc T-SQL queries, and shape common sqlcmd commands for database analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database passwords can be exposed through command-line arguments in the documented sqlcmd pattern.

Mitigation: Use least-privileged credentials and prefer authentication or invocation patterns that do not place reusable passwords in process arguments.

Risk: Using -C bypasses certificate validation and can weaken transport security when used outside temporary development contexts.

Mitigation: Configure trusted server certificates for normal use and reserve -C for explicit short-lived development exceptions.

Risk: Write-capable database access can alter or delete data if generated SQL is executed without review.

Mitigation: Default to read-only SQL, scope write-capable accounts tightly, and require transaction review, backups, or rollback planning before writes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fchrulk/skills/mssql-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with sqlcmd command examples and T-SQL snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires sqlcmd and the MSSQL_HOST, MSSQL_USER, MSSQL_PASSWORD, and MSSQL_DB environment variables; MSSQL_SQLCMD may override the sqlcmd path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
