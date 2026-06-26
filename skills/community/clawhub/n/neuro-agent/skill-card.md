## Description: <br>
类脑分区的情感智能Agent系统 Neuro-α，模拟大脑分区协作来 support emotional companionship, task reasoning, persistent memory, proactive care, and daily reflection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alfredli-stack](https://clawhub.ai/user/alfredli-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add a relationship-style AI companion workflow with emotion detection, intent reasoning, memory capsules, proactive check-ins, and self-reflection routines. It is intended for agents that can run Python scripts and manage local user memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent private memory may store sensitive conversations and relationship context. <br>
Mitigation: Review memory paths and retention behavior before deployment; provide users a clear way to inspect, delete, or disable stored memory. <br>
Risk: Background jobs and proactive messaging can contact users without an immediate prompt. <br>
Mitigation: Disable or review cron, heartbeat, and messaging settings before enabling the skill in a live agent. <br>
Risk: The artifact includes bundled personal profile material and persona assumptions. <br>
Mitigation: Remove bundled USER.md personal data and hard-coded persona references before use. <br>
Risk: The skill can reuse existing API credentials and send Feishu messages. <br>
Mitigation: Verify credential access, Feishu configuration, and outbound messaging permissions in the target environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alfredli-stack/neuro-agent) <br>
- [README](artifact/README.md) <br>
- [User Guide](artifact/USER_GUIDE.md) <br>
- [Assembly Guide](artifact/ASSEMBLY_GUIDE.md) <br>
- [Architecture v2](artifact/docs/ARCHITECTURE_v2.md) <br>
- [Relationship Stages](artifact/relationship_stages.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with optional Python commands, configuration edits, and generated memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local persistent memory, reflection, heartbeat, and relationship-state files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
