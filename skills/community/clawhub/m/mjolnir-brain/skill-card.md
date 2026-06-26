## Description: <br>
AI Agent 自进化记忆系统。核心功能 100% 本地运行 (纯 Markdown+JSON)。网络备份/节点通信为可选 opt-in，需手动配置凭证。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[king6381](https://clawhub.ai/user/king6381) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add persistent local memory, session recovery, strategy lookup, and self-learning workflows to an OpenClaw-style agent workspace. It is intended for local Markdown/JSON memory management, with backup, cron, and node-communication workflows treated as optional features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional automation can commit, delete, archive, or back up workspace data. <br>
Mitigation: Keep cron, auto-commit, remote backup, and node-communication features disabled until the scripts are audited and scoped to the intended memory directory. <br>
Risk: Local memory files and daily logs may contain sensitive information that could later be committed or backed up. <br>
Mitigation: Avoid storing secrets in MEMORY.md, USER.md, daily logs, or any file included in commit or backup workflows. <br>
Risk: Remote backup features require WebDAV or SSH credentials and can send workspace data to external storage. <br>
Mitigation: Enable backup only with trusted storage targets, secure credentials, and a dry-run review of the backup behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/king6381/mjolnir-brain) <br>
- [Security notes](docs/security.md) <br>
- [Architecture](docs/architecture.md) <br>
- [Self-learning mechanism](docs/self-learning.md) <br>
- [Multi-user architecture](docs/multi-user.md) <br>
- [Node protocol specification](docs/node-protocol-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory templates, strategy registry entries, setup guidance, and optional automation commands for an agent workspace.] <br>

## Skill Version(s): <br>
3.0.2 (source: evidence.json release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
