## Description:

Reviews database schema migrations for production safety under live traffic, focusing on destructive operations, lock-taking DDL, deploy ordering, backfills, and rollback paths without executing migrations or SQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review EF Core, Prisma, Alembic, Rails, Flyway, or raw SQL schema migrations before release. It helps identify data-loss risks, blocking DDL, unsafe rollout or rollback ordering, unbatched backfills, and missing rollback plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could be allowed to run migrations, DDL, SQL, or connect to a production database while using the skill.

Mitigation: Keep usage read-only: allow file inspection and reporting, but do not grant database credentials or migration execution permissions.

Risk: Migration safety findings depend on engine, table size, traffic, and deployment ordering context that may not be present in the migration file.

Mitigation: Require the agent to state assumptions and ask for missing production context before treating lock, rollout, rollback, or backfill findings as definitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dennisrongo/skills/migration-safety)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review report with ranked findings, file references, assumptions, and safer alternatives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only review output; the skill instructs the agent not to execute migrations, DDL, or SQL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
