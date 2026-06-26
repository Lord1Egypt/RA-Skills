## Description: <br>
Multi Agent Protocol is an OpenClaw-native v2 protocol for spec-first multi-agent delivery with explicit phase control, dual review gates, stored retry and circuit-breaker state, Lobster approval and recovery, task-store state, and ACP handoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hakityc](https://clawhub.ai/user/hakityc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate two or more agents through a stored, review-gated workflow. It is suited for OpenClaw-native multi-agent delivery where task state, retries, approvals, and external coding harness handoffs need explicit ownership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect phase authority could let executors or reviewers finalize work without orchestration review. <br>
Mitigation: Enforce the documented permission matrix so only the orchestrator can transition phases or open the circuit. <br>
Risk: Deployments, merges, external writes, or destructive edits could run without an explicit human decision. <br>
Mitigation: Keep Lobster approval gates enabled for side-effecting steps and resume only from persisted task-store approval state. <br>
Risk: Task specs, artifacts, or event logs may capture secrets or unnecessary private data. <br>
Mitigation: Avoid placing secrets or unrelated private data in task-store records and review task artifacts before sharing or retaining them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hakityc/multi-agent-protocol) <br>
- [Agent Permission Matrix](references/agent-permissions.md) <br>
- [task-store Plugin Design](references/task-store-plugin.md) <br>
- [Migration From v1 To OpenClaw-native v2](references/migration.md) <br>
- [Lobster Approval Recovery Template](lobster/approval-recovery.template.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured protocol steps, reference schemas, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow guidance and implementation scaffolding for coordinating agent roles, task-store state, approval gates, retries, and ACP handoffs.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
