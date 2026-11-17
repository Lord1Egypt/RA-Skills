## Description:

Helps users register a PowPow account, verify their email, and sign in, with optional assistance for an Alipay or PayPal membership upgrade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

People creating a PowPow account can use an agent to complete registration, troubleshoot verification, and obtain a sign-in link. If they choose a membership upgrade, the agent can help open checkout and check payment status without completing payment for them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration handles personal details, an email verification code, and optionally an avatar.

Mitigation: Share the code only for PowPow account verification and provide only the details needed for registration.

Risk: A temporary session token and order details may remain after the flow.

Mitigation: Run the provided cleanup step when finished and avoid sharing sign-in links or session details.

Risk: Optional membership checkout could result in a payment.

Mitigation: Confirm that the user wants the upgrade; let them complete payment themselves on the official Alipay or PayPal cashier page.

## Reference(s):

- [PowPow registration skill on ClawHub](https://clawhub.ai/durenzidu/skills/powpow-register-pa)
- [PowPow registration page](https://global.powpow.online/register)
- [Registration flow](artifact/references/registration-flow.md)
- [Payment and activation flow](artifact/references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Links]

**Output Format:** [Conversational text and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes sign-in and optional checkout links; provides guided registration if automated assistance is unavailable.]

## Skill Version(s):

2.2.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
