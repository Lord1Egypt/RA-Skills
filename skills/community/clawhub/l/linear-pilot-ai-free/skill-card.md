## Description: <br>
Linear Pilot Ai Free guides an agent through a Linear task automation workflow that receives issues through webhooks, updates status, sends notifications, and optionally synchronizes results to Git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and small teams use this skill to connect Linear issues to an agent-driven workflow for task intake, status updates, notifications, and optional Git commits. It is suited to a single basic workflow from Todo to In Progress to Done. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can change Linear issue status and add comments automatically. <br>
Mitigation: Require manual approval before comments or status changes, and use least-privilege Linear credentials. <br>
Risk: Webhook payloads and notifications can expose sensitive issue content to external services. <br>
Mitigation: Verify webhook authentication and avoid forwarding sensitive issue details unless the destination is approved. <br>
Risk: Git synchronization can commit or push changes before they are reviewed. <br>
Mitigation: Keep autoPush disabled until tested and require manual approval before commits or pushes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/linear-pilot-ai-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell, JSON, and text examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to perform Linear API actions, send notifications, and run Git commands when the user has configured the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
