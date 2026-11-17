## Description:

Helps users create a PowPow account, verify their email, and sign in, with optional guidance for membership upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to register for PowPow, verify their email, and sign in. They can also request help with an optional membership upgrade or registration problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signup requires an email address, password, and verification code.

Mitigation: Keep the password out of command arguments and files, and use the verification code only for registration with PowPow.

Risk: A temporary login token may remain after registration.

Mitigation: Clean up temporary registration state when the process is complete.

Risk: Optional membership upgrades involve a real payment.

Mitigation: Confirm the payment method with the user; have them complete payment only on the official Alipay or PayPal page.

## Reference(s):

- [PowPow website](https://global.powpow.online)
- [PowPow registration](https://global.powpow.online/register)
- [PowPow Register ClawHub listing](https://clawhub.ai/durenzidu/skills/powpow-register-pnb)
- [Registration flow](references/registration-flow.md)
- [Agent flow](references/agent-flow.md)
- [Payment and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with links and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include registration steps, one-click sign-in links, and optional payment instructions.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
