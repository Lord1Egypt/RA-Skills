## Description:

Email sending skill via SMTP or API providers. Supports attachments, HTML templates, and batch sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send individual emails, automated notifications, HTML messages with attachments, or batch email campaigns through SMTP or supported email API providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound email, attachments, and batch campaigns can send unintended, sensitive, or non-compliant messages.

Mitigation: Use only where outbound email is intended and recipients, message content, attachments, consent, and anti-spam obligations are reviewed before sending.

Risk: SMTP or email API credentials can grant broad email-sending capability if over-scoped or exposed.

Mitigation: Use appropriately scoped credentials, store them securely, and avoid embedding secrets in prompts, source files, logs, or shared artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-email-sender)
- [ClawHub publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger outbound email delivery, attachments, and batch sends when configured with SMTP or provider credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
