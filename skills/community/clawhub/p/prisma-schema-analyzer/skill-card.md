## Description:

Analyze Prisma schemas for performance, relation design, index strategy, migration safety, and query optimization - audit schema.prisma for production readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Prisma schema.prisma files for production readiness, including model design, relation behavior, indexing, migration safety, and Prisma Client query patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migration-diff step uses an unpinned Prisma CLI invocation through npx, which can unexpectedly download code.

Mitigation: Run Prisma from a locally installed, lockfile-controlled project dependency or another local-only invocation, using ordinary project permissions and avoiding unnecessary production credentials.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis report with findings, schema metrics, and recommended Prisma changes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include shell commands for local schema, migration, and Prisma Client usage discovery; does not create files by itself.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
