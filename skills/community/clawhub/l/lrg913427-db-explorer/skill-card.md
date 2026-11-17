## Description:

Db Explorer helps agents connect to PostgreSQL, MySQL, SQLite, MongoDB, and Redis databases to inspect schemas, run bounded queries, export results, and debug database issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to explore database structure, run diagnostic or read-only queries, export bounded result sets, and prepare cautious database maintenance commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database exploration can expose or alter sensitive production data when run with broad credentials.

Mitigation: Use least-privileged database accounts, prefer read-only operations, and require explicit confirmation with target verification before any write, restore, import, migration, or full export.

Risk: Credential examples that place passwords in command lines can leak secrets through shell history, process listings, or logs.

Mitigation: Use environment variables, prompts, or secret managers instead of pasting real passwords directly into commands.

Risk: Unbounded exports and Redis key scans can create operational load or expose more data than intended.

Mitigation: Limit query results by default, scope exports narrowly, and avoid Redis KEYS on production or shared Redis instances.

## Reference(s):

- [Db Explorer ClawHub Release](https://clawhub.ai/lrg913427-dot/skills/lrg913427-db-explorer)
- [lrg913427-dot Publisher Profile](https://clawhub.ai/user/lrg913427-dot)
- [MongoDB Shell Documentation](https://www.mongodb.com/docs/shell/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with SQL and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database queries, schema summaries, export commands, diagnostic commands, and safety confirmation prompts.]

## Skill Version(s):

2.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
