## Description: <br>
用户与模型间的任何交互行为都会触发此技能；提供Context Engineering五大核心能力（选择、压缩、检索、状态、记忆）及认知模型层支持；作为元技能强制常驻运行 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiwifruit13](https://clawhub.ai/user/kiwifruit13) <br>

### License/Terms of Use: <br>
GPL-3.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add persistent memory, context selection, compression, retrieval, state tracking, and cognitive-model support to an agent. It is intended as an always-on memory layer for cross-session agent interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is an always-on cross-session memory layer and can persist private user or project context. <br>
Mitigation: Install only when persistent memory is intended, use a dedicated storage directory, and confirm export and delete controls before use with private conversations or sensitive projects. <br>
Risk: The release evidence flags broad persistent access, sensitive profiling, credential storage, and unsafe local file primitives as requiring review. <br>
Mitigation: Review security-sensitive modules before deployment, avoid storing credentials unless explicitly needed, and disable emotional or personality profiling and host monitoring unless the user has clearly consented. <br>
Risk: The artifact declares GPL-3.0 but server release evidence lists MIT-0. <br>
Mitigation: Confirm the authoritative release license before publishing or redistributing the skill card. <br>


## Reference(s): <br>
- [Architecture Overview](references/architecture_overview.md) <br>
- [Architecture Execution Model](references/architecture_execution_model.md) <br>
- [Dual-Track Architecture Overview](references/dual_track_architecture_overview.md) <br>
- [Usage Guide](references/usage_guide.md) <br>
- [API Reference](references/api_reference.md) <br>
- [Module Index](references/module_index.md) <br>
- [Privacy Guide](references/privacy_guide.md) <br>
- [Encryption Guide](references/encryption_guide.md) <br>
- [Best Practices](references/best_practices.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing memory, retrieval, compression, privacy, and orchestration guidance; included scripts may create or update local memory data when used by an agent.] <br>

## Skill Version(s): <br>
1.0.11 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
