## Description:

Helps the agent use the one-wallet CLI to manage Ethereum/EVM wallets, send transactions, call contracts, and sign data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viyozc](https://clawhub.ai/user/viyozc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide agent-assisted Ethereum/EVM wallet operations through the one-wallet CLI, including wallet management, balance checks, transactions, contract calls, and signing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide irreversible blockchain transactions, token approvals, contract writes, wallet deletion, and signatures.

Mitigation: Require explicit user confirmation before any transaction, approval, contract write, wallet deletion, or signature.

Risk: Private keys, passwords, and wallet session details may be exposed if placed in commands, source files, or chat transcripts.

Mitigation: Use a dedicated least-privileged environment with test wallets or limited funds, keep secrets out of transcripts and repositories, and prefer environment-variable based secret handling.

Risk: Automation flags such as -y can bypass interactive confirmation for value-moving actions.

Mitigation: Avoid -y unless the recipient, amount, network, and action have been pre-approved.

Risk: Unpinned CLI installation may change behavior over time.

Mitigation: Pin the CLI version or commit where possible before using the skill in controlled workflows.

## Reference(s):

- [ClawHub one-wallet skill page](https://clawhub.ai/viyozc/skills/one-wallet)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend JSON output for automation and explicit confirmations for transaction or signing actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
