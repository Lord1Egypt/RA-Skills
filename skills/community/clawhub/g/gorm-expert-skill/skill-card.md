## Description:

Gorm Expert provides GORM v2 best-practice guidance, code review support, performance tuning advice, and local helper scripts for Go database development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lynnss-ai](https://clawhub.ai/user/lynnss-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review GORM code, diagnose slow queries and N+1 patterns, design indexes and transactions, generate model or migration scaffolding, and apply multi-tenant database patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL or migration output may be unsafe for a production database if applied without review.

Mitigation: Manually review generated SQL, test migrations against representative data, and use established migration controls before execution.

Risk: The scaffolded dbcore package has tenant-isolation concerns in the security evidence.

Mitigation: Review and fix tenant enforcement before relying on the scaffold for tenant security in a real application.

Risk: Telemetry or pprof examples could expose sensitive operational data if copied into production unchanged.

Mitigation: Protect or disable diagnostic endpoints and review observability examples against production security requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lynnss-ai/skills/gorm-expert-skill)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)
- [Reference Index](artifact/references/README.md)
- [Base Model Pattern](artifact/references/base-model-pattern.md)
- [Indexing](artifact/references/indexing.md)
- [Session](artifact/references/session.md)
- [Migration](artifact/references/migration.md)
- [Observability](artifact/references/observability.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, generated Go code, SQL, JSON, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some local scripts can generate files only when output flags are supplied; generated SQL and database scaffolding should be reviewed before use.]

## Skill Version(s):

1.6.0 (source: server release evidence and changelog, released 2026-03-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
