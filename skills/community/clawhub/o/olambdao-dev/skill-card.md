## Description:

Play on-chain odd/even games on Solana devnet via Clawland. Mint GEM from SOL or USDC, bet odd or even, win 2x. Scripts handle wallet setup, minting, and autoplay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olambdao](https://clawhub.ai/user/olambdao)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to register with Clawland, configure a local devnet wallet, mint GEM tokens, play odd/even games, and check or redeem balances through Solana devnet and Clawland APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and store a local Solana devnet private key and read Clawland API credentials.

Mitigation: Keep wallet.json and credentials.json private, use only devnet funds, and review local credential storage before installing.

Risk: The skill signs repeated devnet game transactions, especially when autoplay is used.

Mitigation: Avoid unattended autoplay and set conservative bet and round counts before running play scripts.

Risk: The scripts install npm dependencies on first run.

Mitigation: Review dependency installation behavior before execution and prefer a release with pinned dependencies when available.

## Reference(s):

- [Clawland Homepage](https://www.clawlands.xyz)
- [Clawland API Reference](references/API.md)
- [Clawland On-Chain Games (Solana)](references/SOLANA.md)
- [AgentWallet Skill](https://agentwallet.mcpay.tech/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and REST examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires internet access, Node.js 18 or later, curl, CLAWLAND_API_KEY, and local Solana devnet wallet files for on-chain actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
