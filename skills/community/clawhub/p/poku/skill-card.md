## Description: <br>
Poku lets an agent use the Poku API to place calls, send SMS, WhatsApp, and Slack messages, manage dedicated phone numbers, and configure inbound webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emileindik](https://clawhub.ai/user/emileindik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use Poku to let an agent coordinate calls and messages, reserve phone numbers, and set up inbound communication flows that can deliver call or message events to an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook features can persistently forward private call and message data. <br>
Mitigation: Create webhooks only to destinations the user controls, use a signing secret when possible, and avoid forwarding full message bodies, call summaries, or customer information to third-party channels unless everyone involved has consented. <br>
Risk: The skill can place calls or send messages to external recipients. <br>
Mitigation: Confirm the recipient, channel, E.164 phone number or Slack ID, and full message or call plan with the user before executing. <br>
Risk: The skill requires a sensitive Poku API key. <br>
Mitigation: Use a dedicated Poku API key where possible and mask bearer tokens or resolved keys in user-facing output. <br>
Risk: Phone number release is irreversible and can affect inbound communication. <br>
Mitigation: List the number being released and require explicit confirmation before deleting it. <br>


## Reference(s): <br>
- [Poku ClawHub release](https://clawhub.ai/emileindik/poku) <br>
- [Poku homepage](https://pokulabs.com) <br>
- [Full API reference for LLMs](https://docs.pokulabs.com/llms.txt) <br>
- [Interactive Poku docs](https://docs.pokulabs.com) <br>
- [Poku webhook documentation](https://docs.pokulabs.com/poku-skill/webhook) <br>
- [OpenClaw webhook reference](https://docs.openclaw.ai/automation/webhook) <br>
- [Poku API Reference](references/API.md) <br>
- [Calls](references/CALLS.md) <br>
- [Call Templates](references/CALL-TEMPLATES.md) <br>
- [Messages](references/MESSAGES.md) <br>
- [Message Templates](references/MESSAGE-TEMPLATES.md) <br>
- [Phone Number Reservation and Management](references/NUMBERS.md) <br>
- [Webhooks and Inbound Configuration](references/WEBHOOKS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with JSON and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POKU_API_KEY; calls, messages, number reservations, number releases, and webhook changes should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
