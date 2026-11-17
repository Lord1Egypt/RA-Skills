## Description:

Helps users register for PowPow, verify their email, and access their account through a one-click login link, with optional membership payment guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

People signing up for PowPow can use this skill to complete registration, troubleshoot verification or activation, and optionally arrange a membership payment through the official checkout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent handles an account password or generated password and an email verification code during registration.

Mitigation: Use the skill only if comfortable sharing these with the agent; choose the manual web flow on shared or privacy-sensitive systems.

Risk: Generated one-click login links can grant access if disclosed in screenshots, messages, or logs.

Mitigation: Treat login links like passwords, do not share screenshots or logs containing them, and run cleanup after use.

Risk: Optional membership setup creates payment links and orders.

Mitigation: Review the order and complete any payment yourself through the official checkout.

## Reference(s):

- [PowPow registration skill on ClawHub](https://clawhub.ai/durenzidu/skills/powpow-register-id)
- [PowPow registration page](https://global.powpow.online/register)
- [Registration flow](artifact/references/registration-flow.md)
- [Payment and activation guidance](artifact/references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Links]

**Output Format:** [Conversational registration guidance with account and checkout links when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer for assisted registration; otherwise offers a manual web flow.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
