## Description:

用统一规则管理长期项目的发现、进入、退出、恢复与阶段性固化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuboyang025-sketch](https://clawhub.ai/user/liuboyang025-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project maintainers use this skill to manage long-running, multi-session project work with file-backed discovery, entry, recovery, exit, checkpoint, and state-solidification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The initializer can write outside intended project folders when given crafted paths or project names.

Mitigation: Use trusted project and workspace roots, reject path separators and '..' in project names, avoid overwrite until target files are reviewed, and enforce path containment before installation.

Risk: The skill uses a file-backed workflow that reads registered project paths and creates project records.

Mitigation: Install it only in workspaces where this file access is acceptable, and review registry entries and generated records before relying on them for recovery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuboyang025-sketch/skills/openclaw-project-context-manager)
- [README](README.md)
- [Initialization and Testing Guide](docs/初始化与测试说明.md)
- [Project Registry Maintenance Guide](docs/项目注册表维护说明.md)
- [Release Notes and User Guide](docs/发布说明与用户使用指南.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON and shell command examples; initializer produces project directories and Markdown template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 for the initializer script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
