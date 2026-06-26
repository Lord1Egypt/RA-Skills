## Description: <br>
Manage Monday.com workspaces, boards, items, teams, and documents. Create projects, manage tasks and columns, handle team permissions, automate workflows with webhooks, and track portfolio-level analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and project teams use this skill to manage Monday.com workspaces, boards, items, teams, documents, webhooks, automations, dashboards, and portfolio analytics from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth-backed access to a connected Monday.com workspace through ClawLink. <br>
Mitigation: Install only when ClawLink is trusted for the workspace, review OAuth permissions, and use the least-privileged Monday account practical. <br>
Risk: The skill can perform powerful create, update, archive, delete, webhook, user, and admin actions. <br>
Mitigation: Confirm the target resource and intended effect before execution, and use preview or read operations first when they reduce ambiguity. <br>


## Reference(s): <br>
- [Monday.com API Documentation](https://developer.monday.com/api-reference/) <br>
- [Monday.com GraphQL API](https://api.monday.com/v2) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Monday.com tool-call names, JSON parameter examples, setup steps, and confirmation guidance for write actions.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
