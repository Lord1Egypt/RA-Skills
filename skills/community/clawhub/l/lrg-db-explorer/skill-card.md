## Description:

Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis). Run queries, inspect schemas, export data. Use when user wants to query a database, explore schema, check data, export results, or debug database issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect database schemas, run bounded queries, export selected data, and diagnose database health across PostgreSQL, MySQL, SQLite, MongoDB, and Redis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated database commands may expose credentials in command arguments, shell history, or transcripts.

Mitigation: Use least-privilege credentials, prefer environment variables or interactive prompts for secrets, and redact connection strings before sharing logs.

Risk: Exports, backups, imports, restores, and migrations can move sensitive or production data to unsafe locations or alter database state.

Mitigation: Review each command, avoid shared temporary paths for production data, and require separate explicit confirmation before full-table exports, imports, restores, migrations, or writes.

Risk: Unbounded queries can expose more data than intended or affect database performance.

Mitigation: Use read-only credentials where possible and keep query limits unless the user explicitly requests a broader result set.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lrg913427-dot/skills/lrg-db-explorer)
- [Publisher Profile](https://clawhub.ai/user/lrg913427-dot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline SQL and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Database commands should be reviewed before execution, with read-only credentials and explicit confirmation for writes, imports, restores, and full-table exports.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
