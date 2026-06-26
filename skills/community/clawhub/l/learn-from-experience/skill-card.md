## Description: <br>
Learn from experience: self-reflection + self-criticism + self-learning + self-organizing memory + cross-session sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shibing624](https://clawhub.ai/user/shibing624) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preserve explicit corrections, confirmed preferences, and self-reflection lessons across sessions. It helps agents organize local memory, cite learned rules, and sync confirmed patterns into supported agent startup configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist learned user preferences in local memory. <br>
Mitigation: Install only when persistent agent memory is desired, review what will be stored, and audit ~/learn-from-experience regularly. <br>
Risk: The skill can automatically write confirmed preferences into multiple agents' global startup configuration files. <br>
Mitigation: Restrict sync to intended agent configs, back up global config files before enabling sync, and review generated Patterns entries. <br>
Risk: The setup flow may propose installing an optional Proactivity companion skill. <br>
Mitigation: Review the optional companion skill separately and install it only after explicit approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shibing624/learn-from-experience) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Setup guide](artifact/setup.md) <br>
- [Security boundaries](artifact/boundaries.md) <br>
- [Memory operations](artifact/operations.md) <br>
- [Learning mechanics](artifact/learning.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with setup snippets and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory files and startup configuration updates when the agent follows the documented setup and sync flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
