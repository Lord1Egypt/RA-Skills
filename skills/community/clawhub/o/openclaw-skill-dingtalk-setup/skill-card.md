## Description:

钉钉企业内部机器人渠道快速对接。Use when: 用户需要对接钉钉渠道、配置钉钉 Stream 模式、排查钉钉消息问题。NOT for: 飞书/Lark、企业微信等其他平台。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaoyunhao0107](https://clawhub.ai/user/shaoyunhao0107)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect OpenClaw to a DingTalk internal bot channel, configure Stream mode, install the DingTalk plugin, and troubleshoot channel connectivity or message response issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports realistic-looking DingTalk credentials in examples.

Mitigation: Replace all example credentials with user-owned values, rotate them if they were ever real, and avoid storing or sharing secrets in command history or published configuration.

Risk: The security summary reports unsafe credential and dependency-installation examples.

Mitigation: Review installation sources before use, prefer pinned plugin versions or reviewed packages, and restrict access to OpenClaw configuration files that contain channel credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shaoyunhao0107/skills/openclaw-skill-dingtalk-setup)
- [DingTalk Plugin Repository](https://github.com/soimy/openclaw-channel-dingtalk)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [DingTalk Open Platform](https://open.dingtalk.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps, configuration options, verification commands, and troubleshooting guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
