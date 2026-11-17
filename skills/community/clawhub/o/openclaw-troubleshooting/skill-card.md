## Description:

OpenClaw故障排除工具提供系统诊断、依赖检查、权限修复和工作区结构修复，帮助用户定位并处理常见 OpenClaw 问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[playgod2023](https://clawhub.ai/user/playgod2023)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and skill developers use this agent skill to diagnose local environment, dependency, permission, and workspace structure issues. It can provide troubleshooting output and run repair actions for common OpenClaw setup problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair paths can automatically install software and change permissions across the OpenClaw workspace.

Mitigation: Run diagnostic commands first, review the exact repair effects before using quick_start.py or fix all, and back up the OpenClaw workspace.

Risk: Dependency repairs can alter the active Python environment through pip installs.

Mitigation: Prefer running dependency repairs inside an isolated virtual environment instead of allowing system-level or user-level pip changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/playgod2023/skills/openclaw-troubleshooting)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and console-style text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; repair paths can modify dependencies, permissions, and workspace directories.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
