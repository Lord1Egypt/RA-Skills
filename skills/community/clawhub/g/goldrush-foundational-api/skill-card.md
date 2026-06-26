## Description: <br>
GoldRush Foundational API helps agents produce REST API guidance, SDK examples, endpoint choices, and request patterns for historical and near-real-time blockchain data across balances, transactions, NFTs, security approvals, cross-chain activity, pricing, and block data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gane5h](https://clawhub.ai/user/gane5h) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and agent builders use this skill to select GoldRush Foundational API endpoints and generate implementation guidance for wallet balances, transaction history, NFT holdings, approvals, portfolio tracking, block explorers, compliance checks, and other on-chain data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route selected wallet addresses, domains, token contracts, and potentially xpub-style identifiers to GoldRush/Covalent. <br>
Mitigation: Direct the agent to query only the specific addresses and endpoints needed, and avoid using the skill for data the user does not want sent to the external service. <br>
Risk: GoldRush API keys may be exposed if placed in URLs, prompts, logs, or other conversation-visible content. <br>
Mitigation: Use a restricted API key from secure configuration, pass it through Authorization headers, and avoid including secrets in URLs or user-visible prompts. <br>


## Reference(s): <br>
- [GoldRush Foundational API Overview](references/overview.md) <br>
- [Balance Endpoints](references/endpoints-balances.md) <br>
- [Transaction Endpoints](references/endpoints-transactions.md) <br>
- [NFT, Security & Cross-Chain Endpoints](references/endpoints-nft-security-crosschain.md) <br>
- [Utility Endpoints](references/endpoints-utility.md) <br>
- [LLM Integration Guide](references/integration-guide.md) <br>
- [Workflows & Decision Trees](references/workflows.md) <br>
- [GoldRush TypeScript Client SDK](https://www.npmjs.com/package/@covalenthq/client-sdk) <br>
- [GoldRush API Documentation](https://goldrush.dev/docs/) <br>
- [GoldRush API Reference](https://goldrush.dev/docs/api-reference/) <br>
- [Supported Chains](https://goldrush.dev/chains/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline TypeScript, curl, JSON, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference wallet addresses, domains, token contracts, chain names, pagination settings, quote currencies, and GoldRush API authentication headers supplied by the user.] <br>

## Skill Version(s): <br>
3.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
