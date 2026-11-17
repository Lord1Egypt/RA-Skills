## Description:

Guides users through PowPow account registration, email verification and one-click login, with optional subscription assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

External users can create a PowPow account with agent-assisted registration, verify their email and sign in. If desired, the agent can help open an optional subscription checkout while the user completes payment directly with the provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent handles an email verification code, optional avatar and temporary login token during account creation.

Mitigation: Use the agent only if comfortable sharing these with it, and run cleanup when registration is complete.

Risk: Optional subscription checkout involves payment information.

Mitigation: Do not share payment credentials with the agent; complete payment only in the official Alipay or PayPal cashier.

## Reference(s):

- [PowPow website](https://global.powpow.online)
- [PowPow registration](https://global.powpow.online/register)
- [Agent-assisted registration flow](artifact/references/agent-flow.md)
- [Registration and troubleshooting](artifact/references/registration-flow.md)
- [Payment and activation](artifact/references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with registration guidance and a one-click login link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a temporary login link and optional checkout instructions.]

## Skill Version(s):

2.2.0 (source: ClawHub release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
