## Description: <br>
Use this skill when working with Prisma ORM in Node.js/TypeScript projects; it covers schema design, migrations, query optimization, relations, transactions, and best practices for production-ready database interactions with Prisma 5+. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goldath](https://clawhub.ai/user/goldath) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design Prisma schemas, plan migrations, write relation-heavy queries, handle transactions and errors, and tune Prisma usage in Node.js and TypeScript applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prisma reset, raw delete, and bulk delete examples can erase data if run against a production or shared database. <br>
Mitigation: Confirm DATABASE_URL points to a disposable local, development, or isolated test database before running commands; require backups and explicit approval before using destructive examples on shared data. <br>


## Reference(s): <br>
- [Prisma Query Optimization Patterns](references/query-optimization.md) <br>
- [Prisma Schema Design Reference](references/schema-design.md) <br>
- [Prisma Testing & Migrations Reference](references/testing-migrations.md) <br>
- [ClawHub release page](https://clawhub.ai/goldath/prisma-patterns) <br>
- [Publisher profile](https://clawhub.ai/user/goldath) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Prisma schema, TypeScript, SQL, JSON, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database commands and examples that should be reviewed against the active DATABASE_URL before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
