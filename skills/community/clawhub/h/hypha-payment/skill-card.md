## Description:

P2P agent coordination and USDT settlement via the Hypha Network for mesh discovery, hiring, service payments, direct USDT transfers on Base L2, balance checks, and network participation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pointsnode](https://clawhub.ai/user/pointsnode)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to connect agents to the Hypha P2P mesh, discover peers, announce services, and coordinate USDT payments or escrow-based hiring on Base L2.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle wallet seed material and payment credentials.

Mitigation: Do not use a real funded wallet seed with the setup script, avoid placing seeds on the command line or in logs, and keep private keys out of shared agent transcripts.

Risk: The skill includes examples for USDT payments, escrow creation, and mainnet-capable transactions.

Mitigation: Test only on Base Sepolia unless production use has been explicitly approved, and require human approval before any USDT payment, escrow creation, or mainnet transaction.

Risk: The skill depends on the external hypha-sdk package and network endpoints.

Mitigation: Pin and review hypha-sdk before use, and confirm RPC endpoints and contract addresses against trusted operational sources.

## Reference(s):

- [Hypha Network Reference](references/network.md)
- [hypha-sdk on PyPI](https://pypi.org/project/hypha-sdk/)
- [Hypha Network Source](https://github.com/Pointsnode/hypha-network)
- [Base Mainnet RPC](https://mainnet.base.org)
- [Base Sepolia RPC](https://sepolia.base.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python examples, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment, wallet, escrow, and network endpoint guidance that should be reviewed before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
