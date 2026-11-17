## Description:

智能盯盘插件，用于监控A股、港股、比特币等金融市场行情并在条件触发时发送提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyv](https://clawhub.ai/user/lingyv)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to configure market watch conditions for A-shares, Hong Kong stocks, indices, and cryptocurrencies, then receive reminders when the configured conditions trigger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends an authentication token and possible contact details through a plaintext WebSocket endpoint.

Mitigation: Use the skill only when you trust the publisher and bridge service, avoid untrusted networks until the endpoint uses wss://, and omit email or phone notifications unless off-platform contact is intended.

Risk: The documented setup uses a global, unpinned npm install.

Mitigation: Prefer a pinned and reviewed package version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lingyv/skills/glance-watch)
- [Market reference](references/markets.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a product code, market type, condition expression, variables, and OpenClaw notification channel details when creating a watch.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
