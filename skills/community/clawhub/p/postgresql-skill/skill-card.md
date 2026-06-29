## Description: <br>
Execute PostgreSQL database operations using psycopg2. List tables, describe schema, execute SQL queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tengshengbo](https://clawhub.ai/user/tengshengbo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect PostgreSQL tables, describe schemas, run SQL queries, generate schema summaries, and make controlled row-level changes when database access is authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The schema summary command can print sample rows from every public table, which may expose sensitive database contents. <br>
Mitigation: Use the skill only with databases the agent is allowed to inspect, prefer a read-only or limited database user, and avoid schema summaries on sensitive production databases. <br>
Risk: The skill can insert, update, and delete database records. <br>
Mitigation: Require explicit user confirmation before write operations and use least-privilege database credentials unless writes are necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tengshengbo/postgresql-skill) <br>
- [Project homepage](https://gitee.com/tengshengbo/postgre_sql_skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require PostgreSQL connection configuration through config.yaml or DB_* environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; skill frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
