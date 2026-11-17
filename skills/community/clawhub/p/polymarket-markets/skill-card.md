## Description:

Browse prediction markets, inspect books and balances, and manage orders or positions in Polymarket - powered by ClawLink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to work with Polymarket from chat: discovering markets, reviewing balances and positions, previewing orders, and managing orders after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill requires trusting ClawLink with Polymarket access.

Mitigation: Review connected-account scopes before use and revoke the ClawLink device or Polymarket connection when it is no longer needed.

Risk: Order placement, cancellation, or similar portfolio-affecting actions can affect the user's Polymarket account.

Mitigation: Keep write actions confirmation-only and preview order changes before execution.

Risk: Credential exposure can occur if users paste raw credentials into chat.

Mitigation: Use the hosted ClawLink pairing and connection flows and do not request or repeat raw credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/polymarket-markets)
- [ClawLink](https://claw-link.dev)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Source](https://github.com/hith3sh/clawlink)
- [Polymarket Docs](https://docs.polymarket.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confirmation prompts before portfolio-affecting actions.]

## Skill Version(s):

0.1.0 (source: release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
