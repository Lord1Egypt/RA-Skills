## Description:

Mirror Polymarket whale wallets, inspect wallet positions, follow specific trader addresses, or paper-trade copytrading with $SIM before using real money. Polling mode is free; Reactor mode is Pro for event-driven real-time mirroring via Simmer's on-chain signal infrastructure.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and their agents use this framework to inspect Polymarket wallet positions, follow selected trader addresses, and prepare or execute copytrading through Simmer. It can also report account positions and trade results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that simulated venue or dry-run settings may not prevent real-money orders.

Mitigation: Do not rely on those settings to prevent real trades; review the selected venue and trading mode before connecting funds or enabling execution.

Risk: A wallet private key could be exposed if shared in chat.

Mitigation: Never share a wallet private key in chat; store it securely outside the conversation.

Risk: The security scan is incomplete: one of six components was not inspected and one analyzer was degraded.

Mitigation: Treat the scan evidence as incomplete and review the skill before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-copytrading)
- [Simmer API](https://api.simmer.markets)
- [Simmer SDK migration documentation](https://docs.simmer.markets/v2-migration)
- [Simmer dashboard](https://simmer.markets/dashboard)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown text with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet position summaries, trade previews, and execution reports.]

## Skill Version(s):

1.12.9 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
