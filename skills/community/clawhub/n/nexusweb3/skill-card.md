## Description:

Complete financial infrastructure for AI agents on Base mainnet, covering wallet, identity, payments, yield, insurance, reputation, marketplace, bridge, governance, and launchpad workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexusweb3dev](https://clawhub.ai/user/nexusweb3dev)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to configure an AI agent for Base mainnet wallet, identity, payment, escrow, yield, insurance, reputation, marketplace, bridge, governance, and launchpad interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent live Base mainnet financial authority through wallet or operator credentials.

Mitigation: Use only a dedicated low-balance wallet or tightly limited operator key, never a primary wallet key.

Risk: Transaction examples can result in real approvals, transfers, fees, escrow actions, bridge registrations, governance votes, or protocol launches.

Mitigation: Require explicit confirmation for every mainnet transaction, approval, recipient, amount, contract, and fee before execution.

Risk: A leaked operator key can spend up to its configured allowance.

Mitigation: Configure narrow spending limits, fund the vault minimally, and rotate or revoke operator access if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nexusweb3dev/skills/nexusweb3)
- [nexusweb3dev publisher profile](https://clawhub.ai/user/nexusweb3dev)
- [BaseScan AgentVaultFactory contract](https://basescan.org/address/0x1F28579F8C2dffde8746169116bb3a4d9E516f5A)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Solidity transaction examples and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an ETH_OPERATOR_KEY environment variable and Base mainnet ETH and USDC for protocol interactions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
