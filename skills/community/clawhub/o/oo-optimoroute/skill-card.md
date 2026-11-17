## Description:

OptimoRoute (optimoroute.com). Use this skill for any OptimoRoute request, including reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams use an assistant with this skill to retrieve, create, update, and delete OptimoRoute orders through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run a downloaded installer and may add changes to the agent environment.

Mitigation: Prefer an already trusted oo CLI; otherwise verify and pin the installation, and check whether it adds other agent skills before proceeding.

Risk: Creating, updating, or deleting orders changes OptimoRoute account data.

Mitigation: Confirm the exact payload and effect before writes, and obtain explicit approval for deletions.

## Reference(s):

- [OptimoRoute](https://optimoroute.com/)
- [OptimoRoute API documentation](https://optimoroute.com/api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with oo CLI commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers read-only retrieval and order changes; the skill requires confirmation for writes and explicit approval for deletions.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
