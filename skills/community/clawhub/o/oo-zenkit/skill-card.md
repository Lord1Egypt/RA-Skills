## Description:

Zenkit (zenkit.com). Use this skill for ANY Zenkit request — reading, creating, updating, and deleting data. Whenever a task involves Zenkit, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search and read Zenkit data, inspect workspaces and collections, and create, update, or delete entries in their connected Zenkit account through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, the documented setup runs a remote installer whose contents were not inspected.

Mitigation: Review and approve CLI installation separately, preferably using a pinned, verified release.

Risk: The hosted connector implementation and remote installer were not inspected.

Mitigation: Connect only the intended Zenkit account and retain the documented confirmation requirement for write and destructive actions.

## Reference(s):

- [Zenkit API documentation](https://base.zenkit.com/docs/api/)
- [Zenkit](https://zenkit.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with oo CLI shell commands and Zenkit results in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports reads, writes, and destructive actions; writes and deletes require user confirmation.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
