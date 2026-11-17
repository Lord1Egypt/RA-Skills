## Description:

Helps users register for PowPow through chat, verify their email, and sign in with a one-click link, with optional Alipay or PayPal subscription assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to create a PowPow account, resolve registration issues, and obtain a one-click sign-in link. It can also guide optional subscription upgrades and track payment status without making the payment for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration exposes passwords, email verification codes, and sign-in tokens to the agent workflow.

Mitigation: Share only the needed verification code, avoid sharing payment credentials, and protect sign-in links as account access credentials.

Risk: Local status output and temporary files may reveal account and payment workflow details.

Mitigation: Limit access to local output and files, and run cleanup when finished.

Risk: Optional subscription orders can lead to financial commitments.

Mitigation: Confirm the user's choice before creating an order and leave payment authorization to the user.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/durenzidu/skills/powpow-register-ur)
- [PowPow website](https://global.powpow.online)
- [Agent workflow](references/agent-flow.md)
- [Registration workflow](references/registration-flow.md)
- [Payment and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Links]

**Output Format:** [Conversational text with commands and sign-in or checkout links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sign-in links may contain a login token; optional subscription assistance returns payment status.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
