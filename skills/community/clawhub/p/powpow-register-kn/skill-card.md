## Description:

Helps users register for PowPow in a conversation, verify their email, and open a one-click login link, with optional subscription guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

People signing up for PowPow use the skill to complete account registration and email verification with an agent, then access their account. It can guide an optional Alipay or PayPal membership upgrade, but does not create posts or digital humans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shared temporary login state file can mix accounts across conversations on the same host.

Mitigation: Avoid concurrent registrations and shared service accounts; for multi-user hosts, use per-user state with token expiry and locking, and clean up after each workflow.

Risk: The agent sees registration details and token-bearing login links.

Mitigation: Use only in an authorized private conversation, avoid sharing login links, and keep payment credentials with the Alipay or PayPal checkout.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-kn)
- [PowPow website](https://global.powpow.online)
- [Registration flow](artifact/references/registration-flow.md)
- [Payment and activation](artifact/references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Links]

**Output Format:** [Conversational text with registration, login, and optional payment links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires email verification; agent-assisted actions require Node.js 18 or later, otherwise guidance-only.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
