## Description:

A standalone CLI wallet for the Kaspa blockchain that lets agents check balances, send KAS payments, estimate fees, generate wallet mnemonics, and build payment URIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manyfestation](https://clawhub.ai/user/manyfestation)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent operate a Kaspa CLI wallet for balance checks, fee estimates, wallet generation, payment URI generation, and KAS transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real cryptocurrency transfers and spend wallet funds.

Mitigation: Use testnet or small balances first, and require a confirmation or dry-run workflow before allowing mainnet sends.

Risk: Wallet private keys or mnemonics may be exposed if broad agent sessions can read environment variables.

Mitigation: Limit credential scope to trusted sessions, avoid logging secrets, and remove wallet credentials when the task is complete.

Risk: Installation pulls the unpinned kaspa dependency before use.

Mitigation: Pin and review dependencies in a controlled environment before granting the skill wallet-spending capability.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manyfestation/skills/kaspa-wallet)
- [Kaspa mainnet explorer](https://explorer.kaspa.org/txs/{txid})
- [Kaspa testnet explorer](https://explorer-tn10.kaspa.org/txs/{txid})

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON command responses with shell command usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Wallet actions require KASPA_PRIVATE_KEY or KASPA_MNEMONIC; network defaults to mainnet unless configured otherwise.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
