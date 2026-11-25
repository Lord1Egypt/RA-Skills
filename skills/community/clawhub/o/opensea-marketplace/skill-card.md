## Description:

Buy and sell NFTs through OpenSea on EVM chains and Solana. Fulfill listings, accept or create offers, cancel orders, make cross-chain purchases, and sweep listings. Requires wallet signing; for read-only queries use opensea-api instead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opensea](https://clawhub.ai/user/opensea)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to create and manage NFT listings and offers, fulfill or cancel orders, and prepare supported cross-chain purchases and collection sweeps through OpenSea. It provides transaction steps for a configured wallet to sign after the user reviews and approves them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet transactions and token approvals can authorize or move assets.

Mitigation: Review the dry-run summary, recipients, fees, warnings, and approval amount; obtain user approval before signing or submitting. Use a standing unlimited approval only when the user explicitly agrees.

Risk: The security scan was partial, and its review flagged unpinned install commands.

Mitigation: Review the relevant scripts and dependencies, and use reviewed fixed package versions before installation.

## Reference(s):

- [Marketplace API reference](references/marketplace-api.md)
- [OpenSea developer documentation](https://docs.opensea.io/)
- [Wallet setup and signing policies](../opensea-wallet/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown guidance, shell commands, JSON request bodies, and transaction steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transaction details and approval steps for user review before signing or submission]

## Skill Version(s):

2.35.0 (source: package.json and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
