## Description:

OpenClaw skill for designing Telegram Bot API workflows and command-driven conversations using direct HTTPS requests (no SDKs).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovefromio](https://clawhub.ai/user/lovefromio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design Telegram Bot API command flows, webhook or polling update handling, direct HTTPS request payloads, and operational checklists for bot releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram bot tokens, webhook secrets, or update payloads could be exposed through generated examples, logs, or source control.

Mitigation: Keep tokens and webhook secrets out of logs and source control, use a secret store or environment variables, and review generated bot code before use.

Risk: A bot that accepts broad or unvalidated update types can process unexpected chats, callbacks, or payloads.

Mitigation: Restrict allowed update types, validate incoming update payloads and chat context, and use a webhook secret token header when webhooks are enabled.

Risk: Generated HTTP requests can send messages, change webhook settings, or trigger Bot API side effects if executed without review.

Mitigation: Treat generated requests as proposals, inspect endpoint, token, chat_id, and payload values, and test in a controlled bot or chat before production use.

## Reference(s):

- [Telegram Bot API Field Notes](references/telegram-bot-api.md)
- [Telegram Command Playbook](references/telegram-commands-playbook.md)
- [Telegram Request Templates (HTTP)](references/telegram-request-templates.md)
- [Telegram Update Routing](references/telegram-update-routing.md)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram Bot FAQ](https://core.telegram.org/bots/faq)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with HTTP request templates and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Bot API endpoint plans, command routing tables, webhook or polling configuration, and operational checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
