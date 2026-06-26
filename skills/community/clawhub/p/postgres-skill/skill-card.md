## Description: <br>
PostgreSQL 数据库管理技能。通过自然语言查询、管理 PostgreSQL 数据库，支持复杂查询、性能分析、JSON 操作、全文搜索等高级功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and database administrators use this skill to draft PostgreSQL queries and operational commands for advanced SQL analysis, JSONB work, full-text search, performance review, backups, and restores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL or administrative commands can change, restore, or expose database data if run against the wrong database or with broad privileges. <br>
Mitigation: Use least-privilege or read-only database accounts where possible, confirm the target host and database, and manually approve UPDATE, CREATE INDEX, backup, restore, and sudo installation steps. <br>
Risk: Database credentials or connection strings may be exposed if pasted into chats, logs, or generated command examples. <br>
Mitigation: Avoid sharing real passwords or full connection strings; prefer environment-specific secret handling and redact credentials before asking for help. <br>


## Reference(s): <br>
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) <br>
- [PostgreSQL Performance Optimization](https://wiki.postgresql.org/wiki/Performance_Optimization) <br>
- [PostgreSQL JSON Types](https://www.postgresql.org/docs/current/datatype-json.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL and shell command code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PostgreSQL client installation guidance, connection configuration, SQL statements, psql usage, pg_dump or pg_restore commands, and review notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
