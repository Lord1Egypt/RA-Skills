## Description:

Helps users register for PowPow (Bubble), sign in with a one-click link, and optionally set up a membership subscription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

External users can create a PowPow account with guided email verification and one-click sign-in, troubleshoot registration, and choose an optional Alipay or PayPal subscription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles passwords and sign-in links that can grant access to the account.

Mitigation: Treat passwords and generated links as sensitive; share links only with the intended user and clear temporary account state when finished or interrupted.

Risk: The skill can open a payment page for an optional subscription.

Mitigation: Confirm the user's choice before opening the payment page; the user completes payment directly with the cashier.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-en)
- [PowPow official site](https://global.powpow.online)
- [Agent-assisted flow](references/agent-flow.md)
- [Registration guidance](references/registration-flow.md)
- [Subscription and activation guidance](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Links]

**Output Format:** [Conversational Markdown with sign-in and optional payment links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bundled product screenshots; sign-in links grant access to the account.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
