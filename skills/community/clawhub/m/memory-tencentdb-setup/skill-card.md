## Description:

提供 memory-tencentdb 插件的安装步骤、依赖配置、路径说明及常见问题解决，支持 OpenClaw 四层记忆系统集成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this guide to install and configure the memory-tencentdb plugin, including Gateway dependency placement, openclaw.json configuration, restart steps, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin is intended to store conversation history and build local user profiles.

Mitigation: Enable it only when users accept that retention behavior, and document how to delete or disable the memory store.

Risk: The guide installs or copies npm dependencies into the Gateway runtime, which can broaden dependency risk if packages are unconstrained.

Mitigation: Pin and verify npm dependencies before installation, use --ignore-scripts as shown, and review the resulting Gateway node_modules contents.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/paudyyin/skills/memory-tencentdb-setup)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw issue tracker](https://github.com/openclaw/openclaw/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown installation guide with command and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operating-system-specific paths, dependency installation options, validation commands, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: evidence release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
