## Description:

Guides users through PowPow account registration and one-click sign-in within a conversation, with optional subscription payment assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to create a PowPow account, verify email, sign in, and optionally arrange a subscription or troubleshoot activation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email verification codes, passwords, and account session tokens may be exposed during assisted registration.

Mitigation: Share codes and credentials only in the intended session, keep generated sign-in links private, and run cleanup when finished.

Risk: The agent can create optional subscription payment orders without sufficient user-facing confirmation.

Mitigation: Obtain explicit user approval for the plan and payment method before creating an order; let the user complete payment at the official checkout.

## Reference(s):

- [PowPow skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-sw)
- [PowPow platform](https://global.powpow.online)
- [Agent flow](references/agent-flow.md)
- [Registration flow](references/registration-flow.md)
- [Payment and activation](references/payment-and-activation.md)
- [Product screenshots](references/screenshots.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Images, Guidance]

**Output Format:** [Conversational text with links, optional screenshots, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide sensitive one-click sign-in links and optional checkout links.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
