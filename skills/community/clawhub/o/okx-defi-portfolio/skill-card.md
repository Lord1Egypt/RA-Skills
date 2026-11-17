## Description:

Helps agents view OKX DeFi portfolio positions, holdings, and per-protocol position details across supported chains without performing deposit, redeem, claim, wallet-balance, or swap operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect DeFi holdings, summarize positions by protocol and chain, and retrieve identifiers needed for later detail or portfolio-management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may query OKX Agentic Wallet addresses and DeFi position data when the user asks for portfolio views.

Mitigation: Use it only for requested portfolio inspection, confirm automatically resolved addresses when needed, and review displayed results before relying on them.

Risk: Position identifiers shown by this read-only skill can be used by separate invest, redeem, or claim workflows.

Mitigation: Treat identifiers as references only and require explicit user intent before invoking any separate skill that changes positions.

Risk: Mixing incompatible wallet address formats and chains can produce failed or misleading portfolio queries.

Mitigation: Query compatible chain and address groups separately, such as EVM chains with EVM addresses and Solana with Solana addresses.

## Reference(s):

- [OKX Web3](https://web3.okx.com)
- [ClawHub Skill Page](https://clawhub.ai/ok-james-01/skills/okx-defi-portfolio)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown tables with inline shell commands and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only portfolio views; position-detail output includes identifiers that may be used by separate invest, redeem, or claim workflows.]

## Skill Version(s):

3.1.3 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
