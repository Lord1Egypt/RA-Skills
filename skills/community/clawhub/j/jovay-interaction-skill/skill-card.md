## Description:

Skill for interacting with Jovay or Ethereum network using jovay-cli

This skill is ready for commercial/non-commercial use.

## Publisher:

[jovay-developer](https://clawhub.ai/user/jovay-developer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Jovay CLI commands for wallet setup, balance checks, transfers, bridge operations, contract calls, transaction inspection, and network configuration across Jovay and Ethereum.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys or encryption passwords could be exposed through chat transcripts or shell history.

Mitigation: Do not paste real wallet secrets into an AI chat or shell command history; prefer test wallets, hardware wallets, or external signing.

Risk: Blockchain transfers, approvals, bridge actions, and contract writes can be irreversible when sent with --broadcast.

Mitigation: Verify every recipient, spender, amount, network, contract address, and method before broadcasting a transaction.

Risk: Installing an unpinned CLI package can introduce supply-chain uncertainty.

Mitigation: Pin and verify the jovay CLI package where possible before use.

## Reference(s):

- [Jovay Network Information](https://docs.jovay.io/developer/network-information)
- [ClawHub Skill Page](https://clawhub.ai/jovay-developer/skills/jovay-interaction-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may include transaction broadcast flags and wallet configuration options that require user review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
