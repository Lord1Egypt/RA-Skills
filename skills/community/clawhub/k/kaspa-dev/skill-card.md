## Description:

A comprehensive Kaspa blockchain development toolkit for building transactions, integrating wallets, creating dApps and block explorers, operating nodes, and working with Kaspa SDKs and KRC20 tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codecustard](https://clawhub.ai/user/codecustard)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to generate Kaspa development guidance, code examples, scripts, and configuration for wallet, transaction, dApp, block explorer, node, SDK, and KRC20 token work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet examples and utilities can print or save private keys or mnemonics in plaintext.

Mitigation: Use testnet or devnet first, remove plaintext secret output, and use secure key storage or hardware-backed signing before handling real funds.

Risk: The Python transaction builder and signing flow are not suitable as-is for production transaction submission.

Mitigation: Use reviewed official SDK signing flows, inspect generated transactions, and test submission behavior away from mainnet before production use.

Risk: Dependency, binary, container, and node RPC guidance can expose systems if packages are unpinned or RPC is reachable remotely without strong controls.

Mitigation: Pin and verify packages, images, and binaries, and bind RPC to localhost unless authenticated remote-access controls are explicitly configured.

## Reference(s):

- [Kaspa Developer Platform API Reference](references/api-reference.md)
- [Kaspa Go SDK](references/kaspa-go-sdk.md)
- [Kaspa Python SDK](references/kaspa-python-sdk.md)
- [Kaspa Rust SDK](references/kaspa-rust-sdk.md)
- [Kaspa WASM SDK](references/kaspa-wasm-sdk.md)
- [KRC20 Token Standard](references/krc20-tokens.md)
- [Kaspa Node Operations Guide](references/node-operations.md)
- [Kaspa Wallet Integration Guide](references/wallet-integration.md)
- [Kaspa Documentation](https://docs.kas.fyi/)
- [Kaspa Developer Platform](https://kas.fyi/)
- [Kaspa API Endpoint](https://api.kaspa.org)
- [Kaspa Motoko Package](https://mops.one/kaspa)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include runnable scripts or command examples; review before execution or use with real funds.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
