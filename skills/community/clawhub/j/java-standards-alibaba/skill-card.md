## Description:

Use when writing or modifying Java code - enforces Alibaba Java Development Guidelines (Songshan edition) for naming, formatting, OOP, collections, concurrency, control statements, exceptions, logging, MySQL, security, and project structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endcy](https://clawhub.ai/user/endcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate, modify, refactor, and review Java code against Alibaba Java Development Guidelines, including database, API, testing, logging, security, and project-structure conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill applies Alibaba Java Development Guidelines broadly, which may conflict with established repository conventions or project-specific standards.

Mitigation: Confirm the desired style standard before use and override the skill when local conventions take precedence.

Risk: Database, SQL, and schema guidance can affect production data if applied without review.

Mitigation: Require human review for database changes and use backups, migrations, transactions, and environment-specific testing before deployment.

Risk: Most detailed reference material is in Chinese, which can make interpretation harder for teams that do not read Chinese.

Mitigation: Have bilingual reviewers or translated project standards confirm important decisions before accepting generated code or reviews.

## Reference(s):

- [Skill page](https://clawhub.ai/endcy/skills/java-standards-alibaba)
- [README](README.md)
- [API contract guidelines](references/api-contract.md)
- [Code format guidelines](references/code-format.md)
- [Collections guidelines](references/collections.md)
- [Comment guidelines](references/comments.md)
- [Concurrency guidelines](references/concurrency.md)
- [Constants guidelines](references/constants.md)
- [Control-flow guidelines](references/control-flow.md)
- [Date and time guidelines](references/date-time.md)
- [Design guidelines](references/design.md)
- [Exception guidelines](references/exceptions.md)
- [Logging guidelines](references/logging.md)
- [MySQL DDL guidelines](references/mysql-ddl.md)
- [MySQL index guidelines](references/mysql-index.md)
- [MySQL SQL guidelines](references/mysql-sql.md)
- [Naming guidelines](references/naming.md)
- [OOP guidelines](references/oop.md)
- [ORM guidelines](references/orm.md)
- [Other Java guidelines](references/others.md)
- [Project structure guidelines](references/project-structure.md)
- [Security guidelines](references/security.md)
- [Unit test guidelines](references/unit-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, SQL, API, testing, and review recommendations when relevant to the user's Java task.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no hidden execution, data access, persistence, or exfiltration behavior was reported by the security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
