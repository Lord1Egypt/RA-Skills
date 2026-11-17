## Description:

Database Helper Pro provides SQL query-building guidance, SQLite helper code, schema inspection, CSV import/export examples, and ORM template generation for database workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to prototype local database workflows, compose SQL snippets, inspect schemas, and generate starter code for CSV import/export and ORM models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database write, delete, and schema-change operations could alter or remove production data.

Mitigation: Review generated operations before execution, require explicit confirmation for writes and deletes, and test against backups or disposable databases first.

Risk: Unsafe query-building patterns can expose databases to malformed SQL or injection when identifiers or raw conditions come from untrusted input.

Mitigation: Validate table and column identifiers, parameterize values, and restrict raw SQL fragments to trusted callers.

Risk: The provided implementation is SQLite-focused even though the skill text mentions MySQL and PostgreSQL support.

Mitigation: Confirm database-driver support and dialect differences before using generated code with MySQL or PostgreSQL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-database-helper)
- [Publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Python and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SQL snippets, SQLite helper code, schema summaries, CSV import/export examples, and ORM templates.]

## Skill Version(s):

2.0.0 (source: evidence release, SKILL.md frontmatter, hub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
