## Description: <br>
Helps agents send Feishu text, image, and file messages to users or groups through the Feishu Bot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[InuyashaYang](https://clawhub.ai/user/InuyashaYang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to have an agent send Feishu Bot messages and upload selected images or files to target users or chats. It is most useful when a workflow needs reliable Feishu image delivery rather than sending file paths as plain text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to send messages and upload selected images or files through a configured Feishu bot. <br>
Mitigation: Confirm recipients, chat IDs, captions, and absolute file paths before sending, especially for confidential business files. <br>
Risk: Misusing raw paths, webhook bots, expired tokens, or cross-tenant image keys can cause images to be sent as text or fail to display. <br>
Mitigation: Use the configured Feishu message tool with Bot App permissions and verify upload status, token freshness, and tenant alignment when delivery fails. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/InuyashaYang/inuyasha-feishu-img) <br>
- [Image sending pitfalls](references/image-sending-pitfalls.md) <br>
- [Feishu image upload API](https://open.feishu.cn/document/server-docs/im-v1/image/create) <br>
- [Feishu common questions](https://feishu.apifox.cn/doc-1944903) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local file paths, Feishu chat or user IDs, message captions, and required Feishu IM permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
