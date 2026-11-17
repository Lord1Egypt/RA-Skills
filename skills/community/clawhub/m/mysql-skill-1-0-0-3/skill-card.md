## Description:

MySQL database management skill for using natural language to query and manage MySQL databases, including SELECT, INSERT, UPDATE, DELETE, table management, backup, and restore workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ding-renew](https://clawhub.ai/user/ding-renew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database administrators, and operators use this skill to draft MySQL queries, table changes, backup and restore commands, troubleshooting steps, and performance review guidance from natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose destructive database changes such as UPDATE, DELETE, ALTER TABLE, and restore operations.

Mitigation: Review generated SQL before execution, require explicit confirmation for writes and restores, back up first, and use transactions where possible.

Risk: Database credentials may be stored in local configuration or environment variables.

Mitigation: Use least-privilege database accounts and store credentials with restrictive permissions or a safer secret mechanism.

Risk: Unbounded or inefficient SQL may affect performance on large datasets.

Mitigation: Review query plans, add LIMIT clauses where appropriate, and validate indexing before running expensive queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ding-renew/skills/mysql-skill-1-0-0-3)
- [MySQL documentation](https://dev.mysql.com/doc/)
- [MySQL optimization guide](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [MySQL Workbench](https://www.mysql.com/products/workbench/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with SQL, shell, and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before execution, especially writes, restores, and credential-related configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
