## Description:

Helps users register for PowPow and sign in with one click, with optional assistance for membership checkout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow users can create an account through a guided conversation, confirm an email code, and receive a sign-in link. If they choose membership, the agent can prepare a checkout and check payment status; the user completes payment themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends account details to PowPow and temporarily stores a login token on the user's system.

Mitigation: Install only if you intend to create an account; run the provided cleanup command when finished.

Risk: One-click sign-in links contain a login token and can grant access if shared.

Mitigation: Keep generated sign-in links private.

Risk: Optional membership checkout involves a financial transaction.

Mitigation: Complete payment yourself; do not give payment credentials to the agent.

## Reference(s):

- [PowPow skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-ha)
- [PowPow platform](https://global.powpow.online)
- [Agent flow](references/agent-flow.md)
- [Registration flow](references/registration-flow.md)
- [Payment and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with sign-in and optional checkout links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include account details and locally bundled product screenshots.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
