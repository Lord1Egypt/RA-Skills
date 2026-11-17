## Description:

Linear同步(专业版) helps agents operate Linear from the command line for issue lifecycle management, batch operations, documents, milestones, GraphQL queries, and Git-linked workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering leads, and project managers use this skill to have an agent inspect and change Linear issues, projects, documents, milestones, and related Git workflow state through CLI and GraphQL commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using this skill can make broad live changes to Linear workspace data, including issue, document, project, team, and GraphQL mutation operations.

Mitigation: Require the agent to show the exact target object and proposed command or mutation, then obtain explicit approval before execution.

Risk: Confirmation-bypassing delete examples such as delete commands with -y can remove Linear records without an interactive safety check.

Mitigation: Avoid -y delete flows unless recovery options and permissions have been confirmed, and prefer a separate approval step for destructive commands.

Risk: Linear API keys and tokens are required for use and could expose workspace access if mishandled.

Mitigation: Use Linear's authentication flow or environment variables, keep credentials out of code and shared logs, and apply the minimum permissions needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/linear-sync-tool-pro)
- [Linear GraphQL API endpoint](https://api.linear.app/graphql)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and JSON-shaped command result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run Linear CLI and GraphQL operations that read, create, update, or delete workspace data.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
