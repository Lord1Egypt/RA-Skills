## Description:

HypurrFi helps agents manage DeFi lending on Hyperliquid by depositing assets for yield, borrowing against collateral, and checking positions across supported markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lastandy](https://clawhub.ai/user/lastandy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to manage HypurrFi lending positions on Hyperliquid, including deposits, withdrawals, borrowing, repayment, position checks, and health-factor monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and stores a raw wallet private key locally.

Mitigation: Use a dedicated low-balance wallet, protect or replace ~/.hyperliquid-wallet.json, and avoid sharing the wallet file.

Risk: The skill can sign high-impact on-chain lending and borrowing transactions.

Mitigation: Review transaction previews before execution, use --yes only after review, start with small amounts, and monitor health factor regularly.

Risk: Persistent ERC-20 approvals may remain after transactions.

Mitigation: Check and revoke allowances after repayments or when the wallet no longer needs protocol access.

Risk: Some advertised markets or token addresses are incomplete in the artifact.

Mitigation: Verify supported markets and contract addresses before using Prime, Yield, Vault, or placeholder-address assets.

## Reference(s):

- [HypurrFi homepage](https://hypurr.fi)
- [HypurrFi app](https://app.hypurr.fi)
- [HypurrFi docs](https://docs.hypurr.fi)
- [Hyperliquid explorer](https://explorer.hyperliquid.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-capable command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a locally configured Hyperliquid wallet.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
