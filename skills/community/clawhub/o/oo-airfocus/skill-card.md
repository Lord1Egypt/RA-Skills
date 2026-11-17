## Description:

Operate airfocus through the user's OOMOL-connected account for reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to find and manage airfocus workspaces and items through their connected account. It supports read actions as well as creating, updating, and deleting items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute remote code without separate installation approval.

Mitigation: Review and approve CLI installation separately, including installed skill changes; prefer a pinned, verified release.

Risk: The connector mediates access to the connected airfocus account, including item writes and permanent deletion.

Mitigation: Limit connected-account permissions and confirm the exact targets and effects of writes and deletions.

## Reference(s):

- [airfocus](https://airfocus.com/)
- [airfocus API documentation](https://developer.airfocus.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured airfocus data and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected airfocus account and the selected action.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
