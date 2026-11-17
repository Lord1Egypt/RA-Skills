## Description:

GoldRush Foundational API — REST API for historical and near-real-time blockchain data across 100+ chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gane5h](https://clawhub.ai/user/gane5h)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to select and call GoldRush Foundational API endpoints for wallet balances, transaction history, NFT holdings, token approvals, prices, cross-chain activity, block data, and portfolio tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example requests and integration guidance can expose GoldRush API keys if secrets are placed in URLs, prompts, logs, screenshots, or reusable shell commands.

Mitigation: Keep API keys in environment variables or a secret manager and prefer the SDK or Authorization header for authenticated requests.

Risk: Wallet identifiers, xPub/yPub/zPub values, token approvals, portfolio data, and transaction histories can reveal sensitive financial activity.

Mitigation: Use the skill only for intended GoldRush/Covalent queries and handle wallet-derived data as sensitive user information.

Risk: Mixed real-time or WebSocket guidance may be unsuitable for streaming workflows.

Mitigation: Use a dedicated streaming skill for WebSocket or real-time streaming work.

## Reference(s):

- [GoldRush Foundational API Skill Page](https://clawhub.ai/gane5h/skills/goldrush-foundational-api)
- [GoldRush Foundational API Overview](references/overview.md)
- [Balance Endpoints](references/endpoints-balances.md)
- [Transaction Endpoints](references/endpoints-transactions.md)
- [NFT, Security & Cross-Chain Endpoints](references/endpoints-nft-security-crosschain.md)
- [Utility Endpoints](references/endpoints-utility.md)
- [LLM Integration Guide](references/integration-guide.md)
- [Workflows & Decision Trees](references/workflows.md)
- [GoldRush Supported Chains](https://goldrush.dev/chains/)
- [GoldRush TypeScript Client SDK](https://www.npmjs.com/package/@covalenthq/client-sdk)
- [GoldRush API Documentation](https://goldrush.dev/docs/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include REST endpoint choices, SDK snippets, authentication guidance, pagination notes, and response-handling guidance.]

## Skill Version(s):

3.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
