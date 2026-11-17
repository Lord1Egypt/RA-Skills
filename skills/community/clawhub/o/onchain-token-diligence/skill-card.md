## Description:

On-chain Token Diligence helps agents run pre-trade token checks using x402-paid crypto data endpoints for rug and honeypot signals, DEX price and liquidity, whale transfers, and smart-money wallet activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rccola990-cloud](https://clawhub.ai/user/rccola990-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External agents, developers, and crypto analysts use this skill before buying, swapping, recommending, or sizing a token trade. It guides the agent to check token security, DEX market data, whale transfers, and smart-money wallet activity before making a recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to call paid x402 crypto-data endpoints without sufficient payment review.

Mitigation: Require explicit confirmation before each paid request, verify the amount, chain, asset, recipient, and host, and enforce strict session and daily spending limits.

Risk: A payment-capable wallet used by the agent could expose more funds than intended.

Mitigation: Use a dedicated low-balance x402 wallet for this skill rather than a primary wallet.

Risk: Live token diligence signals may be incomplete, stale, or insufficient for a trading decision.

Mitigation: Treat the results as one input to human-reviewed due diligence and corroborate high-risk or high-value decisions before trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rccola990-cloud/skills/onchain-token-diligence)
- [AgentExchange endpoint catalog](https://store.agentexchange.work)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown guidance with HTTP GET request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger paid x402 requests to crypto-data endpoints after payment requirements are presented.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
