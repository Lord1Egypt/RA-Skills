## Description: <br>
ERC-8004 agent identity management. Register AI agents on-chain, update reputation scores, query the validation registry, and manage attestations for autonomous DeFi and governance participation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x-wzw](https://clawhub.ai/user/0x-wzw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare ERC-8004 agent identity operations, including on-chain registration, validation lookups, reputation updates, and attestations for DeFi and governance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web3 write operations can spend gas or modify live registry state if run against the wrong chain or contract. <br>
Mitigation: Verify the registry contract and chain before any cast send, and test on a testnet before mainnet use. <br>
Risk: Private keys used for wallet, validator, or attester operations can be exposed through shared shells, logs, or unsafe command handling. <br>
Mitigation: Use a dedicated low-value wallet and avoid pasting production private keys into shared shells or logs. <br>
Risk: Remote installer commands and Ethereum-style tooling can introduce local environment risk. <br>
Mitigation: Review remote installer commands before executing them and install only if comfortable with Ethereum-style tooling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0x-wzw/ox-agent-identity) <br>
- [ERC-8004 Draft](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [Ethereum Magicians Forum](https://ethereum-magicians.org/t/erc-8004-agent-identity-standard/) <br>
- [Foundry Book](https://book.getfoundry.sh/) <br>
- [Repository declared in artifact metadata](https://github.com/0x-wzw/agent-identity) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment-variable examples and cast commands for read and write blockchain operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
