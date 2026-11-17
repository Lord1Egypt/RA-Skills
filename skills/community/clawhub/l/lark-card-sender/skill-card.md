## Description:

Provides Feishu/Lark interactive card sending helpers with templates, validation, token handling, and group or direct message delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calmtime](https://clawhub.ai/user/calmtime)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation builders use this skill to create and send Feishu/Lark interactive card messages for notifications, summaries, tasks, system status, and similar workflow updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python examples and test paths can send live Feishu/Lark messages to fixed recipient IDs when real credentials are present.

Mitigation: Replace or remove hard-coded recipient IDs and test only with approved staging users or groups before using production credentials.

Risk: Card content, recipient identifiers, and message payloads may be sent to Feishu/Lark or printed in logs.

Mitigation: Treat card inputs as external message data, avoid secrets or sensitive content, and keep FEISHU_APP_SECRET in a secrets manager or private environment.

Risk: The JavaScript sender reports delivery success without a real authenticated transport and logs full payloads.

Mitigation: Do not rely on the JavaScript sender for production delivery until it uses a verified Feishu/Lark transport and redacts payload logging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calmtime/skills/lark-card-sender)
- [Feishu message create API](https://open.larkoffice.com/document/server-docs/im-v1/message/create)
- [Feishu interactive card JSON format](https://open.larkoffice.com/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json)
- [OpenClaw Feishu extension](https://github.com/openclaw/openclaw/tree/main/extensions/feishu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and JavaScript code examples and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce runnable examples that send card content and recipient identifiers to Feishu/Lark.]

## Skill Version(s):

1.0.0 (source: server release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
