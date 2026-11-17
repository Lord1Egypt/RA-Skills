## Description:

Helps people register for PowPow (Bubble), verify their email, and access their new account, with optional assistance initiating a membership upgrade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

People signing up for PowPow use this skill to complete account registration and email verification with an agent, then open a one-click login link. If they choose to upgrade or access requires a subscription, the agent can initiate an Alipay or PayPal checkout for the user to complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration involves a password and email verification code.

Mitigation: Share these only deliberately; keep the password out of command arguments, use the code only for the intended registration, and run cleanup when finished.

Risk: One-click login links grant access to the user's account.

Mitigation: Treat login links as sensitive and do not forward or publish them.

Risk: An optional membership upgrade opens an Alipay or PayPal checkout.

Mitigation: Verify the payment page and terms yourself before completing any payment.

## Reference(s):

- [PowPow skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-vi)
- [PowPow website](https://global.powpow.online)
- [Agent registration workflow](artifact/references/agent-flow.md)
- [Registration guidance](artifact/references/registration-flow.md)
- [Payment and activation guidance](artifact/references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands]

**Output Format:** [Markdown with links and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a one-click login link or optional checkout link; the user completes payment on the provider's page.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
