## Description:

Connects a DingTalk Stream-mode bot to OpenClaw so user messages can be sent to the OpenClaw HTTP API and returned to DingTalk through a webhook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tongshendota](https://clawhub.ai/user/tongshendota)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a DingTalk AI assistant that forwards chat messages to OpenClaw and posts the generated response back into DingTalk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enterprise chat content and credentials are handled by the generated DingTalk bot workflow.

Mitigation: Use a dedicated low-privilege DingTalk app, store credentials outside source code, and approve data handling before forwarding sensitive messages.

Risk: Plaintext configuration and webhook/token examples can lead to accidental secret exposure.

Mitigation: Move DingTalk credentials, webhook URLs, and OpenClaw tokens into a secret manager or protected environment variables before deployment.

Risk: Message-body logging may record sensitive user content.

Mitigation: Disable message-body logging or redact chat content in logs before using the bot in an organization.

Risk: Unrestricted bot access can allow unintended users or chats to invoke OpenClaw.

Mitigation: Restrict allowed DingTalk chats and users, and pin dependencies before running the integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tongshendota/skills/litmedia-dingtalk-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential, webhook, logging, and local OpenClaw gateway configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
