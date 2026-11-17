## Description:

Live Hyperliquid intelligence with no API key, paid per call via x402 ($0.02 to $0.25). Stock, index, gold and oil perps 24/7, weekend tape, HIP-3 dex catalog, OI caps, funding, whale positions, trader track records, copy-trading leaderboard, vault screener, builder-code revenue, sports odds, liquidation map, 24h alert rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pulsenetwork](https://clawhub.ai/user/pulsenetwork)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to retrieve current Hyperliquid market, funding, trader, vault, builder-revenue, odds, liquidation, and alert data for market research and monitoring. Requests to paid endpoints require the user's explicit cost approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid requests can incur per-call charges.

Mitigation: Before making paid requests, disclose the endpoint price and approve the total cost; use a dedicated wallet with limited funds and spending caps.

Risk: Queries, wallet addresses, and alert callback URLs are shared with the provider.

Mitigation: Avoid sending sensitive query details or wallet addresses, and use callback URLs intended to be shared with the provider.

Risk: The optional payment client was not audited in the supplied security review.

Mitigation: Review the payment client before enabling or relying on it.

## Reference(s):

- [CryptoPulse API reference (OpenAPI)](https://cryptopulse.theaslangroupllc.com/openapi.json)
- [CryptoPulse LLM documentation](https://cryptopulse.theaslangroupllc.com/llms.txt)
- [ClawHub skill release](https://clawhub.ai/pulsenetwork/skills/hyperliquid-intel)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis]

**Output Format:** [Structured JSON market data with concise explanatory summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live, time-sensitive market data; paid per-call endpoints priced at $0.02–$0.25.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
