## Description:

Helps users register for PowPow (Bubble), verify their email, sign in, and optionally navigate subscription activation through chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

People signing up for PowPow use this skill to receive registration guidance, complete email verification, and obtain a sign-in link. It can also guide optional Alipay or PayPal subscription activation while the user completes any payment themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account creation sends the user's email and registration details to PowPow.

Mitigation: Get the user's consent and confirm their details before submitting registration.

Risk: A login token and payment state are temporarily stored in a predictable local file, which could be exposed on a shared machine.

Mitigation: Avoid shared machines and run the skill's cleanup command after the flow.

Risk: The skill can open a local payment page for an optional subscription.

Mitigation: Require confirmation before opening any payment page; the user completes payment themselves.

## Reference(s):

- [PowPow skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-pcm)
- [PowPow platform](https://global.powpow.online)
- [Agent flow](references/agent-flow.md)
- [Registration flow](references/registration-flow.md)
- [Payment and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Images]

**Output Format:** [Conversational Markdown with sign-in links and optional product screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Payment pages are optional; the user completes payment on the provider's page.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
