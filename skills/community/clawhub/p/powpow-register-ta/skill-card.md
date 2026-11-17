## Description:

Helps people create a PowPow account, sign in with a one-click link, and optionally arrange a membership payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

People new to PowPow use this skill to learn about the service, register with an email verification code, and receive a sign-in link. It can also guide optional Alipay or PayPal membership checkout and troubleshoot registration or activation issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration shares an email address, username, and optional avatar with PowPow.

Mitigation: Confirm the user wants to register and upload any selected avatar before submitting their information to global.powpow.online.

Risk: One-click sign-in uses a local login token that may expose account access on a shared machine.

Mitigation: Prefer a single-user machine, avoid sharing sign-in links, and run cleanup after registration to remove the local token.

Risk: Optional membership orders can lead to an unintended or misdirected payment.

Mitigation: Create an order only on request, and have the user verify the checkout destination and amount before paying.

## Reference(s):

- [PowPow website](https://global.powpow.online)
- [Registration flow](references/registration-flow.md)
- [Agent-assisted flow](references/agent-flow.md)
- [Payment and activation](references/payment-and-activation.md)
- [Screenshot guide](references/screenshots.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text with links and optional product screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide a one-click sign-in link and, if requested, a payment checkout link.]

## Skill Version(s):

2.2.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
