## Description:

Helps users create a PowPow account in conversation, verify their email, and open a one-click login link, with optional subscription assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

New PowPow users can complete assisted registration and email verification, receive a one-click login link, and optionally navigate subscription checkout or registration problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session-login data is stored in a predictable temporary file.

Mitigation: Use a trusted single-user machine or isolated agent environment and run cleanup after registration.

Risk: One-click login links contain tokens that can grant account access if shared.

Mitigation: Send login links only to the intended user and do not share or publish them.

Risk: Subscription checkout involves payment credentials.

Mitigation: Enter payment credentials only in the official Alipay or PayPal checkout; the agent should not handle them.

## Reference(s):

- [PowPow registration skill on ClawHub](https://clawhub.ai/durenzidu/skills/powpow-register-ml)
- [PowPow official site](https://global.powpow.online)
- [Agent registration flow](references/agent-flow.md)
- [Registration and troubleshooting](references/registration-flow.md)
- [Payment and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Conversational text with login links and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide an account summary and optional checkout instructions; login links grant session access.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
