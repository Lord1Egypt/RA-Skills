## Description:

Query Hedera blockchain data via Mirror Node API for balances, token info, transactions, NFTs, account history, and network status without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to query public Hedera Mirror Node and SaucerSwap endpoints for account, token, transaction, NFT, supply, and market information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports hidden unrelated agent-registration and heartbeat endpoint metadata in a comment.

Mitigation: Remove the hidden onlyflies.buzz coordination metadata or document it plainly with explicit consent before installation.

Risk: Lookup commands can send account, token, transaction, or NFT identifiers to public Mirror Node and SaucerSwap endpoints.

Mitigation: Review whether sharing those blockchain identifiers with the public endpoints is acceptable before use.

## Reference(s):

- [Hedera REST API documentation](https://docs.hedera.com/hedera/sdks-and-apis/rest-api)
- [Hedera Mirror Node mainnet API](https://mainnet-public.mirrornode.hedera.com/api/v1)
- [Hedera Mirror Node testnet API](https://testnet.mirrornode.hedera.com/api/v1)
- [SaucerSwap token API](https://api.saucerswap.finance/tokens)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands query public REST endpoints and return endpoint JSON when executed.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
