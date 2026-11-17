## Description:

Helps users register for PowPow, verify their email and sign in through a guided conversation, with optional assistance starting an Alipay or PayPal subscription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow users can ask an agent to help create an account, troubleshoot email verification and sign in. If they choose a subscription, the agent can initiate checkout and check activation; posting and creating digital people are outside this skill's scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated login links can grant access to an active session.

Mitigation: Treat login links as sensitive, avoid sharing them and run cleanup when finished.

Risk: Order and subscription details may appear in status output or checkout files.

Mitigation: Do not share status output; review checkout files and any browser-opening step before payment.

## Reference(s):

- [PowPow registration skill on ClawHub](https://clawhub.ai/durenzidu/skills/powpow-register-bho)
- [PowPow website](https://global.powpow.online)
- [Agent workflow](references/agent-flow.md)
- [Registration guidance](references/registration-flow.md)
- [Subscription and activation guidance](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Links]

**Output Format:** [Conversational text with commands and sign-in or checkout links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer for assisted registration; otherwise provides manual guidance.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
