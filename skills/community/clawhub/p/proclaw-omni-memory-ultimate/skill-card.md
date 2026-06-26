## Description: <br>
Integrates an 8-layer memory system with self-driven, self-evolving, self-learning, and core-axis components for agent cognitive architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thinkbugs](https://clawhub.ai/user/thinkbugs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building agents use this skill to add durable local memory, semantic recall, consolidation, backup, multimodal memory, and autonomous agent loops. It is intended for agent workspaces where persistent user, project, feedback, and reference memory are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly stores and reuses user or project information with weak consent, retention, and safety controls. <br>
Mitigation: Install only in workspaces where durable local memory is acceptable, inspect generated memory files regularly, and avoid storing secrets, credentials, regulated personal data, or confidential project details. <br>
Risk: Automatic consolidation, restore, federation, or multimodal search can expose or propagate sensitive workspace data. <br>
Mitigation: Review these behaviors before enabling them on sensitive data, and evaluate the skill in a sandbox or disposable workspace first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thinkbugs/proclaw-omni-memory-ultimate) <br>
- [ProClaw website](https://www.proclaw.top) <br>
- [Memory Architecture](references/memory-architecture.md) <br>
- [Memory Types](references/memory-types.md) <br>
- [WAL Protocol](references/wal-protocol.md) <br>
- [Advanced Features](references/advanced-features.md) <br>
- [Cellular Architecture](references/cellular-architecture.md) <br>
- [Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory directories and files when followed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
