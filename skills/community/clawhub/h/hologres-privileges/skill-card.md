## Description: <br>
Hologres privilege management using the PostgreSQL standard authorization model for creating users, granting and revoking schema, table, column, and view privileges, configuring default privileges, diagnosing permission issues, and planning role-based access control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenbingyu](https://clawhub.ai/user/wenbingyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Database administrators, data platform engineers, and developers use this skill to manage Hologres Expert Model privileges, prepare GRANT and REVOKE workflows, configure default privileges for future objects, and diagnose permission failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL may change Hologres users, roles, privileges, default privileges, or ownership if executed against the wrong instance, database, schema, role, or user. <br>
Mitigation: Verify the target instance, database, schema, role, and user before running generated SQL, and require review before write operations. <br>
Risk: Examples include powerful administrative actions such as SUPERUSER changes, PUBLIC grants, ownership transfer, DROP USER/ROLE, REASSIGN OWNED, ALTER DATABASE, and default-privilege changes. <br>
Mitigation: Avoid PUBLIC and SUPERUSER unless explicitly intended, and require extra review for ownership transfer, user or role removal, database alteration, and default-privilege changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wenbingyu/hologres-privileges) <br>
- [GRANT/REVOKE Complete Syntax Reference](references/grant-revoke-reference.md) <br>
- [Permission Diagnostic SQL Collection](references/diagnostic-queries.md) <br>
- [Privilege Management Best Practices](references/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated SQL and commands should be reviewed before execution against a Hologres instance.] <br>

## Skill Version(s): <br>
0.2.0 (source: release evidence and VERSION file) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
