## Description:

Guides agents through Feishu IM messaging operations, including sending text, images, and files to users or groups through the Bot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inuyashayang](https://clawhub.ai/user/inuyashayang)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to help an agent send Feishu messages and media correctly through a configured Bot App. It is especially useful for avoiding common image-upload mistakes such as sending a raw file path instead of uploading media first.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases could start a Feishu send workflow unintentionally.

Mitigation: Review message targets, attachments, and content before allowing outbound sends in shared or business chats.

## Reference(s):

- [Feishu image-sending pitfalls](references/image-sending-pitfalls.md)
- [Feishu Upload Image API](https://open.feishu.cn/document/server-docs/im-v1/image/create)
- [Feishu API FAQ](https://feishu.apifox.cn/doc-1944903)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration]

**Output Format:** [Markdown guidance with tool-call examples and troubleshooting notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead an agent to send outbound Feishu messages or upload media through an authorized bot.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
