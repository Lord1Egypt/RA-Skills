## Description:

Helps users register for PowPow, verify their email, and sign in through a guided conversation, with optional help initiating a subscription checkout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow users can get guided account registration, email verification, and one-click sign-in. If they choose a subscription, the agent can initiate checkout and check its status while the user completes payment themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration handles sensitive account details, including email, password, and verification code.

Mitigation: Use only if comfortable submitting those details to the official PowPow service; avoid sharing the password beyond the registration flow.

Risk: Optional checkout creates payment-adjacent data and local checkout HTML files.

Mitigation: Complete payment personally in the opened Alipay or PayPal checkout; run cleanup afterward and delete generated checkout HTML files from shared devices.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-ja)
- [PowPow official site](https://global.powpow.online)
- [Registration flow](references/registration-flow.md)
- [Agent flow](references/agent-flow.md)
- [Payment and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with sign-in and optional checkout links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide account status and payment confirmation guidance.]

## Skill Version(s):

2.2.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
