## Description:

Guides an agent through PowPow account registration, email verification, one-click sign-in, and optional subscription setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

People signing up for PowPow can have an agent assist with registration, email verification, and sign-in, then optionally guide a subscription upgrade or troubleshoot account access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A temporary state file may contain a session token, especially risky on shared machines.

Mitigation: Avoid shared machines and run cleanup after registration.

Risk: The agent can open payment pages and create an optional payment order.

Mitigation: Review the payment page before paying; use manual payment if you prefer not to involve the agent.

Risk: Agent-assisted signup handles an email address, password, and optionally an avatar or phone number.

Mitigation: Use manual registration if you do not want the agent to handle account details.

## Reference(s):

- [PowPow homepage](https://global.powpow.online)
- [Agent flow](references/agent-flow.md)
- [Registration flow](references/registration-flow.md)
- [Payment and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown guidance with registration, sign-in, and optional payment links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes account troubleshooting and optional payment status guidance.]

## Skill Version(s):

2.2.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
