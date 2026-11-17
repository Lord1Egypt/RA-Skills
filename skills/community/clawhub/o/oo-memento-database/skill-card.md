## Description:

Memento Database (mementodatabase.com). Use this skill for ANY Memento Database request — reading, creating, updating, and deleting data. Whenever a task involves Memento Database, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users with a connected Memento Database account can read, search, create, update, and delete database entries through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded code that has not been verified.

Mitigation: Review setup and independently verify the oo CLI source and version before running it.

Risk: CLI setup may introduce broader agent changes through automatic skill synchronization.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI, and approve local changes separately.

Risk: Write and delete actions change Memento Database records.

Mitigation: Confirm the exact payload and effect before running any write or destructive action.

## Reference(s):

- [Memento Database](https://mementodatabase.com/)
- [Memento Database API documentation](https://mementodatabase.docs.apiary.io/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Guidance]

**Output Format:** [JSON connector responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific responses; write and delete actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
