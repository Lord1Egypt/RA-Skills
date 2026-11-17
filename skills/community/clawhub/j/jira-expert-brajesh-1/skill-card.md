## Description:

Atlassian Jira expert for creating and managing projects, planning, product discovery, JQL queries, workflows, custom fields, automation, reporting, and all Jira features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omesh06](https://clawhub.ai/user/omesh06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, Scrum Masters, and Jira administrators use this skill to plan and configure Jira projects, write JQL, design workflows, create dashboards and reports, and draft Jira automation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Jira administration and automation changes can affect project permissions, workflows, notifications, or large sets of issues.

Mitigation: Review proposed Jira MCP commands before execution and test workflow or automation changes in a sandbox before applying them to production projects.

Risk: Bulk edits or broad JQL filters can update unintended issues and may be difficult to reverse.

Mitigation: Preview bulk operations, confirm the JQL result set, and apply changes in small batches when possible.

Risk: Webhook, Slack, Teams, or email automation payloads may expose issue descriptions, user identities, or customer data to unapproved systems.

Mitigation: Limit notification and webhook payloads to approved destinations and exclude sensitive Jira fields unless the recipient system is authorized.

## Reference(s):

- [Jira Automation Reference](references/AUTOMATION.md)
- [Jira Workflows Reference](references/WORKFLOWS.md)
- [Jira Automation Examples](references/automation-examples.md)
- [JQL Query Examples](references/jql-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Jira MCP command examples, JQL snippets, workflow validation guidance, and automation rule patterns.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
