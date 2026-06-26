## Description: <br>
OpenClaw skill for designing Telegram Bot API workflows and command-driven conversations using direct HTTPS requests without SDKs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovefromio](https://clawhub.ai/user/lovefromio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design Telegram bot command flows, update routing, direct HTTPS Bot API requests, and operational checklists without relying on a full SDK. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens could be exposed if copied into chat logs, generated examples, or application logs. <br>
Mitigation: Treat bot tokens as secrets, use a test bot while experimenting, and avoid logging tokens in generated code or operational output. <br>
Risk: Generated Telegram API calls such as setWebhook, sendMessage, editMessageText, or deleteMessage can affect a production bot or chat if used without review. <br>
Mitigation: Review generated API calls and payloads before using them with a production bot, and validate chat context and update payloads. <br>
Risk: Webhook or polling handlers can receive untrusted or repeated updates. <br>
Mitigation: Use secret webhook headers where possible, restrict allowed update types, and keep handlers idempotent with retry-aware backoff. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lovefromio/lovefromio-telegram) <br>
- [Telegram Bot API](https://core.telegram.org/bots/api) <br>
- [Telegram Bot FAQ](https://core.telegram.org/bots/faq) <br>
- [Telegram Bot API Field Notes](references/telegram-bot-api.md) <br>
- [Telegram Command Playbook](references/telegram-commands-playbook.md) <br>
- [Telegram Request Templates](references/telegram-request-templates.md) <br>
- [Telegram Update Routing](references/telegram-update-routing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP request examples and JSON payload snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces planning guidance and templates; no executable install behavior is included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
