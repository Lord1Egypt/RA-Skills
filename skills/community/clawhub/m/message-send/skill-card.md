## Description:

Provides a Portuguese workflow for using `openclaw message send` to send text, media, buttons, cards, and other payloads across chat channels such as WhatsApp, Telegram, Discord, and Slack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raphacastelloes](https://clawhub.ai/user/raphacastelloes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare and verify OpenClaw chat-send commands, choose channel and target identifiers, and send messages or structured payloads to supported chat services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages may be sent to the wrong channel, account, or recipient if identifiers are not confirmed.

Mitigation: Confirm channel, account, and recipient IDs with OpenClaw channel and directory commands before sending.

Risk: Complex JSON payloads may be malformed or differ across channel implementations.

Mitigation: Use `--dry-run` for complex payloads before sending.

Risk: Chat messages can expose secrets or sensitive personal data.

Mitigation: Avoid sending secrets or sensitive personal data unless that is intentional and authorized.

## Reference(s):

- [Canais Suportados pelo OpenClaw](references/channels.md)
- [Exemplos de Payloads JSON para Mensagens](references/payloads.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples and JSON payload snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional dry-run guidance for complex payloads; no files or code are generated.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
