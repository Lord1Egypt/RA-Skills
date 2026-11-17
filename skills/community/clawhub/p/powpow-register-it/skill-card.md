## Description:

Helps people register for PowPow (Bolla) through a conversation, including email verification, one-click sign-in, and optional subscription assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

People signing up for PowPow (Bolla) use this skill to create an account, verify their email, and receive a one-click sign-in link. It can guide optional subscription checkout and help resolve registration problems; if Node.js is unavailable, it provides manual registration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One-click sign-in links and temporary session state can grant account access if exposed.

Mitigation: Treat sign-in links as private and run cleanup when the registration flow ends.

Risk: Optional subscription checkout involves payment information.

Mitigation: Enter payment credentials only on the official Alipay or PayPal checkout pages; do not share them with the agent.

Risk: An optional avatar image is uploaded to PowPow during registration.

Mitigation: Provide an avatar path only if you intend to upload that image.

## Reference(s):

- [PowPow website](https://global.powpow.online)
- [PowPow registration](https://global.powpow.online/register)
- [ClawHub skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-it)
- [Agent flow](artifact/references/agent-flow.md)
- [Registration flow](artifact/references/registration-flow.md)
- [Payment and activation](artifact/references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown messages with sign-in or optional checkout links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registration status and next-step guidance; optional account summary.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
