## Description:

GoCreative Crypto provides paid HTTPS endpoints for live crypto and DeFi market data, including spot prices, market data, DEX liquidity, protocol TVL, gas prices, sentiment, trending coins, and stablecoin data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinhughes2121](https://clawhub.ai/user/colinhughes2121)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI agents use this skill to retrieve live crypto and DeFi market data for trading, research, treasury, and on-chain analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated polling or bundled crypto-360 calls may charge the user's x402 wallet.

Mitigation: Use wallet budgets or approval controls before repeated calls, polling workflows, or bundle calls.

Risk: Market lookup requests are sent to GoCreative's external API.

Mitigation: Avoid placing private trading strategy details or sensitive identifiers in lookup parameters.

Risk: Agents may rely on live crypto market data for trading, research, or treasury decisions.

Mitigation: Treat responses as decision support and require appropriate review before financial action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/colinhughes2121/skills/gocreative-crypto)
- [GoCreative API](https://api.gocreativeai.com)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [Markdown guidance with HTTPS endpoint examples; API responses are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid external API calls via x402; most endpoints are disclosed as about $0.01 per call and the crypto-360 bundle as about $0.20 per call.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
