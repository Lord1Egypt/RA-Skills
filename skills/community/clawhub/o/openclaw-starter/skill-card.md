## Description:

OpenClaw 安装后引导助手。当新手不知道安装什么 Skills、如何配置渠道、如何使用时，提供智能推荐和分步指导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[testmtcode](https://clawhub.ai/user/testmtcode)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers new to OpenClaw use this skill to choose starter skills, configure messaging channels, create starter documentation, and check local setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide recommends bulk installing skills, including high-impact capabilities such as SSH, code execution, cron jobs, webhooks, and email sending.

Mitigation: Install recommended skills one at a time after checking publisher, permissions, and actual need.

Risk: Messaging channel setup uses bot tokens and similar credentials.

Mitigation: Keep tokens out of chats, screenshots, and repositories; prefer environment variables or the documented configuration flow.

Risk: The release includes an unpinned requests dependency.

Mitigation: Remove it if unused, or pin and review the dependency before running the scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/testmtcode/skills/openclaw-starter)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw)
- [OpenClaw Telegram channel documentation](https://docs.openclaw.ai/channels/telegram)
- [OpenClaw WhatsApp channel documentation](https://docs.openclaw.ai/channels/whatsapp)
- [OpenClaw Discord channel documentation](https://docs.openclaw.ai/channels/discord)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Discord developer documentation](https://discord.com/developers/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style guidance with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest local CLI commands and starter templates for OpenClaw setup.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
