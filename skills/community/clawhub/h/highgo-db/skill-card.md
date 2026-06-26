## Description: <br>
Connects an agent to HighGo DB through a bundled custom psycopg2-style driver and executes SQL using a Python helper script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ygp987](https://clawhub.ai/user/ygp987) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to let an agent connect to HighGo DB, run SQL queries or administrative statements, and return query results. It is intended for environments where the operator deliberately grants the agent database access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute arbitrary SQL against a HighGo database when given valid connection details. <br>
Mitigation: Use a least-privilege or read-only database account where possible and require human review before running SQL that changes data, schema, permissions, or database configuration. <br>
Risk: Database credentials may be exposed if real passwords are placed directly in prompts, shell history, logs, or command-line DSNs. <br>
Mitigation: Use secret-management mechanisms or short-lived credentials and avoid embedding production passwords in prompt text or saved command examples. <br>
Risk: The skill depends on legacy Python 2.7 and bundled or external psycopg2-compatible driver components, which may not match the target host. <br>
Mitigation: Validate the driver source and runtime dependencies in a controlled environment before connecting to production databases. <br>


## Reference(s): <br>
- [HighGo DB skill page](https://clawhub.ai/ygp987/highgo-db) <br>
- [Publisher profile](https://clawhub.ai/user/ygp987) <br>
- [Driver information](references/driver_info.md) <br>
- [psycopg project](https://psycopg.org/) <br>
- [PostgreSQL documentation](https://www.postgresql.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON results from the query helper, plus Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [SQL execution depends on a supplied DSN, SQL string or SQL file path, and an optional driver path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
