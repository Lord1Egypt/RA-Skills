## Description:

Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis). Run queries, inspect schemas, export data. Use when user wants to query a database, explore schema, check data, export results, or debug database issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect database schemas, run diagnostic queries, export results, and troubleshoot PostgreSQL, MySQL, SQLite, MongoDB, or Redis data stores from a terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through live database connections that may expose credentials or sensitive data.

Mitigation: Use read-only, least-privilege credentials where possible, avoid placing passwords directly on command lines, and keep exports in private temporary directories.

Risk: Restore, import, migration, full export, and data-changing workflows can alter or expose production data if followed without enough verification.

Mitigation: Require explicit confirmation, verify the target database, preview commands before execution, and use transaction or rollback-oriented checks before committing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrg913427-dot/skills/hermes-db-explorer)
- [ClawHub publisher profile](https://clawhub.ai/user/lrg913427-dot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline bash, SQL, and database shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CSV, JSON, SQL dump, or database backup files when export, backup, restore, or migration workflows are used.]

## Skill Version(s):

2.4.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
