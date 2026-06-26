## Description: <br>
Atlassian Jira expert for creating and managing projects, planning, product discovery, JQL queries, workflows, custom fields, automation, reporting, and all Jira features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omesh06](https://clawhub.ai/user/omesh06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Jira administrators, project leads, Scrum Masters, product managers, and developers use this skill to plan and configure Jira projects, build JQL queries, design workflows, create dashboards, define automation rules, and validate workflow definitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad Jira administration and automation changes that may affect projects, workflows, permissions, notifications, and reports. <br>
Mitigation: Use least-privilege Jira or service accounts, test changes in a sandbox, and require review before applying project-wide or organization-wide configuration changes. <br>
Risk: Bulk JQL operations can unintentionally update or transition the wrong issues. <br>
Mitigation: Preview JQL results, review small batches before applying changes at scale, and confirm the filter matches only intended issues. <br>
Risk: Automation examples may send issue details to email, chat, GitHub, Confluence, or webhooks. <br>
Mitigation: Use only approved destinations and avoid sending descriptions, email addresses, customer data, secrets, or security-sensitive details unless those destinations are authorized. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/omesh06/jira-expert-old) <br>
- [Jira Automation Reference](references/AUTOMATION.md) <br>
- [Jira Workflows Reference](references/WORKFLOWS.md) <br>
- [Jira Automation Examples](references/automation-examples.md) <br>
- [JQL Query Examples](references/jql-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JQL, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Jira MCP command examples, JQL snippets, automation recipes, workflow validation reports, and configuration guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
