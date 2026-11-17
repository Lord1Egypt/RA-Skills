## Description:

Helps users register a PowPow account, verify their email, and open a one-click login link through an agent conversation, with optional subscription assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow users can ask an agent to guide or complete account registration, troubleshoot verification and activation, and optionally help initiate a subscription purchase. The user supplies account details and an email verification code and completes any payment themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared temporary session state can mix accounts across simultaneous or stale registration runs under one OS account.

Mitigation: Run only one PowPow registration workflow at a time per OS account and clean up temporary state promptly.

Risk: A generated one-click login link grants access to the user's session if shared.

Mitigation: Send the link only to the intended user and do not share or publish it.

## Reference(s):

- [PowPow Register on ClawHub](https://clawhub.ai/durenzidu/skills/powpow-register-te)
- [PowPow official site](https://global.powpow.online)
- [Agent workflow reference](artifact/references/agent-flow.md)
- [Registration workflow reference](artifact/references/registration-flow.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Conversational text with links and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide an account summary and a one-click login link.]

## Skill Version(s):

2.2.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
