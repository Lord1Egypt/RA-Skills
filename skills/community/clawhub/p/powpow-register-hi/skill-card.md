## Description:

Helps users register for PowPow through a conversation, complete email verification, open a one-click login link, and optionally arrange a membership checkout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow users can create an account and sign in with the agent's guidance, providing their own email verification code. If they choose a membership, the agent can arrange checkout and check its status while the user completes payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration handles an email address, verification code, optional avatar, and password.

Mitigation: Install only if you trust PowPow; pass the password through an environment variable and share the verification code only for registration.

Risk: An optional membership checkout involves a financial transaction.

Mitigation: Let the agent arrange checkout and check status, but complete payment yourself after confirming the browser is on an official Alipay or PayPal page.

Risk: Temporary account state contains a login token.

Mitigation: Run the skill's cleanup command when finished to remove temporary token state.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-hi)
- [PowPow website](https://global.powpow.online)
- [Agent flow](references/agent-flow.md)
- [Registration flow](references/registration-flow.md)
- [Payment and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Links]

**Output Format:** [Conversational text with links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a one-click login link, optional checkout link, and account summary.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
