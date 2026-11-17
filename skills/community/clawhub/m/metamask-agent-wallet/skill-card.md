## Description:

Guides agents using the MetaMask Agentic CLI for wallet management, blockchain transactions, trading, signing, and x402 payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metamask](https://clawhub.ai/user/metamask)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other wallet users can have an agent prepare and, with appropriate approval, execute MetaMask CLI operations for balances, transfers, signing, swaps, trading, yield, and paid resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet transactions, trades, and x402 payments can move real funds or authorize contracts.

Mitigation: Review the recipient, network, amount, fees, and contract intent before approval; test with small amounts or on testnet first.

Risk: Unattended execution can bypass an intended review step.

Mitigation: Avoid beast mode and --yes unless unattended execution is explicitly intended; pin the skill and CLI versions.

Risk: Wallet credentials and third-party plugins can expose sensitive access.

Mitigation: Never pass mnemonics or passwords on the command line; inspect plugin manifests and requested permissions before installation.

## Reference(s):

- [MetaMask Agent Wallet on ClawHub](https://clawhub.ai/metamask/skills/metamask-agent-wallet)
- [Wallet operations](artifact/references/wallet.md)
- [Transaction operations](artifact/references/transaction.md)
- [Plugin permissions](artifact/references/plugins.md)
- [x402 payments](artifact/references/x402.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operations may require explicit user approval and return pending requests for follow-up.]

## Skill Version(s):

7.7.0 (source: release evidence and skill frontmatter; targets CLI 7.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
