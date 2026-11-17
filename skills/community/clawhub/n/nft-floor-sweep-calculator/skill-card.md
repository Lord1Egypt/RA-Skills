## Description:

Calculates estimated NFT floor sweep costs for Solana or EVM collections by fetching live floor prices from Magic Eden or CoinGecko and applying configurable marketplace fee and slippage assumptions.

This skill is for research and development only.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External users, NFT traders, developers, and agent operators use this skill to estimate the cost of sweeping a specified number of NFTs from a collection floor before manually checking live order books or placing trades. It is intended for planning and research, not wallet management or trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Collection slugs or NFT identifiers queried by the user are sent to Magic Eden or CoinGecko public APIs.

Mitigation: Review queried collection identifiers before running the calculator, and avoid submitting sensitive or private portfolio research where external API disclosure is a concern.

Risk: The calculated total is an estimate, not a trade quote, because free public APIs do not provide full live order-book depth and royalties are not included.

Mitigation: Check the live marketplace order book and applicable royalties before using the estimate to make a buying decision.

Risk: Public API availability, latency, or stale floor data can make outputs incomplete or misleading.

Mitigation: Treat errors or unexpected values as a signal to retry later or verify directly on the source marketplace before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/nft-floor-sweep-calculator)
- [Magic Eden collection stats endpoint](https://api-mainnet.magiceden.dev/v2/collections/{slug}/stats)
- [CoinGecko NFT endpoint](https://api.coingecko.com/api/v3/nfts/{nft_id})
- [CoinGecko NFT list endpoint](https://api.coingecko.com/api/v3/nfts/list)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; the calculator script emits plain text reports or JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes estimated per-item prices, subtotal, marketplace fee, total cost, and average price per item; results depend on public API responses and user-provided slippage and fee assumptions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
