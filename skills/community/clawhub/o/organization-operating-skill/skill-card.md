## Description: <br>
A general-purpose skill for connecting the organization platform with external agents. Use it to access user, organization, post, and activity APIs, and to complete authentication, organization operations, content publishing, and activity workflows whenever an agent needs to execute actions through the platform APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urzeye](https://clawhub.ai/user/urzeye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to authenticate with the ZingUp/Groupoo organization platform, manage user and organization workflows, publish posts, and save, publish, search, or sign up for activities through platform APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live production organization changes, publish public posts, publish or remove activities, and create signups. <br>
Mitigation: Use --env test or an explicit test base URL during development, and require human approval before any production organization change, public post, activity publish/cancel/delete, or signup. <br>
Risk: Reusable session tokens may be saved outside the skill repository. <br>
Mitigation: Use a dedicated --session-file for each account, protect those files, and delete or rotate them when access is no longer needed. <br>
Risk: The generic request command can issue arbitrary authenticated API requests. <br>
Mitigation: Limit generic request usage to reviewed endpoints and require human approval before using it against production or sensitive accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/urzeye/organization-operating-skill) <br>
- [README](README.md) <br>
- [Auth and Environment Reference](references/auth_reference.md) <br>
- [Organization Reference](references/org_reference.md) <br>
- [Content Reference](references/content_reference.md) <br>
- [Activity Reference](references/activity_reference.md) <br>
- [API Reference Index](references/api_reference.md) <br>
- [Capability Inventory](references/capability_inventory.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses saved session files outside the skill repository; API responses vary by selected environment and account permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
