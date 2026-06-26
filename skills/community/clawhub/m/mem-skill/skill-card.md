## Description: <br>
Mem Skill gives AI agents a persistent local knowledge and experience store that retrieves prior context and records approved reusable learnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oliguo](https://clawhub.ai/user/oliguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain project-scoped or optional QMD-backed memory across conversations, retrieve previous solutions, and save approved knowledge, preferences, and skill experience for future tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores conversation-derived knowledge and experience in the workspace. <br>
Mitigation: Ask for approval before recording, keep secrets and sensitive personal or business data out of saved entries, and periodically inspect or delete the knowledge-base, experience, and log files. <br>
Risk: Optional QMD setup adds a local dependency and indexing workflow. <br>
Mitigation: Verify the QMD package and any MCP daemon before enabling it, prefer project-scoped collections, and review collection names, scope, and file masks during initialization. <br>


## Reference(s): <br>
- [Mem Skill on ClawHub](https://clawhub.ai/oliguo/mem-skill) <br>
- [Memory Engine Architecture](references/engines.md) <br>
- [QMD Memory Engine Reference](references/qmd-engine.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration files and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local knowledge-base, experience, log, and memory configuration files after user approval.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
