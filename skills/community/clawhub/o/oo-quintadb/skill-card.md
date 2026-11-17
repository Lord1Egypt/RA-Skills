## Description:

QuintaDB (quintadb.com). Use this skill for ANY QuintaDB request — reading, creating, updating, and deleting data. Whenever a task involves QuintaDB, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with a connected QuintaDB account can use the skill to inspect databases, forms, fields, and records, and to create, update, or delete records through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A missing CLI prerequisite can trigger downloaded installer code without a clear user approval step.

Mitigation: Review and approve CLI installation separately, verify the release, and check automatic skill synchronization before setup.

Risk: Record creation, updates, and permanent deletion can change QuintaDB data.

Mitigation: Inspect the live action schema and confirm the exact write payload or deletion target and effect before running the action.

## Reference(s):

- [QuintaDB](https://quintadb.com)
- [QuintaDB API documentation](https://quintadb.com/api/index)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-quintadb)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON connector responses and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include retrieved database, form, field, or record data.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
