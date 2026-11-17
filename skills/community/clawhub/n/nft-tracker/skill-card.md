## Description:

Track NFT collection prices, floor prices, and sales data. Supports Ethereum collections including BAYC, MAYC, CryptoPunks, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianalloway](https://clawhub.ai/user/ianalloway)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and NFT users use the skill to query OpenSea for collection statistics, metadata, recent sales, and individual token details, and to create a one-shot floor-price alert example.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OpenSea API key is required for most endpoints and could be exposed if handled carelessly.

Mitigation: Supply OPENSEA_API_KEY through secure secret storage and avoid printing or sharing its value.

Risk: The price-alert example's response fields and currency units were not runtime-tested, and the example runs only once.

Mitigation: Verify the returned floor-price field and units before relying on alerts; install bc for the example and configure separate scheduling for continuous monitoring.

## Reference(s):

- [OpenSea API overview](https://docs.opensea.io/reference/api-overview)
- [OpenSea API keys](https://docs.opensea.io/reference/api-keys)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline curl commands and jq filters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned fields depend on the selected OpenSea endpoint.]

## Skill Version(s):

0.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
