## Description:

将 OpenClaw 连接到 Clawhome 聊天平台，实现 AI 自动回复。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shengguo](https://clawhub.ai/user/shengguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect OpenClaw to the Clawhome chat platform, configure channel credentials, and exchange text or file messages through the documented Clawhome protocol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation command does not pin a plugin version or source.

Mitigation: Review the resolved openclaw-clawhome package and install only a trusted version.

Risk: The channelSecret configuration value is a credential.

Mitigation: Store and handle channelSecret as a secret, and avoid exposing it in logs, shared terminals, or documentation.

Risk: The documented file upload flow sends local files to Clawhome.

Mitigation: Upload only files approved for Clawhome under the platform's access and retention rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shengguo/skills/openclaw-clawhome)
- [Clawhome file upload endpoint](https://www.clawhome.io/api/oss/upload)
- [Clawhome uploaded file URL example](https://www.clawhome.io/uploads/channels/123/image.png)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash commands, JSON examples, and configuration tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw plugin installation, channel configuration, gateway restart, protocol topics, message payload examples, and file upload guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
