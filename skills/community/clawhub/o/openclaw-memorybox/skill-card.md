## Description: <br>
MemoryBox is a zero-dependency memory maintenance CLI for OpenClaw that keeps MEMORY.md lean with a 3-tier organization and works alongside Mem0, Supermemory, QMD, or standalone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ramsbaby](https://clawhub.ai/user/Ramsbaby) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw agent maintainers use MemoryBox to diagnose, reorganize, archive, and deduplicate persistent memory files so agent memory remains searchable and compact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the external CLI from a repository can execute code from a moving source. <br>
Mitigation: Inspect the linked repository before installation and pin a trusted commit or release. <br>
Risk: Memory maintenance commands can reorganize persistent MEMORY.md and memory directory contents. <br>
Mitigation: Back up MEMORY.md and the memory directory before running split, archive, dedupe, or init. <br>
Risk: Suggested AGENTS.md changes can influence future agent behavior. <br>
Mitigation: Review any AGENTS.md changes before adopting them. <br>


## Reference(s): <br>
- [MemoryBox GitHub repository](https://github.com/Ramsbaby/openclaw-memorybox) <br>
- [OpenClaw Self-Healing companion repository](https://github.com/Ramsbaby/openclaw-self-healing) <br>
- [MemoryBox ClawHub page](https://clawhub.ai/Ramsbaby/openclaw-memorybox) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance focuses on an external CLI that can inspect and reorganize OpenClaw memory files.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
