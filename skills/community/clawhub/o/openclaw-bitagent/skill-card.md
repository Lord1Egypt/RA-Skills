## Description:

Launch, buy, and sell tokens on BitAgent bonding curves via CLI. Use when the user wants to create a new agent token, or trade existing agent tokens on BitAgent (BSC Testnet/Mainnet).

This skill is ready for commercial/non-commercial use.

## Publisher:

[parasyte-x](https://clawhub.ai/user/parasyte-x)

### License/Terms of Use:


## Use Case:

External developers and OpenClaw users use this skill to launch BitAgent tokens and buy or sell existing BitAgent tokens from an agent-run CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A raw wallet private key can authorize token launches and trades.

Mitigation: Use a dedicated low-balance wallet and keep the private key out of shared files, logs, and backups.

Risk: Mainnet launch, buy, and sell commands can submit irreversible transactions.

Mitigation: Prefer BSC Testnet first and require human confirmation before any mainnet launch or trade.

Risk: Runtime dependencies and remote BitAgent services influence transaction preparation and execution.

Mitigation: Pin and install local dependencies before use, then review CLI parameters and stdout before proceeding.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/parasyte-x/skills/openclaw-bitagent)
- [OpenClaw Project](https://github.com/openclaw/openclaw)
- [BitAgent App](https://app.bitagent.io)
- [BitAgent Testnet App](https://testnet.app.bitagent.io)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI stdout with Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PRIVATE_KEY and user-supplied network, token, amount, or launch parameters; commands may submit BSC Mainnet or Testnet transactions.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
