## Description:

Manage ClickUp data by reading, creating, updating, and deleting items through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to read and manage ClickUp workspaces, tasks, comments, lists, folders, and related data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run downloaded code automatically if the oo CLI is missing; the remote installer is unverified.

Mitigation: Review the CLI installation source and use a pinned, verified release where possible. Keep explicit confirmation before actions that change or delete ClickUp data.

## Reference(s):

- [ClickUp skill release](https://clawhub.ai/oomol/skills/oo-clickup)
- [ClickUp](https://clickup.com)
- [ClickUp API documentation](https://developer.clickup.com/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and payloads, shell command examples, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results depend on the selected ClickUp operation and the connected account's access.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
