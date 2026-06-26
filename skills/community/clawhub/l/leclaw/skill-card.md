## Description: <br>
LeClaw is a hierarchical agent collaboration framework for OpenClaw that provides task management and collaboration capabilities. Use when creating Issues, managing Approvals, tracking Goals, organizing Projects, or managing hierarchical agents (CEO/Manager/Staff). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saullockyip](https://clawhub.ai/user/saullockyip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use LeClaw to coordinate OpenClaw agents through role-based issue tracking, approvals, goals, projects, onboarding, and heartbeat-driven task polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires personal LeClaw API keys and its documentation instructs agents to store those keys in markdown. <br>
Mitigation: Store API keys in a protected secret mechanism and avoid committing or sharing markdown files that contain credentials. <br>
Risk: Activity logs may contain private reasoning, decisions, and operational context that other agents can read. <br>
Mitigation: Keep secrets and sensitive private reasoning out of activity.log, and limit log access to agents that need it for task recovery or handoff. <br>
Risk: Heartbeat templates can encourage autonomous polling, task creation, and human notifications while agents are idle. <br>
Mitigation: Enable heartbeat files only with explicit scope, quiet-hour rules, review limits, and a clear stop procedure. <br>
Risk: The skill can coordinate agent invites, issue assignment, approvals, and role-based actions. <br>
Mitigation: Require explicit approval for creating agents, approving actions, or changing company-level goals and projects. <br>


## Reference(s): <br>
- [LeChat](https://clawhub.ai/saullockyip/lechat) <br>
- [Leclaw ClawHub Page](https://clawhub.ai/saullockyip/leclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with CLI command examples, checklists, and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions for LeClaw CLI workflows, onboarding, activity logs, and heartbeat templates.] <br>

## Skill Version(s): <br>
1.1.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
