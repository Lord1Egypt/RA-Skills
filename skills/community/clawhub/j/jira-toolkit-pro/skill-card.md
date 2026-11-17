## Description:

Jira 事务工具包专业版 helps agents manage Jira issues and project workflows with JQL queries, agile board and sprint operations, workflow automation, bulk field and component management, and cross-project dependency tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and enterprise teams use this skill to inspect, create, query, export, and automate Jira work items through natural-language agent workflows. It is intended for Jira administration and project-management tasks where controlled bulk operations, workflow changes, and audit-aware collaboration are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to use Jira CLI/API credentials and local command execution with broad access.

Mitigation: Use credentials with the minimum Jira permissions needed, keep credentials under approved controls, require previews before execution, and prevent arbitrary local file reads or writes.

Risk: Bulk Jira creates, edits, transitions, and workflow changes could apply incorrect changes at scale.

Mitigation: Require explicit confirmation for creates, edits, transitions, and bulk actions; test bulk operations on a small set before wider execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jira-toolkit-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Jira operation summaries, command previews, configuration examples, execution logs, and structured status responses.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
