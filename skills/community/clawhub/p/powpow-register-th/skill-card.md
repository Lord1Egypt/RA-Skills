## Description:

Helps users register a PowPow account, verify their email, sign in through a one-click link, and optionally arrange an Alipay or PayPal membership upgrade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow users can ask an agent to guide account registration, email verification, and sign-in without leaving the conversation except to retrieve their verification code. Users who choose a membership upgrade can receive help opening checkout and checking activation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration involves an email address, verification code, password, and login token.

Mitigation: Share sensitive details only for the intended registration, avoid exposing them to others, and run cleanup afterward to remove local session state.

Risk: Optional membership checkout may create a payment order.

Mitigation: Start checkout only when the user requests it, and let the user confirm and complete payment themselves.

## Reference(s):

- [PowPow skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-th)
- [PowPow website](https://global.powpow.online)
- [Registration flow](artifact/references/registration-flow.md)
- [Payment and activation](artifact/references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with registration instructions, command examples, and sign-in or optional checkout links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides account setup and optional membership activation; does not create posts or digital humans.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
