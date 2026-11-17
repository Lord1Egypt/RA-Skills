## Description:

杰峰智能宠物喂食器设备控制技能（开发版）。支持远程一键喂食、设置或查询定时喂食计划，以及配置设备端的宠物检测功能开关。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to control bound JFTech smart pet feeders: check feeder capability, trigger remote feeding, manage scheduled feeding, and query or change pet-detection settings.

### Deployment Geography for Use:

China Mainland, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: Signed JFTech credentials and device tokens may be sent to an arbitrary endpoint if JF_ENDPOINT is changed.

Mitigation: Set JF_ENDPOINT only to an official vendor host and rotate credentials if they may have been used with an untrusted endpoint.

Risk: The skill can issue physical feeding commands and change feeder schedules or pet-detection settings.

Mitigation: Require explicit user confirmation before feeding, schedule-changing, or pet-detection setting actions.

Risk: Use of real device credentials in an untrusted runtime could expose account or device access.

Mitigation: Run only in a trusted environment with trusted JFTech credentials and review before installation.

## Reference(s):

- [JFTech Open Platform documentation](https://docs.jftech.com)
- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-feed-control)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JFTech account, app, device, and token environment variables before executing device-control commands.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
