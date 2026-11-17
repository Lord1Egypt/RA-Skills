## Description:

Skill for interacting with Jovay or Ethereum network using jovay-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryogawan](https://clawhub.ai/user/ryogawan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and blockchain operators use this skill to ask an agent for Jovay CLI commands and guidance for wallet management, transfers, bridge operations, contract calls, transaction inspection, and network configuration on Jovay or Ethereum.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet secrets or encryption keys can expose funds if pasted into chat, shell history, scripts, or logs.

Mitigation: Use test wallets first, avoid sharing real private keys or wallet passwords with the agent, and prefer safer signing methods if jovay-cli supports them.

Risk: Incorrect blockchain transaction parameters can move funds, approve spenders, or broadcast transactions on the wrong network.

Mitigation: Verify every recipient, spender, contract, network, amount, value, and broadcast flag before running generated commands.

## Reference(s):

- [Jovay Network Information](https://docs.jovay.io/developer/network-information)
- [ClawHub Skill Page](https://clawhub.ai/ryogawan/skills/jovay-interaction)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Jovay CLI command options, Wei unit conversions, bridge sequence guidance, and transaction safety reminders.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
