## Description:

Helps users register a PowPow Bubble account, verify their email, sign in, and optionally upgrade through Alipay or PayPal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create a PowPow Bubble account, complete email verification, and sign in with agent assistance. It can also guide an optional subscription checkout or provide manual registration guidance when automation is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account credentials and a temporary session token may be handled locally during registration.

Mitigation: Review the workflow before installing, limit access to account information, and run cleanup when finished.

Risk: Creating a checkout order or opening a browser window may initiate an unintended payment flow.

Mitigation: Confirm with the user before creating any order or opening checkout; never provide payment credentials to the agent.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-yo)
- [PowPow website](https://global.powpow.online)
- [Registration flow](artifact/references/registration-flow.md)
- [Agent flow](artifact/references/agent-flow.md)
- [Payment and activation](artifact/references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Conversational text with registration guidance, account links, and optional commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bundled product screenshots and links to sign-in or checkout.]

## Skill Version(s):

2.2.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
