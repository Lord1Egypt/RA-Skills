## Description: <br>
Supervise a main agent so it defaults to execution, suppresses obvious permission loops, and escalates to the user only for true approvals or critical ambiguity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sjingh](https://clawhub.ai/user/sjingh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to supervise agent replies, classify AUTO/CONFIRM/ESCALATE decisions, reduce permission loops, and preserve human approval for risky or ambiguous actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The supervisor policy may reduce user prompts for low-risk actions and could allow an agent to proceed when a human expected confirmation. <br>
Mitigation: Review the AUTO, CONFIRM, and ESCALATE rules before enabling the skill, and keep external sends, destructive actions, payment changes, secret handling, production changes, and legal or compliance-sensitive work in CONFIRM. <br>
Risk: Optional watchdog, cron, hook-pack, or task-state behavior can introduce persistent monitoring or stronger reply enforcement in a workspace. <br>
Mitigation: Enable persistent watchdogs or custom hook packs only after reviewing the workspace impact and keep Phase 1 policy and task files as the default rollout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sjingh/main-agent-supervisor) <br>
- [Supervisor Design](references/design.md) <br>
- [Comparison: Existing Skills vs Needed Supervisor](references/comparison.md) <br>
- [Workspace Implementation Plan](references/implementation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with policy classifications, task-state file patterns, and optional implementation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose task-state markdown files, audit artifacts, cron watchdog behavior, or hook-pack guidance when appropriate.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
