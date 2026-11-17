## Description:

HumanNFT helps agents browse, mint, buy, sell, transfer, and manage human NFTs on the HumanNFT marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesmartape](https://clawhub.ai/user/thesmartape)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to interact with the HumanNFT marketplace on Base mainnet, including browsing humans, minting NFTs, managing portfolios, and preparing marketplace transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support real-money NFT transactions with wallet-enabled authority on Base mainnet.

Mitigation: Use a dedicated low-balance wallet and require explicit approval for every signature and transaction.

Risk: An agent may receive transaction objects for marketplace or minting actions that spend funds or move NFTs.

Mitigation: Verify transaction recipient, chain ID, value, token ID, and calldata before signing or broadcasting.

Risk: The MCP package is referenced without a pinned version.

Mitigation: Pin and inspect the MCP package version before running it.

## Reference(s):

- [HumanNFT skill page](https://clawhub.ai/thesmartape/skills/humannft)
- [HumanNFT website](https://humannft.ai)
- [HumanNFT API](https://humannft.ai/api)
- [Publisher profile](https://clawhub.ai/user/thesmartape)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code, API calls]

**Output Format:** [Markdown with inline code blocks and API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HUMANNFT_API_KEY for authenticated marketplace, portfolio, webhook, and sync actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
