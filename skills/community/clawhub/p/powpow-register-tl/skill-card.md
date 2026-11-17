## Description:

Helps people register for PowPow, verify their email, and sign in through a one-click link, with optional assistance creating and tracking subscription orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to create a PowPow account, resolve common registration issues, and access the service. Users who choose a subscription can receive checkout guidance and payment-status updates without sharing payment credentials with the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The registration flow runs a bundled Node script and handles account and session tokens.

Mitigation: Review the script before installation, limit access to session artifacts, and clear temporary registration state when finished.

Risk: Optional subscription orders can lead users to a payment checkout.

Mitigation: Confirm each payment action, check the browser destination before paying, and keep payment credentials between the user and the checkout provider.

Risk: Temporary payment checkout folders may remain on the device.

Mitigation: Remove temporary powpow-pay checkout folders after use.

## Reference(s):

- [PowPow skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-tl)
- [PowPow website](https://global.powpow.online)
- [Registration flow](references/registration-flow.md)
- [Agent-assisted flow](references/agent-flow.md)
- [Payment and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with registration, sign-in, and optional checkout links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include registration progress and subscription payment-status updates.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
