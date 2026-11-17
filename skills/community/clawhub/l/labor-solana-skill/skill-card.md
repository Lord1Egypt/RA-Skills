## Description:

Transfers native SOL on Solana to a recipient address using a funded signing key from environment configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xxbrain01](https://clawhub.ai/user/0xxbrain01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to prepare and execute native SOL transfers on Solana devnet, mainnet-beta, or a custom RPC endpoint after validating the recipient, amount, and network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make irreversible SOL transfers with a funded signing key.

Mitigation: Use a dedicated low-balance wallet, test on devnet first, and require explicit user confirmation before any mainnet transfer.

Risk: The confirmed network may not be bound to the RPC endpoint used at execution.

Mitigation: Fail closed unless the selected network matches the connected cluster, and independently verify the exact RPC endpoint and recipient before sending funds.

Risk: A private key exposed in chat or logs can compromise the wallet.

Mitigation: Keep SOLANA_PRIVATE_KEY in environment configuration or workspace secrets, and do not print, paste, or log it.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/0xxbrain01/skills/labor-solana-skill)
- [OpenClaw skill documentation](https://docs.openclaw.ai/tools/creating-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON transfer results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful transfer runs report signature, explorer URL, source wallet, recipient, amount, cluster, and RPC URL.]

## Skill Version(s):

1.0.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
