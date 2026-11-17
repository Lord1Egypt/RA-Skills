## Description:

Guides agents through Kite AI smart wallet workflows, including session keys, spending limits, deployed contracts, and network configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nihaovand](https://clawhub.ai/user/nihaovand)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to configure and reason about Kite AI smart wallets, session keys, spending limits, and delegated transaction flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet and session-key examples can authorize delegated transaction activity.

Mitigation: Use testnet or throwaway accounts first, apply spending limits, and revoke session keys that are no longer needed.

Risk: Incorrect or stale contract addresses and network settings can direct transactions to the wrong environment.

Mitigation: Verify contract addresses, chain IDs, RPC endpoints, and explorer links against trusted Kite AI sources before use.

## Reference(s):

- [Kite AI Docs](https://docs.gokite.ai)
- [Biconomy Nexus](https://docs.biconomy.io/new/learn-about-biconomy/nexus)
- [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337)
- [ERC-7579](https://eips.ethereum.org/EIPS/eip-7579)
- [ClawHub skill page](https://clawhub.ai/nihaovand/skills/kite-agent-wallet)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with JavaScript examples and network configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes smart contract addresses and Kite AI network endpoints that should be verified before wallet actions.]

## Skill Version(s):

1.0.0 (source: release metadata, skill.json, artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
