## Description:

Use when the user asks about funding rates, open interest, volume or price of US stock, index or commodity perpetuals on Hyperliquid (HIP-3 xyz market, e.g. xyz:NVDA, xyz:TSLA, xyz:SP500), or which stock perps are most active. Free, no-auth live data from Hyperliquid's public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a0971025732-netizen](https://clawhub.ai/user/a0971025732-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing Hyperliquid HIP-3 stock, index, and commodity perpetuals can retrieve current mark prices, 24-hour changes and volume, open interest, and funding rates for selected tickers or the most active markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker symbols or a result limit are sent to Finch to retrieve market data.

Mitigation: Use the skill only if you are comfortable sharing those queries.

Risk: The optional Maneki AI analysis offered through Finch may be paid.

Mitigation: Check the displayed price and obtain user approval before starting paid analysis.

Risk: Market data could be mistaken for investment advice.

Mitigation: Treat the results as data only; do not use this skill to place trades or request wallet credentials.

## Reference(s):


## Skill Output:

**Output Type(s):** [Market data, JSON]

**Output Format:** [Structured market data in JSON, including prices, 24-hour changes, volume, open interest, funding rates, leverage, and missing tickers when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ticker symbols or a result limit; data only, not investment advice.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
