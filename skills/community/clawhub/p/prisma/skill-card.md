## Description:

Designs Prisma schemas, writes type-safe queries, and helps diagnose migrations, connection pools, deployment, performance, TypeScript, raw SQL, and common Prisma error codes for Node and TypeScript projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to model Prisma schemas, choose safe migration workflows, write Prisma Client queries, troubleshoot common Prisma runtime and migration errors, and prepare Node or TypeScript deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read or maintain a preference and memory file under ~/Clawic/data/prisma/.

Mitigation: Install and use it only when persistent local Prisma preferences are acceptable, and review stored preferences when project context changes.

Risk: Examples may use npx or Prisma commands that should match the project's installed Prisma version.

Mitigation: Run Prisma through the project lockfile or pinned package scripts before applying generated commands.

Risk: Commands involving DATABASE_URL, TEST_URL, force resets, db push, or migration resets can affect the wrong database or destroy data.

Mitigation: Verify the target environment before execution and reserve destructive commands for disposable test databases or reviewed migration workflows.

Risk: Query logging can expose raw SQL parameters or sensitive production data.

Mitigation: Use thresholds and redaction for production logs, and avoid logging raw query parameters unless the data exposure has been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/prisma)
- [Clawic Prisma Skill Page](https://clawic.com/skills/prisma)
- [Skill Definition](artifact/SKILL.md)
- [Setup](artifact/setup.md)
- [Schema Design](artifact/schema.md)
- [Migrations](artifact/migrations.md)
- [Queries](artifact/queries.md)
- [Connections](artifact/connections.md)
- [Deployment](artifact/deployment.md)
- [Raw SQL](artifact/raw-sql.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with code blocks, shell command examples, configuration snippets, and Prisma schema or TypeScript code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Prisma schema changes, migration plans, Prisma Client queries, SQL snippets, deployment checks, and troubleshooting steps.]

## Skill Version(s):

1.0.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
