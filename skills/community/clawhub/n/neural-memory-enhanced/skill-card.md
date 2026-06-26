## Description: <br>
Associative memory with spreading activation for persistent, intelligent recall across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuyu28](https://clawhub.ai/user/zhuyu28) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to persist, recall, and manage local memories such as decisions, errors, preferences, TODOs, and context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can save and automatically reuse conversation context without sufficient consent, scoping, or retention controls. <br>
Mitigation: Install only when persistent agent memory is intended, keep separate brains for different projects or users, and require confirmation before saving or auto-processing conversation content. <br>
Risk: Stored memories may include secrets or regulated personal data. <br>
Mitigation: Avoid storing secrets or regulated personal data, and review memory contents before sharing, transplanting, or reusing a brain. <br>
Risk: The skill installs and runs a package-managed local memory tool. <br>
Mitigation: Verify the intended package source before installation and confirm the configured brain name before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuyu28/neural-memory-enhanced) <br>
- [Declared NeuralMemory project homepage](https://github.com/nhadaututtheky/neural-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to store and retrieve local SQLite-backed memories through NeuralMemory tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
