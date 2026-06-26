## Description: <br>
Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis), run queries, inspect schemas, export data, and debug database issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they need an agent to help inspect database schemas, run diagnostic queries, export query results, or prepare backup and restore commands across common database systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database commands can expose, modify, export, or delete sensitive data if run with broad credentials. <br>
Mitigation: Use read-only or narrowly scoped credentials where possible, review every generated command before execution, and require explicit confirmation before any write, restore, migration, or destructive operation. <br>
Risk: Exported CSV, JSON, SQL, or backup files may contain sensitive records. <br>
Mitigation: Store exports only in approved locations, protect access to generated files, and delete temporary exports or backups when they are no longer needed. <br>
Risk: Unbounded queries or large exports can overload production databases. <br>
Mitigation: Apply result limits by default, test commands against low-risk environments first, and avoid production-scale dumps unless the user explicitly requests them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lrg913427-dot/lrg-db-explorer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database CLI commands, SQL snippets, export paths, and backup or restore procedures for user review before execution.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
