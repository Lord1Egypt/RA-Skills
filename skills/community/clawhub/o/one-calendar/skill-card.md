## Description:

每日单向历图片发送工具。自动获取当天日期，构造图片 URL，并通过飞书发送单向历图片。支持配置向导和定时任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chempeng](https://clawhub.ai/user/chempeng)

### License/Terms of Use:

MIT License

## Use Case:

OpenClaw users use this skill to configure a Feishu recipient and send the daily One Calendar image manually, through chat triggers, or on a scheduled cron job.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted configuration value could cause the send script to run unintended local shell commands.

Mitigation: Protect and review config.json, validate userId and baseUrl strictly, and replace shell-string execution before relying on scheduled sends.

Risk: The skill contacts Feishu and the configured image host when sending the daily image.

Mitigation: Verify the Feishu recipient ID, confirm the image source base URL, and use the skill only in environments where those outbound contacts are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chempeng/skills/one-calendar)
- [Publisher profile](https://clawhub.ai/user/chempeng)
- [Repository link from artifact metadata](https://github.com/chempeng/one-calendar)
- [One Calendar official site](https://www.owspace.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for configuring a local config.json file and sending image messages through OpenClaw and Feishu.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
