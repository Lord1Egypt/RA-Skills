## Description:

Ojos y manos de una persona con baja vision: manda sus mensajes y sus notas de voz con confirmacion hablada obligatoria, le lee documentos y correo, y le redacta textos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kapitecsoluciones](https://clawhub.ai/user/kapitecsoluciones)

### License/Terms of Use:

MIT

## Use Case:

External users and operators use this skill to guide an agent that assists a person with low vision through a single chat. It supports sending text messages and voice notes with spoken confirmation, reading documents and email on request, and drafting text in the user's tone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send WhatsApp messages on behalf of a user, and evidence.security rates the release as suspicious because some safety promises are not technically enforced.

Mitigation: Install only in a tightly controlled OpenClaw environment and restrict outbound WhatsApp sending to the provided wrapper path.

Risk: The model could bypass the sending procedure if it has broad shell or channel access.

Mitigation: Run the actual send token and channel operation in a separate process or permission boundary, and expose only the narrow send request interface to the agent.

Risk: A voice note may contain secrets because audio forwarding is not content-scanned before sending.

Mitigation: Warn users and operators about this limitation, and avoid forwarding voice notes in workflows where secrets, banking data, or one-time codes may be spoken.

Risk: Inbound chat allow-listing and stop-on-interruption behavior are not fully enforced by the skill itself.

Mitigation: Enforce the single allowed inbound chat outside the model, keep automatic email reading disabled, and test the real audio response path before unattended use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kapitecsoluciones/skills/lazarillo)
- [OpenClaw](https://openclaw.ai)
- [Security Model](references/seguridad.md)
- [Setup Guide](references/montaje.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and spoken-response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is designed for Spanish spoken responses and uses concise status lines for user-facing failures.]

## Skill Version(s):

0.2.0 (source: server release metadata and changelog, released 2026-08-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
