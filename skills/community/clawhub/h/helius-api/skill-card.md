## Description: <br>
Query Solana wallet balances, token holdings, NFT holdings, transaction history, transfer activity, identity labels, funding sources, and parsed transaction details through the Helius API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsahedge](https://clawhub.ai/user/itsahedge) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to answer Solana wallet and transaction questions by calling documented Helius REST endpoints and interpreting JSON responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Helius API key, and requests may consume API credits. <br>
Mitigation: Use a limited or easily rotated Helius API key and monitor account usage. <br>
Risk: Wallet addresses and transaction queries are sent to Helius and may be associated with the user's Helius account. <br>
Mitigation: Avoid querying wallets or transactions that should not be linked to the account, and prefer header-based authentication over URL query strings. <br>
Risk: The skill depends on third-party Helius endpoint availability and response behavior. <br>
Mitigation: Handle API errors, pagination, 404 responses, and unsupported networks explicitly before relying on returned data. <br>


## Reference(s): <br>
- [Helius API Skill Page](https://clawhub.ai/itsahedge/helius-api) <br>
- [Helius Docs](https://www.helius.dev/docs) <br>
- [Wallet API Overview](https://www.helius.dev/docs/wallet-api/overview) <br>
- [Enhanced Transactions Overview](https://www.helius.dev/docs/enhanced-transactions/overview) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Balances Endpoint](references/balances.md) <br>
- [History Endpoint](references/history.md) <br>
- [Transfers Endpoint](references/transfers.md) <br>
- [Identity Endpoint](references/identity.md) <br>
- [Funded By Endpoint](references/funded-by.md) <br>
- [Enhanced Transactions API](references/enhanced-transactions.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, code examples, and JSON API response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HELIUS_API_KEY and returns read-only Solana data from third-party Helius endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
