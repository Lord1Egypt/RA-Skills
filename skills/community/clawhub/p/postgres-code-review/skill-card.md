## Description:

Reviews PostgreSQL code for indexing strategies, JSONB operations, connection pooling, and transaction safety. Use when reviewing SQL queries, database schemas, JSONB usage, or connection management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review PostgreSQL-related code and schema changes for performance, connection handling, JSONB usage, transaction safety, and evidence-backed SQL injection findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PgBouncer example uses permissive listener and authentication settings that may be unsafe if copied directly into an environment.

Mitigation: Bind PgBouncer only to localhost or a trusted interface, restrict exposed ports, and prefer SCRAM and TLS where applicable before using the example.

Risk: Review guidance can produce incorrect or overconfident findings if the agent does not cite the actual SQL, DDL, or binding mechanism under review.

Mitigation: Require file and line citations for performance and injection findings, and verify how SQL values are bound before reporting SQL injection risk.

## Reference(s):

- [Postgres Code Review Skill Page](https://clawhub.ai/anderskev/skills/postgres-code-review)
- [Indexes](references/indexes.md)
- [JSONB](references/jsonb.md)
- [Connections](references/connections.md)
- [Transactions](references/transactions.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown review findings with cited code locations and optional SQL, code, shell command, or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; the skill does not execute code automatically.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
