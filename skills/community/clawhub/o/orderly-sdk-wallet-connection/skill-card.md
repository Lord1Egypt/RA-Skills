## Description:

Comprehensive guide to integrating wallet connection in Orderly Network DEX applications, supporting both EVM (Ethereum, Arbitrum, etc.) and Solana wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarnadas](https://clawhub.ai/user/tarnadas)

### License/Terms of Use:


## Use Case:

Developers building Orderly Network DEX applications use this skill to add wallet connection, multi-chain wallet support, chain switching, authentication state handling, and related UI integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet connection and social login can share wallet addresses, chain/account metadata, and authentication details with wallet or identity providers.

Mitigation: Clearly tell users what wallet or identity providers receive before connection or login, and review package and provider settings before release.

Risk: Account setup, chain switching, and trading-enablement flows can affect user accounts if triggered without clear consent.

Mitigation: Keep wallet, account, chain-switching, account creation, and trading-enablement actions behind explicit user confirmation and clear UI state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tarnadas/skills/orderly-sdk-wallet-connection)
- [Publisher profile](https://clawhub.ai/user/tarnadas)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript/TSX and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes package installation commands, provider configuration examples, wallet state usage patterns, chain switching guidance, and best practices.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
