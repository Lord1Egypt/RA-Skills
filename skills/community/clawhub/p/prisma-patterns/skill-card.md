## Description:

Use this skill when working with Prisma ORM in Node.js/TypeScript projects, covering schema design, migrations, query optimization, relations, transactions, and production-ready database interactions with Prisma 5+.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldath](https://clawhub.ai/user/goldath)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for Prisma ORM schema design, migration workflows, production query patterns, transactions, error handling, and testing practices in Node.js and TypeScript projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database reset and cleanup examples can cause serious data loss if copied into the wrong environment.

Mitigation: Review and adapt migration and testing snippets before use, add explicit warnings around reset commands, and require fail-closed checks that confirm test cleanup targets only a disposable test database.

Risk: Package execution snippets can run locally resolved or downloaded Prisma tooling in an uncontrolled environment.

Mitigation: Use locked local Prisma dependencies, package scripts, or npx --no-install when adapting command examples.

## Reference(s):

- [Prisma Query Optimization Patterns](references/query-optimization.md)
- [Prisma Schema Design Reference](references/schema-design.md)
- [Prisma Testing & Migrations Reference](references/testing-migrations.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Prisma schema, TypeScript, SQL, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides reusable ORM patterns and command examples that should be reviewed and adapted before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
