## Description:

OpenClaw 私人教练 - 每日文档同步+技巧教学。用于 (1) 每天自动从官网同步最新文档到 Obsidian 知识库 (2) 每天早上 7:21 发送 OpenClaw 使用技巧 (3) 每天晚上 21:05 让用户选择想了解的技巧主题 (4) 检测 OpenClaw 版本更新并提醒

This skill is ready for commercial/non-commercial use.

## Publisher:

[rabbot42](https://clawhub.ai/user/rabbot42)

### License/Terms of Use:


## Use Case:

OpenClaw users use this skill to keep local OpenClaw documentation synced into an Obsidian knowledge base and receive scheduled Chinese-language coaching tips. It also helps surface OpenClaw version updates during the daily tip workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document sync can overwrite files under ~/Obsidian/Docs/OpenClaw.

Mitigation: Back up the OpenClaw Obsidian folder or review the sync script before enabling scheduled runs.

Risk: Scheduled tips send messages through an OpenClaw/Feishu target.

Mitigation: Set FEISHU_USER_ID only for the intended recipient and review outgoing tip content before automation is enabled.

Risk: The sync workflow downloads OpenClaw documentation and release data from GitHub.

Mitigation: Run it only in environments where outbound GitHub access is expected and acceptable.

## Reference(s):

- [OpenClaw documentation source](https://raw.githubusercontent.com/openclaw/openclaw/main/docs)
- [OpenClaw latest release API](https://api.github.com/repos/openclaw/openclaw/releases/latest)
- [Openclaw Coach on ClawHub](https://clawhub.ai/rabbot42/skills/openclaw-coach)
- [rabbot42 ClawHub profile](https://clawhub.ai/user/rabbot42)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown and shell command output for scheduled OpenClaw coaching messages and local documentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local OpenClaw, jq, network access for document sync, an Obsidian path under ~/Obsidian/Docs/OpenClaw, and FEISHU_USER_ID for message delivery.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
