## Description: <br>
Sends Feishu/Lark interactive card messages with reusable templates, validation, token handling, and single-recipient or group delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calmTime](https://clawhub.ai/user/calmTime) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to build and send Feishu/Lark interactive card notifications for news, travel deals, tasks, status updates, and workflow messages to approved users or chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends live Feishu/Lark messages and can reach users or groups when configured with valid credentials. <br>
Mitigation: Use only credentials you control, apply least-privilege app scopes, test with approved recipients first, and confirm the recipient list before production sends. <br>
Risk: The server security summary flags restriction-bypass framing around direct Feishu/Lark messaging. <br>
Mitigation: Review organizational messaging policy before installation and use approved Feishu/Lark APIs, scopes, and recipient workflows. <br>
Risk: Message payloads and targets may be exposed through logs or demo/test harness output. <br>
Mitigation: Disable verbose logging in production, redact message content and identifiers, and avoid sending sensitive content unless organizational policy allows it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calmTime/lark-card-sender) <br>
- [Feishu/Lark message create API](https://open.larkoffice.com/document/server-docs/im-v1/message/create) <br>
- [Feishu/Lark interactive card message format](https://open.larkoffice.com/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json) <br>
- [Artifact integration guide](artifact/feishu_card_integration_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and JavaScript code examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate live Feishu/Lark message delivery when used with valid credentials and recipients.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
