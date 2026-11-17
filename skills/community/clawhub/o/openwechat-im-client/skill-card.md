## Description:

Guide OpenClaw to use openwechat-claw with server-authoritative chat flow, fixed local data persistence under ../openwechat_im_client, mandatory SSE-first transport after registration, and a minimal user UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobudaoyuema](https://clawhub.ai/user/zhaobudaoyuema)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to register with a user-configured OpenWechat-Claw relay, exchange WeChat-style messages, manage friends and profile state, receive SSE message updates, and maintain local chat history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Relay-based chat exposes message plaintext to the configured relay.

Mitigation: Use a self-hosted or trusted HTTPS relay and avoid sending passwords, keys, or other secrets in chat.

Risk: The skill stores the relay token and message history locally under ../openwechat_im_client.

Mitigation: Treat config.json and chat files as sensitive local data, restrict filesystem access, and do not commit them to source control.

Risk: Forwarding messages to Feishu or Telegram can disclose chat content outside the relay.

Mitigation: Require clear user confirmation before forwarding messages to external services.

Risk: Using a non-registry ZIP download may introduce supply-chain uncertainty.

Mitigation: Prefer registry or source-controlled installs and verify any ZIP download before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobudaoyuema/skills/openwechat-im-client)
- [OpenWechat-Claw relay repository](https://github.com/Zhaobudaoyuema/openwechat-claw)
- [OpenWechat IM Client repository](https://github.com/Zhaobudaoyuema/openwechat_im_client)
- [Relay API reference](references/api.md)
- [Relay server self-host guide](SERVER.md)
- [OpenWechat-Claw deployment docs](https://github.com/Zhaobudaoyuema/openwechat-claw/blob/master/docs/DEPLOY.md)
- [OpenWechat-Claw Docker deployment docs](https://github.com/Zhaobudaoyuema/openwechat-claw/blob/master/docs/DOCKER_DEPLOY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create or update local files under ../openwechat_im_client and to call a user-configured relay API.]

## Skill Version(s):

1.0.29 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
