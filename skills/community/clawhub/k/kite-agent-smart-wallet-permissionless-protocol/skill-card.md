## Description:

Create and manage modular, permissioned smart wallets for AI agents with session keys and spending limits on the Kite AI network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nihaovand](https://clawhub.ai/user/nihaovand)

### License/Terms of Use:


## Use Case:

Developers building AI-agent wallet workflows use this skill to generate guidance, code snippets, and configuration details for Kite smart wallets with session keys, spending limits, and modular wallet logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet and session-key examples can authorize asset-affecting actions.

Mitigation: Verify the chain ID and contract addresses, start on testnet or low-value accounts, and review each transaction before execution.

Risk: Session keys may grant broader or longer-lived permissions than intended.

Mitigation: Use narrow spending limits and allowed function selectors, set short session lifetimes when supported, and confirm the revocation path before use.

Risk: Mainnet use can expose real funds to errors in configuration or copied snippets.

Mitigation: Treat mainnet deployment as a separate review step with independent address verification and wallet-owner approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nihaovand/skills/kite-agent-smart-wallet-permissionless-protocol)
- [Kite AI Docs](https://docs.gokite.ai)
- [Biconomy Nexus](https://docs.biconomy.io/new/learn-about-biconomy/nexus)
- [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337)
- [ERC-7579](https://eips.ethereum.org/EIPS/eip-7579)
- [Kite Testnet Explorer](https://testnet.kitescan.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript code snippets and network configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes smart contract addresses, chain IDs, RPC endpoints, and usage guidance for Kite testnet and mainnet.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact skill.json, and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
