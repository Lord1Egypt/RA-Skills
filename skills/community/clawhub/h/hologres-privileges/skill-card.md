## Description:

Hologres privilege management using the PostgreSQL standard authorization model for creating users, granting and revoking schema, table, column, and view privileges, configuring default privileges, diagnosing permission issues, and planning role-based access control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenbingyu](https://clawhub.ai/user/wenbingyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data platform engineers, and database administrators use this skill to manage and audit Hologres Expert Model permissions with PostgreSQL GRANT, REVOKE, role, ownership, and default privilege workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privilege-changing SQL examples can grant broad access, alter ownership, or change administrative state if copied into production without review.

Mitigation: Use only authorized Hologres administrative accounts, review each command against the intended access boundary, and prefer role-based least-privilege grants.

Risk: Examples involving PUBLIC, SUPERUSER, DROP, OWNER, or ALTER DATABASE can have high operational or security impact.

Mitigation: Require explicit approval and environment-specific scoping before applying these commands.

Risk: The skill depends on hologres-cli for SQL execution.

Mitigation: Install hologres-cli from a trusted, pinned source and verify the target Hologres instance before running write operations.

## Reference(s):

- [GRANT/REVOKE Complete Syntax Reference](references/grant-revoke-reference.md)
- [Permission Diagnostic SQL Collection](references/diagnostic-queries.md)
- [Privilege Management Best Practices](references/best-practices.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance depends on hologres-cli for SQL execution and should be reviewed before applying privilege-changing commands.]

## Skill Version(s):

0.2.0 (source: server release evidence and VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
