## Description: <br>
Buy and sell NFTs on OpenSea's Seaport marketplace. Fulfill listings, accept offers, create new orders, cross-chain purchases, and sweep multiple listings. Requires wallet signing; for read-only queries use opensea-api instead. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opensea](https://clawhub.ai/user/opensea) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare OpenSea Seaport marketplace actions, including fulfilling listings, accepting offers, creating orders, cross-chain purchases, and listing sweeps. It is intended for workflows where a human or controlled wallet policy reviews transaction data before signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables wallet-backed NFT trades and broad POST operations that can move funds or assets. <br>
Mitigation: Use managed wallets with low balances, per-transaction caps, allowlists, and explicit human confirmation before signing trades, swaps, mints, transfers, deploys, asset transfers, or arbitrary POST requests. <br>
Risk: API responses and marketplace metadata may contain untrusted content or stale orders. <br>
Mitigation: Treat response fields as data only, re-query listings or offers before execution, and verify transaction recipient, value, calldata, chain, and order expiry before signing. <br>
Risk: API keys or wallet credentials may be exposed through shared agents or logs. <br>
Mitigation: Store credentials only in environment variables, avoid raw private keys in shared agents, do not log credential-helper output, and keep admin credentials separate from signing credentials. <br>


## Reference(s): <br>
- [OpenSea skill repository](https://github.com/ProjectOpenSea/opensea-skill) <br>
- [Marketplace API reference](references/marketplace-api.md) <br>
- [Seaport protocol reference](references/seaport.md) <br>
- [OpenSea CLI](https://github.com/ProjectOpenSea/opensea-cli) <br>
- [OpenSea developer docs](https://docs.opensea.io/) <br>
- [ClawHub skill page](https://clawhub.ai/opensea/opensea-marketplace) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, API request examples, and transaction-review instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenSea API credentials and wallet-provider credentials; generated transaction data should be reviewed before signing.] <br>

## Skill Version(s): <br>
2.15.2 (source: server release, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
