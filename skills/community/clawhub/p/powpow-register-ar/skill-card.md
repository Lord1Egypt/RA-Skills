## Description:

Helps new users create a PowPow account, verify their email, and sign in through a one-click link, with optional Alipay or PayPal subscription assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to guide or complete PowPow registration, including email verification and optional subscription setup. The agent can provide self-service instructions when its registration script cannot run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A login token is stored in a predictable temporary file that other local users could access.

Mitigation: Use a single-user machine, restrict access to local temporary files, and run cleanup when registration is complete.

Risk: Registration involves a password and an email verification code.

Mitigation: Share the code only for the official registration flow, keep the password private, and avoid retaining credentials after signup.

Risk: Optional subscription upgrades open payment pages.

Mitigation: Confirm the upgrade is wanted and complete payment only on the official Alipay or PayPal page.

## Reference(s):

- [PowPow Register on ClawHub](https://clawhub.ai/durenzidu/skills/powpow-register-ar)
- [PowPow website](https://global.powpow.online)
- [Agent registration flow](artifact/references/agent-flow.md)
- [Registration rules](artifact/references/registration-flow.md)
- [Payment and activation](artifact/references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Links]

**Output Format:** [Markdown with links and step-by-step instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a one-click sign-in link or an optional payment link.]

## Skill Version(s):

2.2.0 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
