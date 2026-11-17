## Description:

Manage Stellar wallets, send XLM payments, configure networks, and interact with Soroban smart contracts via the Stellar CLI on testnet or mainnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sixela33](https://clawhub.ai/user/sixela33)

### License/Terms of Use:


## Use Case:

Developers and blockchain operators use this skill to manage Stellar CLI identities, configure Stellar networks, submit XLM payments, and work with Soroban contracts from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install Stellar CLI from listed external sources, including mutable remote release or installer locations.

Mitigation: Review the selected installer source before use and prefer package-manager or pinned source installation when possible.

Risk: The skill can automatically create, fund, and select a default Stellar testnet wallet and change Stellar CLI testnet configuration.

Mitigation: Manually approve first-run wallet creation when feasible, avoid using a valuable existing identity as the default, and back up secret keys securely.

Risk: Mainnet actions can involve real funds and irreversible key or payment operations.

Mitigation: Require explicit confirmation before mainnet use, verify destination addresses and amounts, and be cautious before deleting keys or exposing secret keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sixela33/skills/open-stellar)
- [Stellar CLI documentation](https://developers.stellar.org/docs/tools/developer-tools/cli)
- [Stellar CLI crate](https://crates.io/crates/stellar-cli)
- [Stellar CLI releases](https://github.com/stellar/stellar-cli/releases/latest)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Stellar CLI commands for wallet, network, payment, and smart contract workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
