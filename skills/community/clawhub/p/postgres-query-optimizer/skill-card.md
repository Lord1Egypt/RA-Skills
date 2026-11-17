## Description:

Analyze slow PostgreSQL queries, interpret EXPLAIN ANALYZE output, identify performance bottlenecks, and recommend indexes, query rewrites, and configuration tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database engineers, and DBAs use this skill to analyze slow PostgreSQL queries and execution plans, identify likely bottlenecks, and generate practical tuning recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations may ask users to run SQL analysis or tuning statements against a live PostgreSQL database.

Mitigation: Review SQL before execution, prefer plain EXPLAIN for untrusted or state-changing statements, and run runtime analysis on staging data when possible.

Risk: Query plans, schemas, pg_stat_statements output, and connection details can expose sensitive operational or tenant data.

Mitigation: Use sanitized SQL and telemetry, and avoid sharing credentials, connection strings, personal data, tenant identifiers, or unrestricted pg_stat_statements exports.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with SQL and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include EXPLAIN plan interpretation, bottleneck rankings, CREATE INDEX statements, query rewrites, configuration suggestions, expected improvement estimates, and warnings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
