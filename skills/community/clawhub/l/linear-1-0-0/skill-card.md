## Description:

Query and manage Linear issues, projects, and team workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryren2024](https://clawhub.ai/user/terryren2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to inspect Linear work, create or update issues, generate standup summaries, and derive Linear-compatible Git branch names from agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Linear API key that can read and modify workspace data.

Mitigation: Use the least-privilege Linear token available, scope it to the intended workspace, and rotate it if exposed.

Risk: Write commands can create issues, add comments, assign users, and change status or priority.

Mitigation: Review generated commands and arguments before running create, comment, assign, status, or priority actions.

Risk: Unsafe input handling could modify unintended Linear data when issue IDs, titles, descriptions, project names, or comments are untrusted.

Mitigation: Avoid passing untrusted text or identifiers to the wrapper until safer GraphQL variable handling and cache handling are implemented.

## Reference(s):

- [Linear](https://linear.app)
- [Linear GraphQL API endpoint](https://api.linear.app/graphql)
- [ClawHub release page](https://clawhub.ai/terryren2024/skills/linear-1-0-0)
- [Publisher profile](https://clawhub.ai/user/terryren2024)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LINEAR_API_KEY and local curl and jq availability.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
