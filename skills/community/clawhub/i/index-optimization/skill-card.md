## Description:

Analyzes query patterns for a target table or collection, designs reusable indexes, and iterates with EXPLAIN validation in full or single-query workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiang-zx](https://clawhub.ai/user/jiang-zx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to inventory query usage for a target table or collection, design a minimal reusable index set, justify schema changes, validate plans with EXPLAIN, and document rollback steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose or execute schema-changing index creation or deletion without explicit approval in its default no-confirmation mode.

Mitigation: Use explicit confirmation-required mode, review each DDL statement before execution, and require intentional approval before any index creation or deletion.

Risk: DROP INDEX or dropIndex operations can degrade production workloads if the replacement index has not been validated.

Mitigation: Do not allow automatic index deletion on production databases; validate replacement plans with EXPLAIN and keep rollback DDL before any approved drop.

Risk: Discovery and EXPLAIN steps may require database access and could expose or affect sensitive environments if run with broad credentials.

Mitigation: Run discovery and EXPLAIN against development or staging targets with read-only credentials until a specific reviewed DDL change is approved.

## Reference(s):

- [Index Rules](references/index-rules.md)
- [MySQL EXPLAIN Guide](references/mysql-explain-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/jiang-zx/skills/index-optimization)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with SQL or MongoDB DDL, EXPLAIN summaries, clickable code-location links, and rollback commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SQL migration files under docs/sql for SQL database workflows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
