## Description:

Execute PostgreSQL database operations using psycopg2, including listing tables, describing schemas, and running SQL queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tengshengbo](https://clawhub.ai/user/tengshengbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect PostgreSQL databases, retrieve schema details, run SQL queries, and make reviewed data changes through a Python command-line interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose database query results, schema details, and sample rows to an agent.

Mitigation: Use a dedicated least-privilege PostgreSQL role and avoid production databases unless agent access to returned data is acceptable.

Risk: The skill supports INSERT, UPDATE, and DELETE operations and its advertised SQL safety checks are incomplete.

Mitigation: Require explicit human review before write operations and treat built-in SQL checks as a supporting control, not the primary approval mechanism.

Risk: Database credentials may be configured in local files.

Mitigation: Prefer environment-injected secrets, keep config files out of version control, and do not commit credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tengshengbo/skills/postgresql-skill)
- [Source homepage](https://gitee.com/tengshengbo/postgre_sql_skill)
- [Packaged README](artifact/README.md)
- [Packaged skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON and text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Database results may include schema details, query rows, sample rows, and affected-row counts.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
