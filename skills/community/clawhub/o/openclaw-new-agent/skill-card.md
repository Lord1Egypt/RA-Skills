## Description:

在 OpenClaw 上创建新的独立飞书机器人（多账号模式）。当用户要求创建新的飞书机器人、新增 Agent、部署第二个机器人时使用。流程包括：收集配置信息、备份、创建工作区、修改配置和验证。

This skill is ready for commercial/non-commercial use.

## Publisher:

[itzhouq](https://clawhub.ai/user/itzhouq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add another independent Feishu bot agent to an existing OpenClaw setup. It guides collection of bot credentials, configuration backup, workspace creation, OpenClaw configuration patching, and post-change validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify ~/.openclaw and OpenClaw gateway configuration.

Mitigation: Review proposed configuration patches, keep a backup of openclaw.json, and validate with openclaw doctor before relying on the new bot.

Risk: Feishu App Secrets may be exposed if pasted into ordinary chat or retained in logs/transcripts.

Mitigation: Enter secrets locally or through a secret manager when possible, restrict permissions on openclaw.json and backups, and rotate any secret that was already exposed.

Risk: Mutable installer commands such as clawhub@latest can change what is installed over time.

Mitigation: Prefer a pinned, reviewed installer version for repeatable installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itzhouq/skills/openclaw-new-agent)
- [Publisher profile](https://clawhub.ai/user/itzhouq)
- [ClawHub homepage from clawdis metadata](https://clawhub.com)
- [Feishu OpenClaw multi-agent app template](https://open.feishu.cn/page/openclaw?form=multiAgent)
- [Introduction video](https://www.bilibili.com/video/BV16fXLBkEwo)
- [Demo video](https://www.bilibili.com/video/BV1cUXaBsEM1)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the user for Feishu App ID, App Secret, bot name, workspace name, and testing details before proposing local OpenClaw configuration changes.]

## Skill Version(s):

1.2.1 (source: server release metadata, SKILL.md frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
