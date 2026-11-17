## Description:

Query Web3 blockchain data from the Moralis API for wallets, tokens, NFTs, DeFi positions, entity labels, blocks, and transactions across EVM chains and Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[novnski](https://clawhub.ai/user/novnski)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to plan and execute Moralis Web3 Data API lookups, including wallet balances, token prices and metadata, NFT data, DeFi positions, entity labels, blocks, and transactions. It is useful when the user needs structured blockchain data retrieval guidance or curl-based API calls for EVM chains and Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MORALIS_API_KEY could be exposed through chat, logs, shell history, or checked-in environment files.

Mitigation: Store the key outside chat, avoid printing it, keep any .env file out of version control, and review shell commands before execution.

Risk: Wallet history, portfolio, profitability, and net-worth lookups can reveal sensitive financial intelligence.

Mitigation: Use the skill only for intended Moralis lookups and confirm that wallet addresses or account data are appropriate to query before sending requests.

Risk: The reSyncMetadata endpoint can update or resync external NFT metadata state rather than only read data.

Mitigation: Require explicit user confirmation before using reSyncMetadata and prefer read-only endpoints when the user only asks for data retrieval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/novnski/skills/moralis-data-api)
- [Moralis Documentation](https://docs.moralis.com)
- [Repository Metadata](https://github.com/MoralisWeb3/onchain-skills)
- [Supported APIs and Chains](references/SupportedApisAndChains.md)
- [Response Patterns](references/ResponsePatterns.md)
- [Pagination](references/Pagination.md)
- [Common Pitfalls](references/CommonPitfalls.md)
- [Performance and Latency](references/PerformanceAndLatency.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline curl commands, code snippets, and JSON response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and MORALIS_API_KEY; outputs should account for EVM and Solana endpoint differences and non-streaming API behavior.]

## Skill Version(s):

1.3.2 (source: server release metadata; artifact frontmatter is 1.3.1 with no file changes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
