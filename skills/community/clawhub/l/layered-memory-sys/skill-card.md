## Description: <br>
Layered Memory Sys provides a six-layer memory management system for AI agents, with TTL-based memory tiers, dream-cycle consolidation, TF-IDF search, import/export, backups, a management panel, and Docker deployment support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[141553](https://clawhub.ai/user/141553) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to add persistent, searchable, tiered long-term memory to OpenClaw-style agent workflows. It is intended for agents that need memory retention, automatic forgetting, knowledge extraction, session-log recall, and memory import/export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read recent OpenClaw session logs and persist long-term memory data. <br>
Mitigation: Review SESSION_DIR and MEMORY_DIR before enabling the skill, and use it only with conversation logs and memory locations intended for retention. <br>
Risk: The skill can persist, import, export, delete, and back up memory data. <br>
Mitigation: Make backups before bulk import, deletion, dream-cycle, or archive operations, and review configured backup retention. <br>
Risk: The local REST API and WebSocket services may be exposed without authentication. <br>
Mitigation: Bind API and WebSocket services to localhost or add authentication before exposing them beyond the local machine. <br>
Risk: Auto-write behavior and optional remote providers can process sensitive conversation content or credentials. <br>
Mitigation: Disable auto-write and remote providers unless needed, and review DOUBAO_API_KEY and DASHSCOPE_API_KEY handling before use. <br>
Risk: The installer can create a persistent service when run with elevated privileges. <br>
Mitigation: Avoid running the installer as root unless a persistent system service is intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/141553/layered-memory-sys) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, REST API responses, and memory export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist memory data, read recent session logs, expose local REST and WebSocket services, and create backups when enabled.] <br>

## Skill Version(s): <br>
2.4.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
