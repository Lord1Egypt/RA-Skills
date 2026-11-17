## Description:

Autonomously stake MOLT or V3 LP NFTs on Base to earn KELP rewards, auto-harvest for others, and receive 3.5% keeper fees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iam-rekt](https://clawhub.ai/user/iam-rekt)

### License/Terms of Use:


## Use Case:

External developers, DeFi operators, and agent builders use this skill to create wallet-driven scripts for Kelp Forest staking, harvesting, keeper operation, and migration on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to operate with live wallet keys.

Mitigation: Use a dedicated low-value wallet and prefer a hardware wallet or keystore instead of raw private keys.

Risk: The skill includes on-chain approval and staking actions that can expose user assets.

Mitigation: Independently verify every contract address and chain ID, approve only the exact amount needed, and revoke leftover allowances.

Risk: LP NFT staking transfers custody to a contract and carries real loss risk.

Mitigation: Treat LP NFT staking as a custody transfer, verify the receiving contract, and stake only assets the user is prepared to risk.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/iam-rekt/skills/kelp-forest)
- [Kelp Forest project site](https://kelpclaw.xyz)
- [Base RPC endpoint](https://mainnet.base.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet configuration, contract addresses, staking scripts, keeper-loop examples, and migration guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
