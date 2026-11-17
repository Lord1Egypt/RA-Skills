## Description:

Phy Test Data Factory generates TypeScript, Python, or SQL test data factories and seed scripts from database schemas or model definitions using local schema analysis and Faker-based values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate local test fixtures, factories, and seed data from application schemas for automated tests and database setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated teardown helpers may delete database records if run against the wrong database.

Mitigation: Review generated factory code before execution and run it only against isolated disposable test databases with least-privilege test credentials, NODE_ENV=test, and a test database allowlist before enabling clearTestData or afterAll cleanup.

Risk: Generated factory and seed code may introduce unreviewed dependencies or schema assumptions into test projects.

Mitigation: Pin Faker, factory_boy, ORM, and database dependencies, then review generated code against the target schema before committing or running it.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-test-data-factory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated TypeScript, Python, or SQL code blocks and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code is intended for review before execution; the skill source claims no external API use.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
