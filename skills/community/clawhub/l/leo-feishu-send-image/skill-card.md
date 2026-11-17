## Description:

Send local images to Feishu (Lark) users or group chats through the Feishu messaging API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-jiqimao](https://clawhub.ai/user/leo-jiqimao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to send generated or local image files to Feishu users and group chats from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could upload an unintended local image file if it is given broad readable filesystem access.

Mitigation: Restrict allowed image paths to a workspace or approved directory and require explicit confirmation before upload.

Risk: Images could be sent through the wrong Feishu account or to the wrong user or group chat.

Mitigation: Validate account IDs and recipient IDs, display the destination before sending, and require confirmation for sensitive workflows.

Risk: Unsupported, oversized, or mislabeled files may be uploaded because the artifact only checks that the path exists.

Mitigation: Add MIME type, extension, and size checks before calling the Feishu upload API.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu Open Platform Documentation](https://open.feishu.cn/document/home/index)
- [Feishu Send Message API](https://open.feishu.cn/document/server-docs/im-v1/message/create)
- [Feishu Upload Image API](https://open.feishu.cn/document/server-docs/im-v1/image/create)
- [ClawHub Skill Page](https://clawhub.ai/leo-jiqimao/skills/leo-feishu-send-image)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends selected local image files through configured Feishu credentials and returns command-line status messages.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
