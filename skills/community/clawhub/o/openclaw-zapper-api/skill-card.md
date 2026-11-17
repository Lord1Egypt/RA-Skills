## Description:

Query DeFi portfolios, token holdings, NFTs, transactions, and prices via Zapper API across 50+ chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zivhm](https://clawhub.ai/user/zivhm)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to inspect wallet balances, DeFi positions, NFT holdings, transaction history, claimable rewards, and token prices through Zapper's GraphQL API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured wallet addresses and query contents may be sent to Zapper, including all configured wallets when no explicit address or label is supplied.

Mitigation: Use explicit addresses or labels for each query and avoid storing unrelated pseudonymous wallets together in the same configuration.

Risk: The skill can read an API key from a local plaintext config file.

Mitigation: Prefer ZAPPER_API_KEY for credentials, and restrict permissions on ~/.config/zapper/addresses.json if a config file is used.

## Reference(s):

- [Zapper GraphQL API Reference](references/API.md)
- [Zapper API Documentation](https://build.zapper.xyz/docs/api/)
- [Zapper Developer Dashboard](https://zapper.xyz/developers)
- [Zapper](https://zapper.xyz)
- [ClawHub Skill Page](https://clawhub.ai/zivhm/skills/openclaw-zapper-api)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a ZAPPER_API_KEY for live API queries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
