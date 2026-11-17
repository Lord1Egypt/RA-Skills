## Description:

提供 OpenClaw Terminal (OCT) 的配置模板和使用指南，支持智能对话、系统控制和开发辅助功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zl585451](https://clawhub.ai/user/zl585451)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to configure and use the OCT desktop app for conversational task assistance, system control, and development workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill points users to a powerful third-party desktop app without strong verification guidance.

Mitigation: Install OCT only when the publisher and release channel are trusted, and verify downloaded installers independently where possible.

Risk: OCT workflows may modify files, run terminal commands, change system settings, or operate on Git repositories.

Mitigation: Review proposed actions before execution, avoid unnecessary administrative privileges, and use backups or version control for recoverability.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zl585451/skills/oct-helper)
- [OCT GitHub release v0.1.2](https://github.com/zl585451/openclaw-terminal/releases/tag/v0.1.2)
- [OCT GitHub Issues](https://github.com/zl585451/openclaw-terminal/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance for installing and using OCT; includes third-party download and support links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
