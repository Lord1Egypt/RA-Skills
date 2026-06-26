## Description: <br>
Manages long-term project context through file-based workflows for project discovery, entry, exit, recovery, and checkpointing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuboyang025-sketch](https://clawhub.ai/user/liuboyang025-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage long-running projects across sessions by creating recoverable project folders, recovery entries, indexes, decision logs, checkpoints, and a project registry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and reuses local project records, which can persist project paths, recovery notes, checkpoints, and registry data between sessions. <br>
Mitigation: Install only when persistent local project context is desired; review generated files, avoid storing secrets in notes, and confirm before scanning or updating registered project directories. <br>
Risk: Project recovery may use stale or incorrect paths if registered project directories move or become invalid. <br>
Mitigation: Use explicit project names and paths, validate registered directories before recovery, and update the registry when project locations or recovery files change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuboyang025-sketch/openclaw-project-context-manager) <br>
- [README](README.md) <br>
- [User guide and release notes](docs/发布说明与用户使用指南.md) <br>
- [Project registry maintenance guide](docs/项目注册表维护说明.md) <br>
- [Initialization and testing guide](docs/初始化与测试说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional JSON arguments and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local project folders, recovery notes, checkpoints, registry entries, and workspace rule files when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
