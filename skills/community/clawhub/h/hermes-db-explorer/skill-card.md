## Description: <br>
Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis). Run queries, inspect schemas, export data. Use when user wants to query a database, explore schema, check data, export results, or debug database issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect database schemas, run diagnostic queries, export data, and troubleshoot PostgreSQL, MySQL, SQLite, MongoDB, or Redis systems from a terminal workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore, import, migration, UPDATE, DELETE, DROP, or full export commands can alter databases or expose sensitive data. <br>
Mitigation: Require the agent to identify the database, environment, and exact operation, show the command or query, and obtain explicit confirmation before execution. <br>
Risk: Database credentials, connection strings, query results, and exported files may contain sensitive information. <br>
Mitigation: Use environment variables for credentials, avoid echoing secrets, limit results by default, and scope exports to the minimum data needed. <br>


## Reference(s): <br>
- [Db Explorer on ClawHub](https://clawhub.ai/lrg913427-dot/hermes-db-explorer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with shell, SQL, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify the target database and operation, limit result sets by default, and request confirmation before destructive or sensitive operations.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
