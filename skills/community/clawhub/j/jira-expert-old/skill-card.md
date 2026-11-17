## Description:

Atlassian Jira expert for creating and managing projects, planning, product discovery, JQL queries, workflows, custom fields, automation, reporting, dashboards, and technical Jira operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omesh06](https://clawhub.ai/user/omesh06)

### License/Terms of Use:

MIT-0

## Use Case:

Jira administrators, project managers, scrum masters, and developers use this skill to plan and configure Jira projects, build JQL queries, design workflows, prepare automation rules, and generate reporting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation examples may perform Jira-changing actions, auto-approvals, outbound notifications, or webhook calls in a live site.

Mitigation: Review rules with Jira administrators and data-governance owners, then test them in a non-production project before enabling them broadly.

Risk: Bulk edits or transitions can affect unintended issues when a JQL filter is too broad.

Mitigation: Preview matching issues, run small batches first, and require administrator approval for production bulk operations.

## Reference(s):

- [Jira Automation Reference](references/AUTOMATION.md)
- [Jira Workflows Reference](references/WORKFLOWS.md)
- [Jira Automation Examples](references/automation-examples.md)
- [JQL Query Examples](references/jql-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Jira MCP command examples, JQL snippets, and optional JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Jira-changing actions; review production automation, bulk changes, notifications, and webhooks before execution.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
