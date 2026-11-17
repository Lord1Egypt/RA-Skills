## Description:

Manage Linear projects, issues, and tasks via a bundled Node.js CLI and the official Linear API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matrixy](https://clawhub.ai/user/matrixy)

### License/Terms of Use:

MIT

## Use Case:

Developers and project teams use this skill to let an agent read, create, update, and organize Linear issues, projects, comments, labels, states, and related workflow data through a local CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and update Linear work items using the user's LINEAR_API_KEY.

Mitigation: Use a dedicated least-privilege API key, keep the token out of issues and comments, and revoke it when automation no longer needs access.

Risk: Incorrect or broad mutations could unintentionally change Linear issues, projects, or comments.

Mitigation: Fetch current state first, prefer narrow updates, and review proposed bulk changes before allowing execution.

Risk: The documentation claims a few Linear resource types that the current CLI does not actually support.

Mitigation: Confirm the intended task is covered by the listed CLI commands before relying on the skill for that workflow.

## Reference(s):

- [Linear API Reference](references/API.md)
- [ClawHub Skill Page](https://clawhub.ai/matrixy/skills/linear-skill)
- [Project Homepage](https://github.com/MaTriXy/linear-skill)
- [Linear GraphQL API](https://api.linear.app/graphql)
- [Linear API Key Settings](https://linear.app/settings/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Linear object IDs, state changes, assignees, comments, and follow-up actions; requires LINEAR_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
