## Description:

Helps people register for PowPow, verify their email, sign in with a one-click link, and optionally upgrade through Alipay or PayPal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

People creating a PowPow account can use this skill to complete registration and email verification with agent assistance, then open a sign-in link. If they choose to subscribe or need access after a trial, the skill guides an optional Alipay or PayPal upgrade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration involves a password and email verification code.

Mitigation: Share the verification code only for the official registration flow; pass the password through an environment variable, never a command argument or saved file.

Risk: One-click login links and locally stored session tokens grant account access.

Mitigation: Treat login links like access tokens, avoid sharing them beyond the intended user, and run cleanup after finishing.

Risk: Subscription setup can direct users to a payment page.

Mitigation: Keep payment optional unless access requires it; complete payments only on official Alipay or PayPal pages and do not share payment credentials with the agent.

## Reference(s):

- [PowPow skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-fa)
- [PowPow website](https://global.powpow.online)
- [Agent-assisted registration flow](references/agent-flow.md)
- [Registration and troubleshooting](references/registration-flow.md)
- [Subscription and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Links]

**Output Format:** [Markdown text with sign-in links and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an account-access link and optional checkout instructions.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
