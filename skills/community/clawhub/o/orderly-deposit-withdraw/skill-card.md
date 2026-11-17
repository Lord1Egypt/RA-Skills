## Description:

Handle token deposits and withdrawals across chains, including allowance approval, vault interactions, and cross-chain operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarnadas](https://clawhub.ai/user/tarnadas)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement Orderly Network deposit, withdrawal, internal transfer, and cross-chain asset movement flows for EVM and Solana wallets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A deposit example uses persistent unlimited ERC-20 token-spending approval.

Mitigation: Prefer exact-amount approvals, verify the vault contract address from trusted Orderly sources, and revoke unused allowances after deposits.

Risk: Incorrect contract addresses, destination addresses, or chain IDs can misdirect funds or cause failed transactions.

Mitigation: Confirm chain ID, verifying contract, vault address, token address, and destination address before signing or submitting asset movement requests.

Risk: The examples can affect real funds when adapted directly in production.

Mitigation: Review the workflow carefully, test on supported testnets first, and require user confirmation before executing wallet signatures or transactions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tarnadas/skills/orderly-deposit-withdraw)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript, JSON, REST endpoint, and shell-style command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes blockchain transaction and API signing guidance for wallet-connected asset operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
