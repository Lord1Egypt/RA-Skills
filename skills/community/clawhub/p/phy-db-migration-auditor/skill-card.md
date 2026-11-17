## Description:

Audits local database migration files for risky schema changes, rollback gaps, backward-compatibility issues, and lock-heavy operations across Alembic, Flyway, Django, Rails ActiveRecord, and Prisma Migrate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review database migrations before deployment, identify schema changes that can cause downtime or data loss, and produce pre-deploy checks and rollback material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect local migration files and source files to find schema risks and code references.

Mitigation: Run it only in workspaces where those local files may be reviewed by the agent and avoid including unrelated sensitive source material.

Risk: Generated rollback scripts may be incomplete for a specific production database state.

Mitigation: Treat rollback scripts as review material; require database-owner approval and staging tests before running them.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-db-migration-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, checklists, and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated rollback scripts are review material and should be tested and approved before use.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
