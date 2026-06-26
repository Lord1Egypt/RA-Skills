## Description: <br>
Query and explore Microsoft SQL Server databases using sqlcmd. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fchrulk](https://clawhub.ai/user/fchrulk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to connect to Microsoft SQL Server with sqlcmd, inspect schemas, run bounded ad-hoc T-SQL queries, and analyze tabular data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses SQL Server connection details and can run database queries through sqlcmd. <br>
Mitigation: Use a read-only or least-privileged database account where possible, and review any requested write, delete, schema, or administrative query before allowing it to run. <br>
Risk: Queries can expose credentials or sensitive database contents if command output or environment values are printed carelessly. <br>
Mitigation: Do not print, echo, or reveal connection strings or credential environment variables; limit query output to the minimum needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fchrulk/mssql-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/fchrulk) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with bash and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MSSQL_HOST, MSSQL_USER, MSSQL_PASSWORD, MSSQL_DB, and optional MSSQL_SQLCMD environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
