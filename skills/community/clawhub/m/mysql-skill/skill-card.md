## Description:

MySQL 数据库管理技能。通过自然语言查询、管理 MySQL 数据库，支持 SELECT/INSERT/UPDATE/DELETE、表管理、备份恢复等操作。当用户提到 MySQL、数据库查询、建表、数据备份时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database administrators, and data analysts use this skill to turn natural-language requests into MySQL queries, table-management operations, backups, restores, and optimization checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose SQL and shell commands that alter data, schema, backups, or restores.

Mitigation: Require manual review and explicit confirmation before running UPDATE, DELETE, ALTER, restore, or production backup commands.

Risk: Database credentials may be exposed or over-privileged if stored casually or used through broad accounts.

Mitigation: Use least-privilege accounts, prefer read-only credentials for analysis, avoid long-lived password environment variables, and protect credential files with restrictive permissions.

Risk: Installation and database administration commands may require privileged local or database access.

Mitigation: Install only in environments where agent-assisted MySQL administration is intended and restrict execution to approved operators.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryanlee-gemini/skills/mysql-skill)
- [Publisher profile](https://clawhub.ai/user/ryanlee-gemini)
- [MySQL documentation](https://dev.mysql.com/doc/)
- [MySQL optimization documentation](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [MySQL Workbench](https://www.mysql.com/products/workbench/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL, shell, and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include database-changing SQL or shell commands that require manual review before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
