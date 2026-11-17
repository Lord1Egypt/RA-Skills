## Description:

Helps users register for PowPow, verify their email, and sign in from chat, with optional subscription checkout support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow users and their agents use this skill to create an account, resolve registration issues, and obtain a one-click sign-in link. It can also guide an optional subscription checkout, but the user completes payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A one-click login link or temporary session state could grant access to the user's account.

Mitigation: Share login links privately, treat temporary state as account access material, and run cleanup when finished.

Risk: Optional checkout may create a paid subscription, including a recurring PayPal plan.

Mitigation: Confirm the plan and renewal terms with the user; only the user should complete payment through the checkout.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/durenzidu/skills/powpow-register-tr)
- [PowPow website](https://global.powpow.online)
- [Registration flow](artifact/references/registration-flow.md)
- [Agent flow](artifact/references/agent-flow.md)
- [Payment and activation](artifact/references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with account access or checkout links when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide an account summary and optional product screenshots.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
