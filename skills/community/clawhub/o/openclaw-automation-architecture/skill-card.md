## Description: <br>
Design OpenClaw-native automation systems using cron, HEARTBEAT.md, spawned sessions, specialist-agent delegation, first-class tools, MCPs, and local scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lsj210001](https://clawhub.ai/user/lsj210001) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to design OpenClaw-native automation workflows, choose the right execution plane, and define state, deduplication, delivery, and recovery behavior for recurring or event-driven work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automation designs can schedule work, connect data sources, or trigger external actions that have operational impact if enabled without review. <br>
Mitigation: Review schedules, cancellation paths, data sources, persistent state files, external connectors, and approval checkpoints before enabling an automation. <br>
Risk: Workflows that publish, pay, modify configuration, or perform destructive changes can create unintended outcomes if approval is skipped. <br>
Mitigation: Require explicit user approval before public posts, payments, destructive changes, or configuration changes. <br>


## Reference(s): <br>
- [OpenClaw Automation Architecture](https://clawhub.ai/lsj210001/openclaw-automation-architecture) <br>
- [Decision Matrix](references/decision-matrix.md) <br>
- [OpenClaw Workflow Patterns](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations cover execution plane, rationale, state and deduplication, failure handling, and whether native OpenClaw or an external workflow tool is justified.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
