## Description:

PostgreSQL database patterns for query optimization, schema design, indexing, and security.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a PostgreSQL reference for writing SQL and migrations, designing schemas, selecting indexes, troubleshooting slow queries, implementing Row Level Security, and setting up connection pooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL or configuration changes can affect production database availability, permissions, or data integrity.

Mitigation: Review generated SQL before use, require explicit approval for production-impacting changes, and prepare backups and rollback plans before destructive migrations.

Risk: Query-stat and diagnostic outputs can expose credentials or sensitive query text if copied into endpoints, logs, or external systems.

Mitigation: Filter, redact, or hash query text before sharing it outside the database administration context.

Risk: User-provided secrets can be repeated in generated examples or warnings.

Mitigation: Refer to credentials by description and use parameters, environment variables, or secret-management patterns instead of echoing secret values.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/snazar-faberlens/skills/postgres-hardened)
- [Faberlens PostgreSQL safety evaluation](https://faberlens.ai/explore/postgres)
- [Faberlens publisher site](https://faberlens.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with SQL, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PostgreSQL query patterns, schema guidance, index recommendations, RLS examples, anti-pattern checks, and operational safety guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
