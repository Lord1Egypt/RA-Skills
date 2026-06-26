## Description: <br>
Query Web3 blockchain data from the Moralis API for wallet balances, tokens, NFTs, transactions, token analytics, DeFi positions, entity labels, blocks, and transactions across EVM chains and Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[novnski](https://clawhub.ai/user/novnski) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to have an agent look up Moralis Web3 Data API endpoints, construct curl-based requests, and interpret wallet, token, NFT, DeFi, block, and transaction responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent use can send queried wallet addresses, contract addresses, token or NFT identifiers, timing, and API-key-authenticated requests to Moralis. <br>
Mitigation: Use the skill only when the user requests Moralis-backed blockchain lookup and avoid sending sensitive wallet or token queries unless they are needed for the task. <br>
Risk: MORALIS_API_KEY can be exposed if copied into chat, committed, or logged with request commands. <br>
Mitigation: Store MORALIS_API_KEY in an environment variable or secret store, keep any .env file out of version control, and redact the key from logs and examples. <br>
Risk: The NFT metadata resync endpoint can change Moralis cached metadata. <br>
Mitigation: Require an explicit user request before using metadata resync and explain that it updates cached metadata behavior before running the request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/novnski/moralis-data-api) <br>
- [Moralis documentation](https://docs.moralis.com) <br>
- [Declared source repository](https://github.com/MoralisWeb3/onchain-skills) <br>
- [Supported APIs and Chains](references/SupportedApisAndChains.md) <br>
- [Response Patterns](references/ResponsePatterns.md) <br>
- [Pagination](references/Pagination.md) <br>
- [Common Pitfalls](references/CommonPitfalls.md) <br>
- [Performance and Latency](references/PerformanceAndLatency.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl commands that require MORALIS_API_KEY and may return JSON from Moralis API endpoints.] <br>

## Skill Version(s): <br>
1.3.2 (source: ClawHub release metadata; artifact frontmatter says 1.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
