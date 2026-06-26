## Description: <br>
Feishu Suite helps an agent manage Feishu messages, documents, calendars, tasks, and bitable records from a single workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a85012712](https://clawhub.ai/user/a85012712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to coordinate Feishu workspace activity, including sending messages, editing documents, managing calendar events, tracking tasks, and updating bitable records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate across messages, documents, calendars, tasks, and bitable records in a Feishu workspace. <br>
Mitigation: Install it only for workflows that need broad Feishu authority and configure the least-privileged Feishu app scopes that still support the intended tasks. <br>
Risk: Write actions could affect recipients, documents, calendar events, tasks, or table records if the agent targets the wrong object. <br>
Mitigation: Use explicit Feishu-specific requests and confirm recipients, target documents, calendars, tasks, and tables before write operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a85012712/jw-feishu-suite) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, API calls] <br>
**Output Format:** [Markdown guidance with Feishu operation examples and permission-scope details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or request Feishu messages, document updates, calendar entries, task changes, and bitable record changes after user authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
