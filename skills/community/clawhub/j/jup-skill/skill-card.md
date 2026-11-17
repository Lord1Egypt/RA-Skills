## Description:

Execute Jupiter API operations on Solana, including fetching quotes, signing transactions, executing swaps, prediction markets, DCA, limit orders, lending, and Jupiter integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifeofpavs](https://clawhub.ai/user/lifeofpavs)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to work with Jupiter API workflows on Solana, including token swaps, transaction signing and submission, portfolio queries, DCA, limit orders, lending, and prediction market operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign and broadcast opaque Solana transactions, which can cause financial loss if the transaction source or contents are untrusted.

Mitigation: Review every transaction outside the skill before signing, use a dedicated low-balance wallet, and avoid signing or broadcasting opaque base64 transactions from untrusted or unverified responses.

Risk: The Jupiter API key could be exposed if API calls are directed outside trusted Jupiter endpoints.

Mitigation: Restrict endpoints to known Jupiter paths and avoid passing API keys directly on the command line.

Risk: Wallet JSON files contain private key material.

Mitigation: Use a dedicated low-balance wallet, prefer ephemeral keys for testing, and use hardware signing where available.

## Reference(s):

- [Jupiter API Base URL](https://api.jup.ag)
- [Jupiter Portal](https://portal.jup.ag)
- [Jupiter Documentation](https://dev.jup.ag)
- [Jupiter Ultra Documentation](https://dev.jup.ag/docs/ultra/index.md)
- [Jupiter Swap Documentation](https://dev.jup.ag/docs/swap/index.md)
- [Jupiter Status Page](https://status.jup.ag)
- [Solscan](https://solscan.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON API examples, and TypeScript script usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Jupiter API key and a local Solana wallet JSON file for transaction signing.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
