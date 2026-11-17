## Description:

monday (monday.com). Use this skill for ANY monday request — reading, creating, updating, and deleting data. Whenever a task involves monday, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using monday.com through an OOMOL-connected account can ask an agent to inspect boards, items, workspaces, users, documents, and activity, or to create and update monday data. The skill directs the agent to inspect an action's schema and confirm state-changing operations before running them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run downloaded CLI installer code, and the exact local changes from remote installers are unverified.

Mitigation: Review and verify the CLI installation and automatic skill synchronization before enabling the skill; install only after checking the source and resulting local changes.

Risk: Some actions can modify, archive, or delete monday data.

Mitigation: Inspect the live action schema, confirm the exact target and effect before state-changing actions, and require explicit confirmation for destructive actions.

## Reference(s):

- [monday API documentation](https://developer.monday.com/api-reference/docs)
- [monday.com](https://monday.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON requests and responses with natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read monday data or change account data; destructive actions can archive, remove, or overwrite data.]

## Skill Version(s):

1.0.9 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
