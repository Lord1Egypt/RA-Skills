## Description:

Uses the MySQL CLI to help agents connect to MySQL databases, run queries and data changes, inspect schemas, manage imports and exports, and format results as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[429668385](https://clawhub.ai/user/429668385)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to have an agent prepare and run MySQL CLI commands for querying data, inspecting schemas, generating reports, importing and exporting data, and troubleshooting database connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad database writes, bulk import or export, script execution, schema changes, and administrative actions.

Mitigation: Use it only with explicit user-directed database targets, least-privilege accounts, reviewed SQL, staging systems or backups for writes, and confirmation before write, import, export, schema, script, or admin actions.

Risk: Credential-handling examples may expose secrets if passwords are placed in commands, process lists, shell history, or unsecured config files.

Mitigation: Prefer interactive password prompts, mysql_config_editor, or an approved secret manager; secure any client configuration files and avoid command-line passwords.

Risk: Use against production or sensitive databases could cause data loss, disclosure, or service impact.

Mitigation: Avoid production use unless the agent is required to request confirmation before risky actions and the operator has appropriate backups, access controls, and change-review procedures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/429668385/skills/mysql-database-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL, shell command, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON output patterns for query results and safety guidance for database credentials and write operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
