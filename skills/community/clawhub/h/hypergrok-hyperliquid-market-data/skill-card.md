## Description:

Read live Hyperliquid market data from the desk computer with curl or the Python SDK - mid, mark and oracle prices, order book depth, funding (current, predicted, historical), open interest, volume, candles, perp and spot metadata, margin tiers, and how to save datasets for the strategy lab. Read-only, no key. Use for any market brief, depth read, funding question or data pull.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and market analysts use this skill to retrieve timestamped public Hyperliquid market data for market briefs, order-book depth and funding questions, and research datasets. It provides read-only data access and guidance for interpreting and reporting the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because some references in SKILL.md could not be resolved.

Mitigation: Review the unresolved references and confirm the market-data use fits the task before relying on related guidance.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/galleonlabs/skills/hypergrok-hyperliquid-market-data)
- [Hyperliquid mainnet API](https://api.hyperliquid.xyz)
- [Hyperliquid testnet API](https://api.hyperliquid-testnet.xyz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Code, JSON, CSV]

**Output Format:** [Markdown market summaries and guidance, with shell or Python examples and structured JSON or CSV data when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only market data; reported figures should include the request source, network, and UTC time.]

## Skill Version(s):

1.9.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
