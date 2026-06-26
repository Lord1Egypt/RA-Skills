## Description: <br>
Multi-Agent Orchestrator v8.2.1 supports goal-driven research, task decomposition, parallel execution, validation review, and model-adaptive decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bjmrcft-hash](https://clawhub.ai/user/bjmrcft-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to plan and run multi-agent research or project workflows in OpenClaw, including task decomposition, parallel worker execution, validation review, aggregation, and cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad control over an OpenClaw workspace and spawned agents. <br>
Mitigation: Install and run it only in workspaces where that level of control is acceptable, and review generated plans before execution. <br>
Risk: Local configuration can affect execution behavior. <br>
Mitigation: Keep openclaw.json writable only by trusted users and review configuration changes before running workflows. <br>
Risk: Cleanup behavior can remove workspace files. <br>
Mitigation: Run cleanup in dry-run mode first and verify the affected paths before allowing deletion. <br>
Risk: Reports, logs, and traces may persist sensitive task content. <br>
Mitigation: Avoid including secrets or sensitive business data in tasks unless the workspace storage and retention practices are appropriate. <br>


## Reference(s): <br>
- [Module Reference](references/modules.md) <br>
- [Runtime Operation Protocols](references/protocols.md) <br>
- [End-to-End Test Lessons](references/test-lessons.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce workflow plans, execution dashboards, worker reports, validation summaries, final reports, archives, logs, and cleanup summaries.] <br>

## Skill Version(s): <br>
8.2.1 (source: evidence.release.version, artifact/skill.json, SKILL.md changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
