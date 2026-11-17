## Description:

快速安装和配置 OpenClaw，支持微信、飞书、钉钉 Channel 设置及心跳和自动化任务管理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install OpenClaw, initialize a workspace, configure WeChat, Feishu, and DingTalk channels, and set up heartbeat automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following the setup may install the `openclaw` npm package globally on the user's machine.

Mitigation: Confirm the package source before installing, and consider pinning or isolating the install.

Risk: Messaging-channel setup may involve App ID, Secret, webhook, or login-session credentials.

Mitigation: Protect channel credentials and avoid exposing them in shared logs, prompts, or configuration files.

Risk: Heartbeat automation can continue running after setup if users forget how it was started.

Mitigation: Confirm how to stop the heartbeat service before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/openclaw-setup-service)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub issues](https://github.com/openclaw/openclaw/issues)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese setup guidance with service tiers and support links.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-03-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
