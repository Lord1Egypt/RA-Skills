## Description:

Helps agents check sUSDC balances, deposit Linea USDC into yield-bearing sUSDC, and transfer funds with CLI scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marvinmarnold](https://clawhub.ai/user/marvinmarnold)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, agent operators, and crypto users use this skill to manage sUSDC balances, deposits, and transfers for a Linea wallet. It is intended for agent workflows that need idle USDC to earn yield while remaining transferable through the provided scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can approve, deposit, and transfer real wallet funds.

Mitigation: Use a dedicated low-balance wallet and require explicit human approval before any deposit or transfer.

Risk: Protocol, contract-address, and asset-conversion assumptions can affect whether funds remain spendable as expected.

Mitigation: Verify the Linea contract addresses and sUSDC transfer semantics before use.

Risk: The deposit flow may request unlimited USDC allowance for the router.

Mitigation: Avoid unlimited approvals when possible, or revoke allowances that are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marvinmarnold/skills/passive-savings-crypto)
- [Publisher Profile](https://clawhub.ai/user/marvinmarnold)
- [Project Homepage](https://github.com/locker-labs/passive-savings-crypto)
- [autoHODL](https://autohodl.money)
- [autoHODL Documentation](https://docs.autohodl.money)
- [Spendable Yield Tokens Reference](https://hackmd.io/@locker/autohodl-syts)
- [Aave](https://aave.com)
- [Linea](https://linea.build)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [CLI stdout and markdown instructions with command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, AGENT_PRIVATE_KEY, RPC_URL, and a Linea wallet funded with USDC.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
