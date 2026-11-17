## Description:

AI Agent 自进化记忆系统。核心功能 100% 本地运行 (纯 Markdown+JSON)。网络备份/节点通信为可选 opt-in，需手动配置凭证。

This skill is ready for commercial/non-commercial use.

## Publisher:

[king6381](https://clawhub.ai/user/king6381)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent users use this skill to give an OpenClaw agent local persistent memory, write-through session logging, strategy lookup, and optional maintenance workflows for personal or workspace-level agent continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently alter workspace memory and behavior files such as AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, and strategy registries.

Mitigation: Install in an isolated workspace first and manually review proposed changes to behavior and memory files before relying on them.

Risk: Optional automation can affect git history, cron entries, backups, and workspace files.

Mitigation: Review scripts before enabling them, keep cron jobs opt-in, and replace whole-workspace auto commits with a narrow allowlist where possible.

Risk: Optional remote backup workflows may expose sensitive local memory content or credentials if configured carelessly.

Mitigation: Avoid storing secrets in the workspace, use HTTPS or encrypted backups only, validate SSH backup paths, and back up only to trusted targets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/king6381/skills/mjolnir-brain)
- [README](README.md)
- [Installation Guide](INSTALL.md)
- [Architecture](docs/architecture.md)
- [Security Notes](docs/security.md)
- [Self-Learning Mechanism](docs/self-learning.md)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workspace memory files and optional script-driven maintenance instructions; optional backup and cron workflows require manual opt-in.]

## Skill Version(s):

3.0.2 (source: evidence.release.version, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
