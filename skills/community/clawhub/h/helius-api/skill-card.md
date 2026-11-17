## Description:

Query Solana wallet, transaction, transfer, identity, funding, token, and NFT data through Helius Wallet API and Enhanced Transactions endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsahedge](https://clawhub.ai/user/itsahedge)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to query Solana on-chain data with Helius, including wallet balances, transaction history, token transfers, known wallet identities, funding sources, and parsed transaction details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses and transaction signatures submitted through this skill are sent to Helius.

Mitigation: Use the skill only with wallet addresses and transaction signatures that are appropriate to share with Helius.

Risk: API keys placed in request URLs can be exposed through logs, shell history, browser history, or copied examples.

Mitigation: Prefer the X-Api-Key header, use scoped Helius API keys where possible, and avoid logging full request URLs containing credentials.

## Reference(s):

- [Balances Endpoint](references/balances.md)
- [History Endpoint](references/history.md)
- [Transfers Endpoint](references/transfers.md)
- [Identity Endpoint](references/identity.md)
- [Funded By Endpoint](references/funded-by.md)
- [Enhanced Transactions API](references/enhanced-transactions.md)
- [Helius Docs](https://www.helius.dev/docs)
- [Wallet API Overview](https://www.helius.dev/docs/wallet-api/overview)
- [Enhanced Transactions Overview](https://www.helius.dev/docs/enhanced-transactions/overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with JSON examples and inline shell or JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helius endpoint responses are JSON; use requires a Helius API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
