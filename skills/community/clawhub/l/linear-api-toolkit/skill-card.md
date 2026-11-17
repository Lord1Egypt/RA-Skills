## Description:

This skill helps agents manage project-management work items, projects, teams, cycles, labels, comments, relations, workflow states, and views through GraphQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and automation teams use this skill to draft and run GraphQL workflows for creating, updating, querying, and organizing project-management records. It is intended for project management, task planning, progress tracking, and team collaboration, not personnel performance evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a project-management API key that can read and change work items, projects, labels, cycles, views, and comments.

Mitigation: Use a scoped API token, store it outside version control, and grant only the project-management permissions required for the task.

Risk: GraphQL mutations can modify or archive project-management records.

Mitigation: Review generated mutations, target IDs, and filters before execution, especially for bulk updates or archive operations.

Risk: The release evidence notes an overbroad command-execution permission even though the documented API workflow does not clearly need shell execution.

Mitigation: Be cautious granting exec access and prefer running API workflows in an agent session with minimal tool permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/linear-api-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with GraphQL and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GraphQL queries and mutations, API key setup guidance, and project-management workflow steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
