## Description:

Manage outbound notifications across WhatsApp, Telegram, and email with templates, scheduling, delivery tracking, and rate limiting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engibarian](https://clawhub.ai/user/engibarian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage outbound WhatsApp, Telegram, and email notifications with reusable templates, scheduling, delivery tracking, and rate limiting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce instructions and templates for real outbound messages.

Mitigation: Review before installing in any environment that can send messages and require explicit operator confirmation for sends and broadcasts.

Risk: Example recipients, caller-supplied links, and high-priority sends can create misuse or delivery-abuse paths.

Mitigation: Replace example recipients with placeholders, validate or generate links server-side, and restrict high-priority use with authorization and bounded quotas.

Risk: Delivery logs and opt-out handling can create privacy or consent risk.

Mitigation: Protect or minimize delivery logs and enforce consent and opt-outs before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engibarian/skills/notification-system)
- [Skill definition](artifact/SKILL.md)
- [Template index](artifact/templates/index.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown templates, JSON queue and rate-limit configuration, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes channel-specific templates, pending queue data, rate limits, and delivery tracking guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
