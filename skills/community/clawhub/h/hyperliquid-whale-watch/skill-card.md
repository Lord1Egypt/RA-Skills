## Description:

Track what Hyperliquid's 40 largest accounts are actually doing with BTC - who opened, added, cut, closed or flipped long/short, the net BTC they bought or sold over the last hour or day, and the biggest moves by wallet. Real on-chain data from AgentReeve, no API key; free sample, live data over x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shakeelamjid](https://clawhub.ai/user/shakeelamjid)

### License/Terms of Use:

MIT-0

## Use Case:

External users and traders use the skill to summarize current positions and recent BTC activity among Hyperliquid's 40 largest accounts, with optional cross-exchange positioning context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live x402 request may incur a charge of up to $0.25 per task without prior confirmation.

Mitigation: Use the free sample when you do not want a charge; review the payment quote and stay within the stated $0.25 per-task cap, requesting approval above it.

Risk: The security review was partial because some local references could not be resolved, so its evidence is incomplete.

Mitigation: Review the unresolved references and assess the full skill before installation or use.

## Reference(s):

- [Source skill on GitHub](https://github.com/shakeelamjid/agentreeve-skills/tree/main/hyperliquid-whale-watch)
- [ClawHub release](https://clawhub.ai/shakeelamjid/skills/hyperliquid-whale-watch)
- [AgentReeve free whale data sample](https://agentreeve.com/api/v1/samples/whales)
- [AgentReeve live whale data endpoint](https://agentreeve.com/api/v1/whales?hours=24)
- [AgentReeve BTC market positioning endpoint](https://agentreeve.com/api/v1/positioning?asset=BTC)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Concise natural-language summary of positions, BTC flows, and largest account moves]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports data gaps instead of estimating; market data is observational and not financial advice.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
