## Description:

ERC-8004 agent identity management. Register AI agents on-chain, update reputation scores, query the validation registry, and manage attestations for autonomous DeFi and governance participation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-wzw](https://clawhub.ai/user/0x-wzw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage ERC-8004 agent identities for DeFi and governance workflows, including registration, reputation checks, validator updates, and attestations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes live on-chain write commands that can spend gas or modify registry, reputation, and attestation state.

Mitigation: Test on Sepolia, Holesky, or another low-value environment before mainnet use, and verify the target chain and registry address before every write.

Risk: The skill shows private keys passed through environment variables and command arguments.

Mitigation: Use low-value dedicated wallets, avoid production private keys, and prefer encrypted keystores, hardware wallets, or signing services.

Risk: The installation guidance includes piping a remote Foundry installer script into a shell.

Mitigation: Install Foundry from reviewed official instructions and inspect installer steps before execution.

## Reference(s):

- [Ox Agent Identity on ClawHub](https://clawhub.ai/0x-wzw/skills/ox-agent-identity)
- [ERC-8004 Draft](https://eips.ethereum.org/EIPS/eip-8004)
- [Ethereum Magicians Forum](https://ethereum-magicians.org/t/erc-8004-agent-identity-standard/)
- [Foundry Book](https://book.getfoundry.sh/)
- [Foundry Installation](https://book.getfoundry.sh/getting-started/installation)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured RPC URL, wallet, ERC-8004 registry address, and Foundry cast for blockchain reads and writes.]

## Skill Version(s):

1.0.0 (source: release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
