## Description:

Interact with Linear for issue tracking, including creating, updating, listing, searching, assigning, commenting on, and changing the status of issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emrekilinc](https://clawhub.ai/user/emrekilinc)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to manage Linear issue workflows from an AI assistant, including reviewing assigned work, creating issues, updating fields, and adding comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create issues, update issue fields, and add comments in a shared Linear workspace.

Mitigation: Require explicit human confirmation before create, update, or comment actions, especially in production workspaces.

Risk: The skill uses a Linear API key from an environment variable or local credentials file.

Mitigation: Use a least-privilege token where possible and protect any credentials file with restrictive permissions.

Risk: Weak input and credential safeguards may expose the workspace to malformed requests or unintended changes.

Mitigation: Validate issue IDs, team IDs, state IDs, assignee IDs, and priority values, and use GraphQL variables or proper JSON encoding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emrekilinc/skills/linear-issues)
- [Linear API examples](references/api-examples.md)
- [Linear API settings](https://linear.app/settings/api)
- [Linear GraphQL endpoint](https://api.linear.app/graphql)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [Human-readable command output or raw JSON from Linear API-backed shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Linear API key provided by LINEAR_API_KEY or a local credentials file.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
