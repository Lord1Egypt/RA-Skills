## Description: <br>
This skill helps agents produce Chinese Feishu automation plans, examples, and templates for scheduled messages, reports, Bitable operations, calendar events, and approval workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Feishu workspace administrators use this skill to design automations for message delivery, recurring reports, Bitable data changes, calendar events, and approval reminders. It is intended to return Chinese guidance, code examples, permission checklists, and reusable output templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Feishu permissions can expose private messages, documents, calendars, approvals, contacts, or business records. <br>
Mitigation: Grant only the scopes required for the workflow, avoid private-message access unless it is necessary, and review permissions before deployment. <br>
Risk: App Secret values and tenant access tokens can leak through logs, examples, or shared configuration. <br>
Mitigation: Store secrets securely, keep tokens out of logs and generated output, and mask sensitive values during troubleshooting. <br>
Risk: Scheduled automations that approve, delete, or modify records can make business changes without timely human review. <br>
Mitigation: Test each workflow with limited data, require review for destructive or approval-related actions, and monitor scheduled runs before broad rollout. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/qqyougitcom/mimo-feishu-automation) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [Detailed Feishu automation examples](references/details.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Chinese Markdown with code blocks, tables, checklists, and automation templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs commonly include required Feishu scopes, Cron triggers, data sources, transformation steps, target destinations, and safety notes.] <br>

## Skill Version(s): <br>
1.3.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
