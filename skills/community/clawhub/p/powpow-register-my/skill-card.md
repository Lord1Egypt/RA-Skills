## Description:

Helps users register and sign in to PowPow through an agent-guided conversation, with optional subscription checkout assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow users and their agents use this skill to create an account, verify an email address, obtain sign-in links, and troubleshoot registration. Users can also request help with an optional Alipay or PayPal subscription upgrade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account setup involves an email address, verification code, password choice, and possibly an avatar or phone number.

Mitigation: Install only when account creation is wanted, share only the details needed for registration, and run cleanup afterward to remove temporary token state.

Risk: Optional subscription assistance can lead to a payment checkout page.

Mitigation: Confirm before opening a generated checkout page and complete payment only on the official Alipay or PayPal page.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-my)
- [PowPow website](https://global.powpow.online)
- [Registration flow](artifact/references/registration-flow.md)
- [Payment and activation](artifact/references/payment-and-activation.md)
- [Agent flow](artifact/references/agent-flow.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Links]

**Output Format:** [Markdown with links and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include registration or sign-in links and optional checkout instructions.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
