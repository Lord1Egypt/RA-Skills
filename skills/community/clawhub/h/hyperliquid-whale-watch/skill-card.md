## Description:

Track what Hyperliquid's 40 largest accounts are actually doing with BTC - who opened, added, cut, closed or flipped long/short, the net BTC they bought or sold over the last hour or day, and the biggest moves by wallet. Real on-chain data from AgentReeve, no API key; free sample, live data over x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shakeelamjid](https://clawhub.ai/user/shakeelamjid)

### License/Terms of Use:

MIT-0

## Use Case:

People monitoring Bitcoin activity on Hyperliquid can use this skill to summarize the positioning and recent trades of the venue's 40 largest accounts, including notable wallet moves. The report is observational market data, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live x402 requests can incur charges, and the security scan flags paid requests as a potential concern.

Mitigation: Use the free sample when live data is unnecessary. Before a paid call, check the quote against the specified recipient, Base network, USDC asset, and $0.25 per-task limit; ask before spending more.

Risk: The security scan was partial because a referenced local path was missing, so its evidence is incomplete.

Mitigation: Review the complete skill and any referenced files before enabling paid calls; do not treat the partial scan as a complete security assessment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shakeelamjid/skills/hyperliquid-whale-watch)
- [Server-resolved GitHub source](https://github.com/shakeelamjid/agentreeve-skills/tree/main/hyperliquid-whale-watch)
- [Free whale-flow sample](https://agentreeve.com/api/v1/btc/samples/whale-flow)
- [Live whale-flow data](https://agentreeve.com/api/v1/btc/whale-flow?hours=24)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown summary of account positioning, one-hour and 24-hour flows, action counts, and largest moves]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers the 40 largest Hyperliquid accounts; reports observed data and does not provide financial advice.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
