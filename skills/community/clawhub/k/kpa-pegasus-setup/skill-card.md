## Description:

为 KONKR Pocket ADVANCE 掌机提供 Pegasus、RetroArch、PPSSPP 和 EKA2L1/N-Gage 的安装、配置、排障与验证指南，并附带相应脚本和配置示例。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

KPA 掌机用户可用此技能安装和维护天马游戏库及相关模拟器，排查方向、核心、封面、简介和存档问题，并在执行设备变更前查看检查步骤与影响。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloads of executable files are not verified by the supplied scan.

Mitigation: Review each download source and command before running it; obtain installers only from sources you trust.

Risk: Broad cleanup may permanently remove device files.

Mitigation: Use the read-only health check to review a scoped deletion list, preserve a recovery copy, and confirm each batch before deleting.

Risk: Some procedures access the host or connected device beyond basic setup needs.

Mitigation: Review the requested access and target paths first, and use dry-run or read-only modes where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lisong2003-lgtm/skills/kpa-pegasus-setup)
- [Publisher profile](https://clawhub.ai/user/lisong2003-lgtm)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Chinese Markdown guidance with shell commands, configuration examples, and verification checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some procedures require a connected KPA device and hands-on verification.]

## Skill Version(s):

2.4.2 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
