## Description: <br>
Pywayne Lark Custom Bot helps agents send Feishu/Lark channel messages through a webhook, including text, images, rich text posts, interactive cards, shared chat content, signatures, and mentions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to send Lark/Feishu bot messages to channels, including text, images, rich posts, interactive cards, shared chats, and mentions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post visible messages to shared Lark/Feishu channels, including @all mentions, images, rich posts, interactive cards, and shared chat content. <br>
Mitigation: Require confirmation before posting, using @all mentions, uploading images, or sharing chats, and review the destination channel and message content before sending. <br>
Risk: The skill uses sensitive bot credentials such as webhook URLs, signing secrets, app IDs, and app secrets. <br>
Mitigation: Store credentials securely, avoid exposing them in shared prompts or outputs, rotate exposed secrets, and use least-privileged bot or app credentials. <br>
Risk: Image upload and bot actions depend on an external pywayne package before real credentials are used. <br>
Mitigation: Verify the package source and dependency version before connecting production credentials or sending sensitive images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyendt/lark-custom-bot) <br>
- [Feishu](https://www.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown with Python code snippets and configuration placeholders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Credential placeholders should be supplied by the user and handled outside shared output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
