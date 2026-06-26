## Description: <br>
Send images via Feishu (Lark) messaging platform using the underlying API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo-jiqimao](https://clawhub.ai/user/leo-jiqimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to send a local image file to a Feishu user or group chat, including images produced by another agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends local image files to Feishu users or group chats, which can disclose generated, private, or sensitive images if the path or recipient is wrong. <br>
Mitigation: Confirm the exact image path and recipient or chat ID before sending, especially for sensitive or batch image workflows. <br>
Risk: The skill reads Feishu app credentials from the OpenClaw configuration. <br>
Mitigation: Keep the OpenClaw configuration private and use a least-privilege Feishu app with only the permissions needed to send images. <br>


## Reference(s): <br>
- [Feishu Open Platform Documentation](https://open.feishu.cn/document/home/index) <br>
- [Feishu Send Message API](https://open.feishu.cn/document/server-docs/im-v1/message/create) <br>
- [Feishu Upload Image API](https://open.feishu.cn/document/server-docs/im-v1/image/create) <br>
- [ClawHub Skill Page](https://clawhub.ai/leo-jiqimao/leo-feishu-send-image) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends a selected local image through Feishu after reading Feishu app credentials from the user's OpenClaw configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
