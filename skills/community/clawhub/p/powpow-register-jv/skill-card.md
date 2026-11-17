## Description:

Helps users register for PowPow, verify their email, and sign in through a one-click link, with optional assistance for Alipay or PayPal membership upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

People creating a PowPow account use this skill to complete email verification and sign in with agent assistance. They can optionally ask the agent to initiate a membership upgrade; payment is completed in a browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent handles an account password and email verification code during registration.

Mitigation: Use a unique password, share the verification code only for this registration, and avoid displaying or retaining either credential unnecessarily.

Risk: A temporary local login token and sign-in link can grant access to the account.

Mitigation: Treat the link as a credential, share it only with the intended user, and run cleanup after registration.

Risk: Optional checkout can open a browser payment page; PayPal membership renews automatically.

Mitigation: Confirm the user's choice before opening checkout, complete payment only in the official Alipay or PayPal browser flow, and review renewal terms before authorizing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-jv)
- [PowPow website](https://global.powpow.online)
- [Agent workflow](references/agent-flow.md)
- [Registration guidance](references/registration-flow.md)
- [Payment and activation guidance](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Links]

**Output Format:** [Markdown text with registration instructions, commands, and sign-in or checkout links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can share bundled product screenshots; does not create posts or digital humans.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
