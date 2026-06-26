## Description: <br>
Lightweight structured memory system for OpenClaw, inspired by memU with zero external dependencies, that provides atomic memory storage with categories (preferences/knowledge/relationships/tasks/skills), tag-based indexing, and fast retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoo-unison](https://clawhub.ai/user/yoo-unison) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent users use memU-lite to maintain persistent local memory for user preferences, project knowledge, relationships, tasks, and reusable skills across OpenClaw sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain conversation-derived user data longer than intended. <br>
Mitigation: Set explicit rules for what may be remembered, avoid storing secrets or sensitive personal data, and periodically review or delete saved memories. <br>
Risk: The installation script seeds example profile-like memory entries that could be mistaken for real user facts. <br>
Mitigation: Remove or replace the seeded examples before normal use. <br>
Risk: Backup and restore commands can preserve or overwrite local memory contents. <br>
Mitigation: Review backup contents and confirm restore targets before using backup recovery or cleanup commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yoo-unison/memu-lite) <br>
- [memU-lite project page](https://github.com/yoo-unison/memu-lite) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [memU inspiration project](https://github.com/NevaMind-AI/memU) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown files, shell command output, and concise setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and manages local memory files under the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
